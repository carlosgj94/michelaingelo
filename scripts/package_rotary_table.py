#!/usr/bin/env python3
"""Package and verify the current RT-01 prototype handoff."""
import argparse
import hashlib
import json
import re
from os.path import relpath
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import urlsplit
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
EXPORT = ROOT / 'exports/rotary-table'
ARCHIVE = EXPORT / 'rt01-print-package.zip'
REPOSITORY = 'https://github.com/carlosgj94/michelaingelo'
REPOSITORY_DOCUMENTS = f'{REPOSITORY}/blob/main'
BOM = 'docs/rotary-table-bom.md'
ARM_REFERENCE = 'references/so-arm100/README.md'
REPOSITORY_ONLY = {
    BOM: f'{REPOSITORY_DOCUMENTS}/{BOM}',
    ARM_REFERENCE: f'{REPOSITORY_DOCUMENTS}/{ARM_REFERENCE}',
    ARCHIVE.relative_to(ROOT).as_posix(): f'{REPOSITORY_DOCUMENTS}/{ARCHIVE.relative_to(ROOT).as_posix()}',
    'docs/archive': f'{REPOSITORY}/tree/main/docs/archive',
}
# These three links predate moving the revision 3 report into docs/archive.
REV3_SOURCE = f'{REPOSITORY}/blob/a403195eeeeea3a8b877d0101240158d2ee1bd07'
REV3_LINKS = {
    '../cad/validation-results.json': f'{REV3_SOURCE}/cad/validation-results.json',
    'rotary-table-fasteners.md': f'{REV3_SOURCE}/docs/rotary-table-fasteners.md',
    '../exports/rotary-table/print-manifest.json': f'{REV3_SOURCE}/exports/rotary-table/print-manifest.json',
}
MARKDOWN_LINK = re.compile(r'\]\(([^\s)]+)\)')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def accessory_hashes(report):
    drain = read_json(EXPORT / 'drain-catch/drain-catch-manifest.json')
    seats = read_json(EXPORT / 'arm-seats/p55-seat-manifest.json')
    fixture = read_json(EXPORT / 'foam-fixture/foam-fixture-manifest.json')
    # The arm-seat and fixture clearances were checked against this assembly.
    for manifest in (seats, fixture):
        assert manifest['source_native_sha256'] == report['native_sha256'], 'Accessory uses stale assembly'

    artifacts = [drain['editable_native'], drain['print'], seats['editable_model'], fixture['editable_assembly']]
    hashes = {item['file']: item['sha256'] for item in artifacts}
    hashes.update({part['print_file']: part['sha256'] for part in seats['parts']})
    for part in fixture['prints']:
        hashes[part['file']] = part['sha256']
        hashes[part['editable_native_file']] = part['editable_native_sha256']

    prototype_evidence = ROOT / 'docs/audit-evidence/2026-11-18-rt01/prototype-fit'
    worm = read_json(prototype_evidence / 'prototype-worm-fit.results.json')
    hashes['exports/rotary-table/drive-study/swg2-r1-ag2-40r1-layout.sc'] = worm['study_model_sha256']
    slices = read_json(prototype_evidence / 'a1-mini-slice.results.json')
    for group in slices['parts'].values():
        for part in group['files']:
            assert hashes[part['file']] == part['sha256'], f'Slice evidence differs for {part["file"]}'
    return hashes


def package_members():
    files = [ROOT / 'michelaingelo.sc', ROOT / 'README.md']
    files += list((ROOT / 'cad').glob('*.json')) + list((ROOT / 'cad').glob('*.csv'))
    files += list((ROOT / 'scripts').glob('*.py'))
    files += list((ROOT / 'docs').glob('rotary-table-*')) + [ROOT / 'docs/specs/rotary-table.md']
    files += [p for p in (ROOT / 'docs/audit-evidence').rglob('*')
              if p.is_file() and p.suffix in ('.json', '.py', '.png', '.sc', '.step', '.stl')]
    files += [ROOT / 'docs/archive/rotary-table-spec-rev3.md', ROOT / 'docs/archive/rotary-table-validation-rev3.md']
    files += [p for p in EXPORT.rglob('*')
              if p.is_file() and p.suffix in ('.json', '.py', '.sc', '.step', '.stl', '.png')]
    return sorted({p.relative_to(ROOT).as_posix() for p in files if p.is_file()} - REPOSITORY_ONLY.keys())


