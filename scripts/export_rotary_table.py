#!/usr/bin/env python3
"""Export named RT-01 bodies, orient STLs, and audit their bed fit and topology.

Run from any directory. Requires the installed SolidCraft CLI; no Python packages.
Input defaults to the reviewed native assembly. No geometry is edited in that file.
"""
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import re
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CLI = '/Applications/SolidCraft.app/Contents/MacOS/solidcraft-cli'


def slug(name):
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')


def rotate(p, angles):
    x, y, z = p
    for axis, degrees in enumerate(angles):
        c, s = round(math.cos(math.radians(degrees)), 12), round(math.sin(math.radians(degrees)), 12)
        if axis == 0:
            y, z = c*y-s*z, s*y+c*z
        elif axis == 1:
            x, z = c*x+s*z, -s*x+c*z
        else:
            x, y = c*x-s*y, s*x+c*y
    return (x, y, z)


def orient_and_check(source, destination, angles):
    raw = source.read_bytes()
    count = struct.unpack_from('<I', raw, 80)[0]
    if len(raw) != 84 + 50*count:
        raise ValueError(f'Expected binary STL: {source}')
    triangles = []
    for i in range(count):
        row = struct.unpack_from('<12fH', raw, 84+50*i)
        triangles.append((rotate(row[:3], angles), [rotate(row[j:j+3], angles) for j in (3, 6, 9)]))
    minimum = [min(v[k] for _, tri in triangles for v in tri) for k in range(3)]
    maximum = [max(v[k] for _, tri in triangles for v in tri) for k in range(3)]
    bounds = [maximum[k]-minimum[k] for k in range(3)]
    if any(d > 168.001 for d in bounds) or any(d+10 > 180.001 for d in bounds[:2]):
        raise ValueError(f'Part exceeds A1 Mini print allowance: {destination.name}: {bounds}')
    data = bytearray(b'RT-01 oriented print mesh; units mm'.ljust(80, b'\0') + struct.pack('<I', count))
    edges, directed = Counter(), Counter()
    signed_volume, degenerate = 0.0, 0
    for normal, tri in triangles:
        tri = [tuple(v[k]-minimum[k] for k in range(3)) for v in tri]
        # Audit the exact float32 vertices that will be written, not higher precision intermediates.
        tri = [struct.unpack('<3f', struct.pack('<3f', *v)) for v in tri]
        a, b, c = tri
        cross = (b[1]*c[2]-b[2]*c[1], b[2]*c[0]-b[0]*c[2], b[0]*c[1]-b[1]*c[0])
        signed_volume += sum(a[k]*cross[k] for k in range(3))/6
        points = [tuple(round(v, 5) for v in point) for point in tri]
        if len(set(points)) != 3:
            degenerate += 1
        for j in range(3):
            u, v = points[j], points[(j+1) % 3]
            edges[tuple(sorted((u, v)))] += 1
            directed[(u, v)] += 1
        data += struct.pack('<12fH', *normal, *(v for point in tri for v in point), 0)
    bad_edges = sum(n != 2 for n in edges.values())
    bad_winding = sum(directed[(v, u)] != n for (u, v), n in directed.items())
    if bad_edges or bad_winding or degenerate or signed_volume <= 0:
        raise ValueError(f'Mesh audit failed: {destination.name}: edges={bad_edges}, winding={bad_winding}, degenerate={degenerate}, volume={signed_volume}')
    destination.write_bytes(data)
    return dict(file=str(destination.relative_to(ROOT)), triangles=count,
                print_bbox_mm=[round(v, 4) for v in bounds],
                footprint_with_5mm_brim_mm=[round(v+10, 4) for v in bounds[:2]],
                mesh_volume_mm3=round(signed_volume, 4), closed_edges=True,
                consistent_winding=True, sha256=hashlib.sha256(data).hexdigest())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--in', dest='native', type=Path, default=ROOT/'michelaingelo.sc')
    args = parser.parse_args()
    parts = json.loads((ROOT/'cad/parts.json').read_text())['parts']
    out = ROOT/'exports/rotary-table'
    for folder in ['stl', 'metal']:
        (out/folder).mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='rt01-export-') as temp:
        temp = Path(temp)
        commands = []
        printed = [p for p in parts if p['kind'] == 'print']
        for part in printed:
            commands.append({'command': 'file.export', 'params': {
                'path': str(temp/(slug(part['name'])+'.stl')), 'format': 'stl',
                'bodies': [part['name']], 'quality': 'fine'}})
        commands.append({'command': 'file.export', 'params': {
            'path': str(out/'rt01-assembly.step'), 'format': 'step',
            'bodies': [p['name'] for p in parts]}})
        for part in parts:
            if part['kind'] == 'metal':
                commands.append({'command': 'file.export', 'params': {
                    'path': str(out/'metal'/(slug(part['name'])+'.step')),
                    'format': 'step', 'bodies': [part['name']]}})
        commands.append({'command': 'file.export', 'params': {
            'path': str(out/'seal-profiles.step'), 'format': 'step',
            'bodies': [p['name'] for p in parts if 'gasket' in p['name']]}})
        script = temp/'export.json'
        script.write_text(json.dumps({'commands': commands}))
        measurement = temp/'measure.json'
        subprocess.run([CLI, 'run', str(script), '--in', str(args.native.resolve()),
                        '--json-out', str(measurement), '--quiet'], check=True)
        bodies = {b['name']: b for b in json.loads(measurement.read_text())['bodies']}
        results = []
        for part in printed:
            filename = slug(part['name'])+'.stl'
            result = orient_and_check(temp/filename, out/'stl'/filename, part['print_rotation_deg'])
            result.update(name=part['name'], rotation_deg=part['print_rotation_deg'], notes=part['notes'])
            cad_volume = bodies[part['name']]['volume_mm3']
            result['cad_volume_mm3'] = cad_volume
            result['mesh_volume_error_percent'] = round(100*abs(result['mesh_volume_mm3']-cad_volume)/cad_volume, 6)
            if result['mesh_volume_error_percent'] > 0.25:
                raise ValueError(f'Tessellation volume discrepancy: {part["name"]}')
            results.append(result)
        manifest = dict(design='RT-01', units='mm', nozzle_mm=0.4, layer_mm=0.2,
                        note='Prototype geometry. Print coupon first. No slicing or physical print verification implied.',
                        parts=results)
        coupon = out/'fit-coupon.stl'
        if coupon.exists():
            manifest['coupon'] = orient_and_check(coupon, coupon, [0, 0, 0])
        (out/'print-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
        print(json.dumps(dict(exported=len(results), largest_dimension_mm=max(max(r['print_bbox_mm']) for r in results),
                              max_mesh_volume_error_percent=max(r['mesh_volume_error_percent'] for r in results)), indent=2))


if __name__ == '__main__':
    main()
