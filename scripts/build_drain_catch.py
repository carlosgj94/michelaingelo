#!/usr/bin/env python3
"""Build four identical removable bench drain cups without changing RT-01.

The canonical part's inlet axis is X0/Y0; +X is radially outward and Z0 is
the flat bench. The main assembly, its STEP and its 25-part print manifest
are inputs only. All checks run in disposable CLI models.
"""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CLI = '/Applications/SolidCraft.app/Contents/MacOS/solidcraft-cli'
OUT = ROOT/'exports/rotary-table/drain-catch'
EVIDENCE = ROOT/'docs/audit-evidence/2026-11-18-rt01/service-follow-up'
BODY = 'P54 removable drain catch'
YELLOW = '#F6C915'


def write(path, value):
    path.write_text(json.dumps(value, indent=2)+'\n')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(script, model=None, save=None, results=False, output=None):
    args = [CLI, 'run', str(script), '--quiet']
    if model:
        args += ['--in', str(model)]
    if save:
        args += ['--save', str(save)]
    if results:
        args += ['--results']
    if output:
        args += ['--json-out', str(output)]
    subprocess.run(args, check=True, cwd=ROOT)


def add(commands, command, **params):
    commands.append(dict(command=command, params=params))


def floor(x):
    return f'dc_inlet_floor-(dc_inlet_floor-dc_sump_floor)*(({x})-dc_inlet_start)/(dc_body_end-dc_wall-dc_inlet_start)'


def prism(commands, body, name, points, plane, depth, operation):
    add(commands, 'sketch.create', name=name, plane=plane)
    add(commands, 'sketch.line', points=points, closed=True, connect=False)
    add(commands, 'sketch.constraint.fix', entities=[f'l{i+1}' for i in range(len(points))], fixed=True)
    add(commands, 'sketch.finish')
    target = dict(body_name=body) if operation == 'new' else dict(targets=[body])
    add(commands, 'solid.extrude', sketch=name, distance=depth, operation=operation, name=name+' extrusion', **target)


def xz_prism(commands, body, name, points, width, operation):
    prism(commands, body, name, points,
          dict(origin=[0, f'({width})/2', 0], x_dir=[1, 0, 0], y_dir=[0, 0, 1]), width, operation)


def parameters(commands):
    for name, expression, comment in [
        ('dc_body_front', '4.5 mm', 'Cup foot starts outside the table flange; fixed RT-01 layout.'),
        ('dc_body_end', '65 mm', 'Outward end relative to the drain axis; rerun all placement checks after changing.'),
        ('dc_width', '40 mm', 'Tangential cup width.'),
        ('dc_height', '24 mm', 'Open cup rim above the flat bench.'),
        ('dc_wall', '2 mm', 'Nominal cup and inlet wall thickness.'),
        ('dc_inlet_start', '-5 mm', 'Inward end of raised inlet, relative to the drain axis.'),
        ('dc_inlet_end', '8 mm', 'Inlet overlap into the main cup.'),
        ('dc_inlet_width', '16 mm', 'Outer inlet width; inner channel is 12 mm.'),
        ('dc_inlet_floor', '15 mm', 'Top of sloping inlet floor at the inward end.'),
        ('dc_sump_floor', '2 mm', 'Floor top at the inner face of the outer wall.'),
    ]:
        add(commands, 'parameters.add', name=name, expression=expression, comment=comment)


