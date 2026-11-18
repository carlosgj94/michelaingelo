#!/usr/bin/env python3
"""Size device reservations in the current RT-01 enclosure and service route."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[1]
CLI = '/Applications/SolidCraft.app/Contents/MacOS/solidcraft-cli'
OUTPUT = ROOT / 'docs/audit-evidence/2026-11-18-rt01/prototype-fit/electronics-space.results.json'
CENTER_Y = -224
REAR_TRAVEL = 140
MINIMUM_CLEARANCE = 1.0

# The reservation includes any plug or ferrule that stays with the device.
OPTIONS = {
    'driver': [(118, 76, 35), (118, 80, 35), (118, 84, 35), (122, 80, 35), (118, 80, 37)],
    'controller': [(80, 55, 20), (108, 64, 20), (114, 68, 20), (118, 70, 20), (114, 68, 21)],
}


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def make_probes():
    commands = read(ROOT / 'cad/support-access-checks.json')['commands']
    boundary = next(i for i, step in enumerate(commands)
                    if step['command'] == 'component.create'
                    and step['params'].get('name') == 'Disposable service tools')
    commands = commands[:boundary]
    hardware = list(dict.fromkeys(step['params']['body_name'] for step in commands
                                  if 'body_name' in step['params']))
    parts = [part['name'] for part in read(ROOT / 'cad/parts.json')['parts']]
    arm = read(ROOT / 'cad/arm-mount-reference.json')['collision_body_names']
    excluded = {'B22 driver packaging envelope', 'B23 controller packaging envelope'}
    obstacles = [name for name in parts + arm + hardware if name not in excluded]
    open_box = [name for name in obstacles
                if name not in ('P52 electronics lid', 'B24 lid gasket', 'P51 removable controller tray')
                and not name.startswith(('TEST F18 ', 'TEST F19 '))]
    commands.append(dict(command='component.create', params=dict(name='Disposable device reservations', grounded=True)))
    tests = []
    for device, choices in OPTIONS.items():
        base, lift = (36, 70.5) if device == 'driver' else (82, 27)
        # The controller rides the tray. Their supporting face is an intended contact.
        installed = [name for name in obstacles
                     if device == 'driver' or name != 'P51 removable controller tray']
        for size in choices:
            width, depth, height = size
            x = -width / 2
            y = CENTER_Y - depth / 2
            shapes = [
                ('installed', [x, y, base], size, installed),
                ('complete lift', [x, y, base], [width, depth, height + lift], open_box),
                ('complete rear withdrawal', [x, y - REAR_TRAVEL, base + lift],
                 [width, depth + REAR_TRAVEL, height], open_box),
            ]
            for phase, corner, shape, against in shapes:
                name = f'REVIEW {device} {size} {phase}'
                commands.append(dict(command='solid.box', params=dict(
                    body_name=name, length=shape[0], width=shape[1], height=shape[2],
                    corner=corner, operation='new')))
                tests.append((device, size, phase, name, len(commands)))
                commands.append(dict(command='inspect.clearance', params=dict(
                    bodies=[name], against=against, nearest=8)))
    return commands, tests


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model', type=Path, default=ROOT / 'michelaingelo.sc')
    parser.add_argument('--out', type=Path, default=OUTPUT)
    args = parser.parse_args()
    commands, tests = make_probes()
    with TemporaryDirectory(prefix='rt01-electronics-') as directory:
        probe = Path(directory) / 'probe.json'
        raw = Path(directory) / 'results.json'
        write(probe, dict(commands=commands))
        subprocess.run([CLI, 'run', str(probe), '--in', str(args.model.resolve()),
                        '--results', '--quiet', '--json-out', str(raw)], check=True)
        results = read(raw)

    candidates = {name: {} for name in OPTIONS}
    for device, size, phase, name, index in tests:
        result = results[index]
        assert not any(result.get(key) for key in ('unchecked', 'truncated', 'pairs_not_checked')), name
        candidate = candidates[device].setdefault(size, {})
        candidate[phase] = dict(nearest=result['nearest'][name], overlaps=result['overlaps'])

    selected = {}
    evidence = {}
    for device, sizes in candidates.items():
        passing = []
        evidence[device] = []
        for size, phases in sizes.items():
            clearances = [pair['distance_mm'] for phase in phases.values() for pair in phase['nearest']
                          if device != 'driver' or not pair['body'].startswith(('M30 driver heat spreader', 'TEST F20 '))]
            narrowest = min(clearances)
            passes = not any(phase['overlaps'] for phase in phases.values()) and narrowest >= MINIMUM_CLEARANCE - 1e-6
            if passes:
                passing.append(size)
            evidence[device].append(dict(size_mm=size, passes=passes, minimum_mm=round(narrowest, 6), phases=phases))
        assert passing, f'No {device} reserve clears the nominal route'
        # Hold driver width and height when alternatives consume service margin.
        if device == 'driver':
            passing = [size for size in passing if size[0] == 118 and size[2] == 35]
            assert passing
        selected[device] = max(passing, key=lambda size: size[0] * size[1] * size[2])

    report = dict(
        source_native_sha256=hashlib.sha256(args.model.read_bytes()).hexdigest(),
        minimum_clearance_mm=MINIMUM_CLEARANCE, selected_reservations_mm=selected,
        scope=['Nominal capacity includes attached rigid connectors within the selected boxes.',
               'The driver-side thermal interface has its own 0.25 mm allowance. Its spreader and flush fasteners remain in overlap checks.',
               'The tray and lid leave before the driver. Device withdrawal follows the recorded lift and rear translation.',
               'Final mounts, flexing leads, hand access, cooling and fitted service need the selected hardware.'],
        candidates=evidence,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    write(args.out, report)
    print(json.dumps(selected))


if __name__ == '__main__':
    main()
