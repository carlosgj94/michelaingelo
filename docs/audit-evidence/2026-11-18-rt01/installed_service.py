"""Replay RT-01 service poses with the hardware from the registered assembly check."""
import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


def service_commands(source):
    population = json.loads(source.read_text())["commands"]
    check = population[-1]
    if check["command"] != "inspect.interference":
        raise ValueError("Expected the last assembly-check command to contain the populated body list")
    bodies = check["params"]["bodies"]
    commands = population[:-1]
    commands.append({"command": "component.activate", "params": {"component": "root"}})
    stages = {}

    def move(parts, xyz):
        commands.append({"command": "solid.move", "params": {"bodies": parts, "translate": xyz}})

    def inspect(label, parts, removed=(), screw_groups=()):
        absent = set(parts) | set(removed)
        against = [b for b in bodies if b not in absent and not b.startswith(screw_groups)]
        commands.append({"command": "inspect.clearance", "params": {
            "bodies": parts, "against": against, "nearest": 3}})
        stages[len(commands) - 1] = label

    hood = ["P46 motor service hood"]
    def hood_pose(label):
        inspect(label, hood, screw_groups=("TEST F17 ",))

    hood_pose("hood seated")
    move(hood, [0, 0, 8])
    hood_pose("hood lifted 8")
    move(hood, [0, 0, -8])
    x = 0
    for new_x in (2, 5, 10, 20, 30, 50, 70):
        move(hood, [new_x - x, 0, 0])
        x = new_x
        hood_pose(f"hood outward {x}")
    move(hood, [0, 0, 30])
    hood_pose("hood outward 70 then up 30")
    move(hood, [0, 0, -30])
    move(hood, [-70, 0, 0])

    removed = []
    for label, parts, heights, released in [
        ("lid", ["P52 electronics lid", "B24 lid gasket"], (8,), ("TEST F18 ",)),
        ("tray", ["P51 removable controller tray", "B23 controller packaging envelope"],
         (27,), ("TEST F18 ", "TEST F19 ")),
        ("driver", ["B22 driver packaging envelope"], (60, 62, 63, 65, 68, 70),
         ("TEST F18 ", "TEST F19 ")),
    ]:
        height = 0
        for h in heights:
            move(parts, [0, 0, h - height])
            height = h
            inspect(f"{label} lift {h}", parts, removed, released)
        y = 0
        for distance in (10, 20, 30, 40, 50, 60, 70, 80, 100, 120, 140):
            move(parts, [0, y - distance, 0])
            y = distance
            inspect(f"{label} rearward {y}", parts, removed, released)
        removed.extend(parts)
        if label != "driver":
            move(parts, [300, 0, 0])
    return commands, stages


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, default=Path("michelaingelo.sc"))
    parser.add_argument("--population", type=Path, default=Path("cad/hardware-assembly-check.json"))
    parser.add_argument("--out", type=Path, required=True, help="Output JSON for the service inspections")
    args = parser.parse_args()
    if args.out.resolve() in (args.model.resolve(), args.population.resolve()) or args.out.suffix != ".json":
        parser.error("Choose a separate .json file for results")
    commands, stages = service_commands(args.population)
    with tempfile.TemporaryDirectory(prefix="rt01-service-") as work:
        work = Path(work)
        probe = work / "service.json"
        raw = work / "raw.json"
        probe.write_text(json.dumps({"commands": commands}))
        subprocess.run([shutil.which("solidcraft-cli") or "solidcraft-cli", "run", str(probe),
                        "--in", str(args.model.resolve()), "--results", "--quiet", "--json-out", str(raw)], check=True)
        values = json.loads(raw.read_text())
    selected = {label: {k: values[i][k] for k in ("overlaps", "nearest", "unchecked", "truncated")}
                for i, label in stages.items()}
    args.out.write_text(json.dumps(selected, indent=2) + "\n")