def cup(commands, body):
    add(commands, 'solid.box', body_name=body, length='dc_body_end-dc_body_front',
        width='dc_width', height='dc_height', corner=['dc_body_front', '-dc_width/2', 0], operation='new')
    left, right = 'dc_body_front+dc_wall', 'dc_body_end-dc_wall'
    xz_prism(commands, body, body+' sloped cup cavity',
             [[left, floor(left)], [right, 'dc_sump_floor'], [right, 'dc_height+1 mm'], [left, 'dc_height+1 mm']],
             'dc_width-2*dc_wall', 'cut')
    # The underside rises at 45 degrees inward. At R164 it is Z4.5,
    # giving 2 mm over the flange. It grows from the cup during upright printing.
    xz_prism(commands, body, body+' self-supporting raised inlet',
             [['dc_inlet_start', '7.5 mm-dc_inlet_start'], ['7.5 mm', 0], ['dc_inlet_end', 0],
              ['dc_inlet_end', 'dc_height'], ['dc_inlet_start', 'dc_height']],
             'dc_inlet_width', 'join')
    left, right = 'dc_inlet_start+dc_wall', 'dc_inlet_end+1 mm'
    xz_prism(commands, body, body+' continuous downhill inlet channel',
             [[left, floor(left)], [right, floor(right)], [right, 'dc_height+1 mm'], [left, 'dc_height+1 mm']],
             'dc_inlet_width-2*dc_wall', 'cut')
    # The outer pour notch opens at Z20, above the intended Z17 fill mark.
    prism(commands, body, body+' accessible pour notch',
          [[-6, 'dc_height+1 mm'], [6, 'dc_height+1 mm'], [0, 'dc_height-4 mm']],
          dict(origin=['dc_body_end-dc_wall-0.5 mm', 0, 0], x_dir=[0, 1, 0], y_dir=[0, 0, 1]),
          'dc_wall+1.5 mm', 'cut')
    add(commands, 'solid.box', length=8, width=1, height=.6, corner=[40, 17.5, 17],
        operation='join', targets=[body], name=body+' nominal 20mL fill mark')
    add(commands, 'appearance.assign', bodies=[body], color=YELLOW)


def liquid(commands, body, level):
    left, right = 'dc_body_front+dc_wall', 'dc_body_end-dc_wall'
    xz_prism(commands, body, body+' main volume',
             [[left, floor(left)], [right, 'dc_sump_floor'], [right, level], [left, level]],
             'dc_width-2*dc_wall', 'new')
    left, right = 'dc_inlet_start+dc_wall', 'dc_body_front+dc_wall+0.1 mm'
    xz_prism(commands, body, body+' inlet volume',
             [[left, floor(left)], [right, floor(right)], [right, level], [left, level]],
             'dc_inlet_width-2*dc_wall', 'join')
    # Match the small displacement of the internal fill mark.
    add(commands, 'solid.box', length=8, width=1, height=.6, corner=[40, 17.5, 17],
        operation='cut', targets=[body], name=body+' mark displacement')