def portable_markdown(member, members):
    source = ROOT / member

    def rewrite(match):
        target = match[1]
        url = urlsplit(target)
        if url.scheme or url.netloc or not url.path:
            return match[0]
        if member == 'docs/archive/rotary-table-validation-rev3.md' and target in REV3_LINKS:
            return f']({REV3_LINKS[target]})'
        relative_target = Path(relpath(source.parent / url.path, ROOT)).as_posix()
        if relative_target in REPOSITORY_ONLY:
            suffix = ('?' + url.query if url.query else '') + ('#' + url.fragment if url.fragment else '')
            return f']({REPOSITORY_ONLY[relative_target]}{suffix})'
        if relative_target not in members and not any(p.startswith(f'{relative_target}/') for p in members):
            raise ValueError(f'{member} links to missing package file {target}')
        return match[0]

    return MARKDOWN_LINK.sub(rewrite, source.read_text(encoding='utf-8'))


def write_package(archive, members, revision, assembly_meshes, hashes):
    note = (
        f'RT-01 revision {revision} foam prototype\n\n'
        f'Open README.md and the revision {revision} response in docs/rotary-table-design-audit-2026-11-18.md.\n'
        'The CAD and package follow-up in that audit records the revised F19 service and P54 capacities.\n'
        f'{len(assembly_meshes)} oriented assembly STLs, a fit coupon, and one drain catch STL to print four times.\n'
        'The arm-seat and foam-fixture folders contain the prototype prints and their manifests.\n'
        'Use the metal STEP files with the machining specification and supplier drawings.\n'
        'The native assembly, generators and verification evidence are included.\n'
        'The repository holds the current bill of materials, SO100 arm reference and historical native files.\n'
        f'{REPOSITORY_ONLY[BOM]}\n'
        f'{REPOSITORY_ONLY[ARM_REFERENCE]}\n'
        'Physical fit, load, thermal, ingress and stopping acceptance remain pending.\n'
    )
    included = set(members)
    archive.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix='.rt01-package-', dir=archive.parent) as directory:
        candidate = Path(directory) / archive.name
        with ZipFile(candidate, 'w', compression=ZIP_DEFLATED, compresslevel=9) as bundle:
            for member in members:
                if member.endswith('.md'):
                    bundle.writestr(member, portable_markdown(member, included))
                else:
                    bundle.write(ROOT / member, member)
            bundle.writestr('README-FIRST.txt', note)
        with ZipFile(candidate) as bundle:
            assert bundle.testzip() is None
            assert set(bundle.namelist()) == included | {'README-FIRST.txt'}
            assert {n for n in bundle.namelist() if n.startswith('exports/rotary-table/stl/')
                    and n.endswith('.stl')} == assembly_meshes
            for name, expected in hashes.items():
                assert hashlib.sha256(bundle.read(name)).hexdigest() == expected, name
        candidate.replace(archive)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ARCHIVE, help='Archive destination')
    archive = parser.parse_args().output.resolve()
    report = read_json(ROOT / 'cad/validation-results.json')
    manifest = read_json(EXPORT / 'print-manifest.json')
    revision = read_json(ROOT / 'cad/parts.json')['revision']
    assert report['revision'] == manifest['revision'] == revision
    assembly_meshes = {part['file'] for part in manifest['parts']}
    assert len(assembly_meshes) == 25
    print_hashes = {part['file']: part['sha256'] for part in manifest['parts'] + [manifest['coupon']]}
    hashes = {'michelaingelo.sc': report['native_sha256']}
    for recorded_hashes in (report['evidence_sha256'], print_hashes, accessory_hashes(report)):
        for name, expected in recorded_hashes.items():
            assert hashes.setdefault(name, expected) == expected, f'Conflicting recorded hashes: {name}'
    members = package_members()
    for name, expected in hashes.items():
        assert name in members, f'Hashed evidence missing from package: {name}'
        assert sha(ROOT / name) == expected, f'Hash mismatch: {name}'

    write_package(archive, members, revision, assembly_meshes, hashes)
    print(json.dumps(dict(file=relpath(archive, ROOT), entries=len(members) + 1,
                          bytes=archive.stat().st_size, sha256=sha(archive))))


if __name__ == '__main__':
    main()
