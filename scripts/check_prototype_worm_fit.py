#!/usr/bin/env python3
"""Check the catalogue SWG2-R1 / AG2-40R1 alternative in the RT-01 core."""
import json
import math
from pathlib import Path
from tempfile import TemporaryDirectory

from build_drain_catch import ROOT, add, run, sha, write


EVIDENCE = ROOT / 'docs/audit-evidence/2026-11-18-rt01/prototype-fit'
EXPORT = ROOT / 'exports/rotary-table/drive-study/swg2-r1-ag2-40r1-layout.sc'
WORM = 'KHK SWG2-R1 worm'
WHEEL = 'KHK AG2-40R1 wheel'
HUB = 'M20 registered output hub'
SHAFT = 'B03 worm shaft reference'
PIN = 'M21 wheel drive pin'
OLD_GEARS = {'B04 duplex worm envelope', 'B11 duplex wheel envelope'}
CATALOGUE = 'https://khkgears.net/pdf/2025/worm-gears.pdf'


def cylinder(commands, body, diameter, length, base, axis='Z', operation='new'):
    selection = dict(body_name=body) if operation == 'new' else dict(targets=[body])
    add(commands, 'solid.cylinder', diameter=diameter, height=length, base=base,
        axis=axis, operation=operation, name=f'{body} {operation} Ø{diameter}', **selection)


def gears(commands, worm_bore):
    cylinder(commands, WORM, 35, 32, [-16, 55.5, 50], 'X')
    cylinder(commands, WORM, 25, 3, [-19, 55.5, 50], 'X', 'join')
    cylinder(commands, WORM, 25, 15, [16, 55.5, 50], 'X', 'join')
    cylinder(commands, WORM, worm_bore, 52, [-20, 55.5, 50], 'X', 'cut')
    cylinder(commands, WHEEL, 86, 18, [0, 0, 41])
    cylinder(commands, WHEEL, 45, 15, [0, 0, 59], operation='join')
    cylinder(commands, WHEEL, 12, 35, [0, 0, 40], operation='cut')
    add(commands, 'appearance.assign', bodies=[WORM, WHEEL], color='#242424')


def drill_wheel_hub(commands):
    # F05 is represented at the thread major diameter for the collision probe.
    for x, y in [(15, 0), (0, 15), (-15, 0), (0, -15)]:
        cylinder(commands, WHEEL, 5, 13, [x, y, 62], operation='cut')

    # Preserve the existing M21 radial slot and conservatively check its full length.
    cutter = 'Study wheel radial slot'
    add(commands, 'solid.box', body_name=cutter, length=2, width=4.01, height=6.3,
        corner=[14, -2.005, 67.8], operation='new')
    for x in (14, 16):
        cylinder(commands, cutter, 4.01, 6.3, [x, 0, 67.8], operation='join')
    add(commands, 'solid.move', bodies=[cutter], axis=[0, 0, 1], origin=[0, 0, 0], angle='45 deg')
    add(commands, 'solid.combine', target=WHEEL, tools=[cutter], operation='cut')


def read(path):
    return json.loads(path.read_text())