def move_to_drain(commands, body, q):
    angle = 45+90*q
    a = math.radians(angle)
    add(commands, 'solid.move', bodies=[body], axis=[0, 0, 1], origin=[0, 0, 0], angle=f'{angle} deg')
    add(commands, 'solid.move', bodies=[body], translate=[161*math.cos(a), 161*math.sin(a), 0])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model', type=Path, default=ROOT/'michelaingelo.sc')
    args = parser.parse_args()
    model = args.model.resolve()
    native_before = sha(model)
    OUT.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    build = []
    parameters(build)
    cup(build, BODY)
    add(build, 'view.save', name='P54 drain catch', camera=dict(target=[28, 0, 10], yaw=-.7, pitch=.65, distance=125))
    script = EVIDENCE/'drain-catch-build.json'
    write(script, dict(commands=build))
    measure_path = EVIDENCE/'drain-catch-build.measure.json'
    native = OUT/'p54-removable-drain-catch.sc'
    run(script, save=native, output=measure_path)
    # A repeat save can create a generated backup; it is not part of this handoff.
    Path(str(native)+'.bak').unlink(missing_ok=True)
    measurement = json.loads(measure_path.read_text())
    part = next(b for b in measurement['bodies'] if b['name'] == BODY)
    assert part['closed']
    with tempfile.TemporaryDirectory(prefix='rt01-drain-catch-') as td:
        td = Path(td)
        export = td/'export.json'
        raw = td/'raw.stl'
        write(export, dict(commands=[dict(command='file.export', params=dict(path=str(raw), format='stl', bodies=[BODY], quality='fine'))]))
        run(export, model=native)
        spec = importlib.util.spec_from_file_location('rt01_export', ROOT/'scripts/export_rotary_table.py')
        exporter = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(exporter)
        mesh = exporter.orient_and_check(raw, OUT/'p54-removable-drain-catch.stl', [0, 0, 0])
    mesh['cad_volume_mm3'] = part['volume_mm3']
    mesh['mesh_volume_error_percent'] = 100*abs(mesh['mesh_volume_mm3']-part['volume_mm3'])/part['volume_mm3']
    assert mesh['mesh_volume_error_percent'] < .25

    # Measured liquid volumes are geometry only, not physical flow/storage results.
    capacity = list(build)
    liquid(capacity, 'REVIEW capacity to pour notch', 20)
    liquid(capacity, 'REVIEW capacity to fill mark', 17)
    cap_script = EVIDENCE/'drain-catch-capacity.probe.json'
    write(cap_script, dict(commands=capacity))
    cap_measure = EVIDENCE/'drain-catch-capacity.measure.json'
    run(cap_script, output=cap_measure)
    cap = {b['name']: b['volume_mm3']/1000 for b in json.loads(cap_measure.read_text())['bodies']}

    route = []
    parameters(route)
    part_names = [p['name'] for p in json.loads((ROOT/'cad/parts.json').read_text())['parts']]
    arm_names = json.loads((ROOT/'cad/arm-mount-reference.json').read_text())['collision_body_names']
    world = part_names+arm_names
    labels = {}
    def check(label, command, **params):
        labels[str(len(route))] = label
        add(route, command, **params)
    catches = []
    for q in range(4):
        name = f'REVIEW P54 drain catch {q+1}'
        cup(route, name)
        move_to_drain(route, name, q)
        catches.append(name)
    for q, name in enumerate(catches):
        against = world+[n for n in catches if n != name]
        check(f'drain {q+1} installed', 'inspect.clearance', bodies=[name], against=against, nearest=4)
        a = math.radians(45+90*q)
        # A ray through the whole drain must first meet the continuous sloped cup floor.
        rays = []
        for radial, tangent in [(0, 0), (-2.45, 0), (2.45, 0), (0, -2.45), (0, 2.45)]:
            rays.append(dict(origin=[(161+radial)*math.cos(a)-tangent*math.sin(a),
                                     (161+radial)*math.sin(a)+tangent*math.cos(a), 102.5], dir=[0, 0, -1]))
        check(f'drain {q+1} discharge', 'view.pick', all=True, rays=rays)
        previous = 0
        for distance in [2, 5, 10, 20]:
            add(route, 'solid.move', bodies=[name], translate=[(distance-previous)*math.cos(a), (distance-previous)*math.sin(a), 0])
            check(f'drain {q+1} outward {distance}', 'inspect.clearance', bodies=[name], against=against, nearest=2)
            previous = distance
        add(route, 'solid.move', bodies=[name], translate=[0, 0, 30])
        check(f'drain {q+1} outward20 then lift30', 'inspect.clearance', bodies=[name], against=against, nearest=2)
        add(route, 'solid.move', bodies=[name], translate=[-20*math.cos(a), -20*math.sin(a), -30])

        # Conservative complete envelopes cover every position on both segments.
        envelope = f'REVIEW drain {q+1} outward sweep'
        add(route, 'solid.box', body_name=envelope, length=80.5, width=40, height=24, corner=[4.5, -20, 0], operation='new')
        xz_prism(route, envelope, envelope+' raised inlet', [[-5, 12.5], [4.5, 3], [4.5, 24], [-5, 24]], 16, 'join')
        move_to_drain(route, envelope, q)
        check(f'drain {q+1} complete outward sweep', 'inspect.clearance', bodies=[envelope], against=against, nearest=2)
        lift = f'REVIEW drain {q+1} lift sweep'
        add(route, 'solid.box', body_name=lift, length=70, width=40, height=54, corner=[15, -20, 0], operation='new')
        move_to_drain(route, lift, q)
        check(f'drain {q+1} complete lift sweep', 'inspect.clearance', bodies=[lift], against=against, nearest=2)
    add(route, 'document.inspect', measure=False, sketch_counts=True)
    route_path = EVIDENCE/'drain-catch-route.probe.json'
    write(route_path, dict(commands=route))
    route_result = EVIDENCE/'drain-catch-route.results.json'
    run(route_path, model=model, results=True, output=route_result)
    results = json.loads(route_result.read_text())
    clearances = {label: results[int(i)] for i, label in labels.items() if 'unchecked' in results[int(i)]}
    assert all(not row['overlaps'] and not row['unchecked'] and not row.get('truncated') for row in clearances.values()), clearances
    discharges = {label: results[int(i)] for i, label in labels.items() if label.endswith('discharge')}
    for q, result in enumerate(discharges.values()):
        assert len(result['hits']) == 5 and all(hits and hits[0]['body'] == catches[q] for hits in result['hits']), result
    assert not any(f.get('error') for f in results[-1]['timeline'])
    assert sha(model) == native_before, 'Input assembly changed during accessory generation'

    # Placement-only picture; sweep bodies never enter the saved native assembly.
    placement = []
    parameters(placement)
    for q, name in enumerate(catches):
        cup(placement, name)
        move_to_drain(placement, name, q)
    shot_script = EVIDENCE/'drain-catch-placement.probe.json'
    write(shot_script, dict(commands=placement))
    subprocess.run([CLI, 'snapshot', str(shot_script), '--in', str(model), '--out', str(EVIDENCE/'drain-catch-placement.png'),
                    '--camera', json.dumps(dict(target=[0, -25, 55], yaw=-.85, pitch=1.25, distance=700)), '--no-grid', '--no-axes', '--width', '1400', '--height', '1000'], check=True, cwd=ROOT)
    summary = dict(design='RT-01 P54 removable drain catch', quantity=4, source_native_sha256=native_before,
                   editable_native=dict(file=str(native.relative_to(ROOT)), sha256=sha(native)),
                   placement=dict(drain_radius_mm=161, angles_deg=[45, 135, 225, 315], bench_z_mm=0,
                                  native_inlet_axis_xy_mm=[0, 0], stl_inlet_axis_xy_mm=[5, 20],
                                  orientation='Canonical +X points outward; rotate about inlet axis, then place that axis at R161.',
                                  removal='Move radially outward 20 mm, then lift 30 mm; keep this bench area clear.'),
                   capacities_ml=dict(to_pour_notch=cap['REVIEW capacity to pour notch'], to_fill_mark=cap['REVIEW capacity to fill mark']),
                   flow=dict(floor_drop_mm=13, floor_run_mm=68, slope_degrees=math.degrees(math.atan(13/68)), inlet_floor_at_drain_mm=15-13*5/68, outlet='Accessible outer V-pour notch; empty after outward removal, not a continuous drain.'),
                   route_clearances=clearances, discharge_rays=discharges, discharge_ray_coverage='Centre and radial/tangential offsets +/-2.45 mm at each 5 mm bore; 20 rays total.', print=mesh,
                   instructions=['Print four identical cups upright, flat cup base on the bed; yellow PETG, 0.4 mm nozzle, 0.20 mm layers and four walls.',
                                 'The raised inlet underside is 45 degrees; inspect the sliced tip and bridges. Clean brim off the bench foot.',
                                 'Use a flat, level, rigid bench at Z0. Centre the inlet directly below the drain: the full 5 mm projected bore has 0.5 mm inward and 3.5 mm tangential mouth margins. Verify positioning with a safe tracer before use.',
                                 'Open cups collect incidental drips. Inspect and empty before the Z17 mark; lift and pour through the outer notch, then rinse or brush through the open top.',
                                 'Inspect the existing 0.50 mm printed gutter lip and validate its cleanout method. Never clip this accessory to that lip.',
                                 'Geometric capacity and routes only. No physical flow, splashing, seal, level-tolerance or contaminant-collection performance is claimed.'])
    write(EVIDENCE/'drain-catch-summary.json', summary)
    write(OUT/'drain-catch-manifest.json', {k: summary[k] for k in ['design', 'quantity', 'editable_native', 'placement', 'capacities_ml', 'flow', 'print', 'instructions']})
    print(json.dumps(dict(stl=mesh['file'], sha256=mesh['sha256'], dimensions_mm=mesh['print_bbox_mm'], capacities_ml=summary['capacities_ml'], route_checks=len(clearances)), indent=2))


if __name__ == '__main__':
    main()