def main():
    model = ROOT / 'michelaingelo.sc'
    source_sha = sha(model)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    EXPORT.parent.mkdir(parents=True, exist_ok=True)

    setup = read(ROOT / 'cad/support-access-checks.json')['commands']
    boundary = next(i for i, step in enumerate(setup)
                    if step['command'] == 'component.create'
                    and step['params'].get('name') == 'Disposable service tools')
    commands = setup[:boundary]
    fasteners = list(dict.fromkeys(step['params']['body_name'] for step in commands
                                   if 'body_name' in step['params']))
    parts = [part['name'] for part in read(ROOT / 'cad/parts.json')['parts']]
    world = [name for name in parts if name not in OLD_GEARS] + fasteners

    with TemporaryDirectory(prefix='rt01-worm-fit-') as directory:
        script = Path(directory) / 'probe.json'
        raw = Path(directory) / 'results.json'
        tests = {}
        add(commands, 'component.create', name='Disposable KHK prototype drive', grounded=True)
        gears(commands, 12)

        def check(label, body, obstacles):
            tests[label] = len(commands)
            add(commands, 'inspect.clearance', bodies=[body], against=obstacles, nearest=5)

        check('stock worm bore against existing shaft', WORM, [SHAFT])
        check('stock wheel bore against existing pilot', WHEEL, [HUB])
        # Resize only the cylindrical locating nose. Leave M20 seating face and
        # M21 unchanged. This cut is confined below the wheel seating plane.
        ring = 'Study M20 pilot turning allowance'
        cylinder(commands, ring, 15.5, 7.01, [0, 0, 66.99])
        cylinder(commands, ring, 11.98, 7.03, [0, 0, 66.98], operation='cut')
        add(commands, 'solid.combine', target=HUB, tools=[ring], operation='cut')
        cylinder(commands, WORM, 15, 52, [-20, 55.5, 50], 'X', 'cut')
        drill_wheel_hub(commands)
        check('machined worm against retained assembly', WORM, world)
        check('machined wheel against retained assembly', WHEEL, world)

        # Constant radial/axial blank envelopes cover wheel rotation against
        # stationary bodies. Omit intentionally co-rotating contact interfaces.
        cylinder(commands, 'Study rotating wheel outer sweep', 86, 18, [0, 0, 41])
        cylinder(commands, 'Study rotating wheel outer sweep', 45, 15, [0, 0, 59], operation='join')
        check('wheel sweep against stationary assembly', 'Study rotating wheel outer sweep',
              [n for n in world if n not in {HUB, PIN, SHAFT} and
               not n.startswith(('TEST F05 ', 'TEST F25 ', 'B07 ', 'B12 ', 'B10 '))])
        write(script, dict(commands=commands))
        run(script, model=model, results=True, output=raw)
        results = read(raw)
        fits = {label: results[index] for label, index in tests.items()}
        assert all(not any(fit.get(key) for key in ('unchecked', 'truncated', 'pairs_not_checked'))
                   for fit in fits.values())
        assert all(fit['overlaps'] for label, fit in fits.items() if label.startswith('stock'))
        assert not any(fit['overlaps'] for label, fit in fits.items() if not label.startswith('stock')), fits

        commands = []
        add(commands, 'component.create', name='KHK prototype drive catalogue pair', grounded=True)
        gears(commands, 12)
        add(commands, 'view.save', name='KHK 40:1 stock pair',
            camera=dict(target=[0, 22, 52], yaw=-.8, pitch=.65, distance=195))
        write(script, dict(commands=commands))
        run(script, save=EXPORT, output=raw)
        bodies = read(raw)['bodies']
        assert len(bodies) == 2 and all(body['closed'] for body in bodies)
        EXPORT.with_suffix('.sc.bak').unlink(missing_ok=True)

    assert sha(model) == source_sha
    write(EVIDENCE / 'prototype-worm-fit.results.json', dict(
        source_native_sha256=source_sha,
        study_model_sha256=sha(EXPORT),
        manufacturer_drawing=CATALOGUE,
        centre_distance_mm=55.5,
        shaft_z_mm=50,
        scope=[
            'The editable study shows the two unmachined stock envelopes.',
            'The assembled probe uses the 15 mm worm bore, 11.98 mm M20 pilot and F05/M21 relief in the wheel boss.',
            'The shaft key, shoulders, spacers, axial retention and bearing preload require final machining drawings.',
            'Tooth shapes and contact pattern are outside the envelope checks.',
        ],
        catalog_backlash_mm=[.06, .16],
        catalog_backlash_at_platter_degrees=[math.degrees(value / 40) for value in (.06, .16)],
        fits=fits,
        study_bodies=bodies,
    ))


if __name__ == '__main__':
    main()
