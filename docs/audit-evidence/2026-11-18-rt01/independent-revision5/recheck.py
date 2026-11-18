"""Replay the independent revision 5 service, seal and drain measurements on a disposable model."""
import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[4]


def read(path):
    return json.loads(path.read_text())


def probes():
    service = read(ROOT / "cad/support-access-checks.json")["commands"]
    parts = [row["name"] for row in read(ROOT / "cad/parts.json")["parts"]]
    arm = read(ROOT / "cad/arm-mount-reference.json")
    world = parts + arm["collision_body_names"]
    # The published service script constructs all 119 fasteners before its first service tool.
    boundary = next(i for i, row in enumerate(service)
                    if row["params"].get("name") == "Disposable service tools")
    commands = service[:boundary]
    labels = {}

    def add(command, **params):
        commands.append({"command": command, "params": params})

    def measure(label, command, **params):
        labels[len(commands)] = label
        add(command, **params)

    def cylinder(name, diameter, x, y, zmin, zmax, operation="new"):
        target = {"body_name": name} if operation == "new" else {"targets": [name]}
        add("solid.cylinder", diameter=diameter, height=zmax-zmin, base=[x, y, zmin],
            operation=operation, **target)

    def box(name, corner, dimensions, operation="new"):
        target = {"body_name": name} if operation == "new" else {"targets": [name]}
        length, width, height = dimensions
        add("solid.box", length=length, width=width, height=height, corner=corner,
            operation=operation, **target)

    def clearance(label, name, against):
        measure(label, "inspect.clearance", bodies=[name], against=against, nearest=2)

    def obstacles(moving):
        return next(row["params"]["against"] for row in service
                    if row["command"] == "inspect.clearance" and row["params"]["bodies"] == moving)

    add("component.create", name="Independent revision 5 gauges", grounded=True)
    # Measure the lip and discharge before placing any artificial solid in a drain.
    box("Review flat bench", [-320, -400, -30], [640, 720, 30])
    for i in range(4):
        angle = math.radians(45 + 90*i)
        u, v = math.cos(angle), math.sin(angle)
        x, y = 161*u, 161*v
        rays = [{"origin": [x+a*u-b*v, y+a*v+b*u, 95.95], "dir": [0, 0, -1]}
                for a, b in [(0, 0), (2.45, 0), (-2.45, 0), (0, 2.45), (0, -2.45)]]
        measure(f"Drain {i} discharge over flat bench", "view.pick", rays=rays, all=True)
        measure(f"Drain {i} radial wall at Z101", "view.pick", all=True,
                rays=[{"origin": [r*u, r*v, 101], "dir": [u, v, 0]} for r in (161, 163.55)])
        name = f"Review drain {i}"
        cylinder(name, 4.98, x, y, .01, 102.5)
        clearance(f"Drain {i} full height gauge", name, world)

    for i, point in enumerate(arm["adapter_holes"]):
        x, y, _ = point["plate_hole_center_mm"]
        washer = f"Review F24 washer {i}"
        cylinder(washer, 9, x, y, 168, 168.8)
        cylinder(washer, 4.3, x, y, 167.5, 169.5, "cut")
        clearance(f"F24 site {i} flat washer to foot", washer, [arm["body"]])
        for label, diameter, bottom, height in [
            ("long AF3 inscribed tool", 3, 172.8, 85), ("short AF3 tool envelope", 3.47, 172.8, 40),
            ("23.5 mm screw head insertion", 7, 168.8, 27.5),
        ]:
            name = f"Review F24 {i} {label}"
            cylinder(name, diameter, x, y, bottom, bottom+height)
            clearance(f"F24 site {i} {label}", name, arm["collision_body_names"])

    diameter = math.sqrt(4**2 + (9**2 - 3.8**2)/.75)
    for i, (x, y) in enumerate((x, y) for x in [-75, 75] for y in [-271, -177]):
        name = f"Review compressed F21 ring {i}"
        cylinder(name, diameter, x, y, 32, 32.75)
        cylinder(name, 4, x, y, 31.5, 33.5, "cut")
        clearance(f"F21 site {i} constant-volume circular seal", name, ["P50 electronics service box"])

    for i, (x, sign) in enumerate([(-52, 1), (52, -1)]):
        against = obstacles([f"TEST F07 side key {i}"])
        for height in [15, 12]:
            name = f"Review F07 key {i} height {height}"
            cylinder(name, 5, x, 18, 23, 23+height)
            box(name, [x-2.5, -47, 23+height-5], [5, 65, 5], "join")
            def turn(degrees):
                add("solid.move", bodies=[name], axis=[0, 0, 1], origin=[x, 18, 23],
                    angle=sign*degrees)

            if height == 15:
                turn(60)
                previous = 0
                for dz in [0, 2.9, 3, 3.1, 5]:
                    if dz:
                        add("solid.move", bodies=[name], translate=[0, 0, dz-previous])
                    clearance(f"F07 {i} specified key at 60 deg lift {dz}", name, against)
                    previous = dz
                continue

            for stroke, angles in [("engaged", range(0, 61, 5)), ("released", range(60, -1, -5))]:
                previous = angles[0]
                for angle in angles:
                    if angle != previous:
                        turn(angle-previous)
                    clearance(f"F07 {i} short key {stroke} at {angle} deg", name, against)
                    previous = angle
                direction = 1 if stroke == "engaged" else -1
                for step in range(1, 6):
                    add("solid.move", bodies=[name], translate=[0, 0, direction])
                    clearance(f"F07 {i} short key after {stroke} stroke step {step}", name, against)

    tray = ["P51 removable controller tray", "B23 controller packaging envelope"]
    for i, (x, y) in enumerate((x, y) for x in [-65, 65] for y in [-258, -190]):
        against = obstacles(tray) + tray + [f"TEST F19 {j}" for j in range(4) if j != i]
        name = f"Review F19 long key {i}"
        cylinder(name, 2, x, y, 84.15, 159.15)
        clearance(f"F19 site {i} straight AF2 core", name, against)
        # Rear entry at Z106.5 then lower to Z83. Probe includes the 30 mm bit and hub.
        name = f"Review F19 horizontal sweep {i}"
        box(name, [x-4, -306, 106.5], [8, y+310, 30])
        clearance(f"F19 site {i} compact rear entry", name, against)
        name = f"Review F19 vertical sweep {i}"
        cylinder(name, 2.31, x, y, 83, 129.5)
        cylinder(name, 8, x, y, 105, 136.5, "join")
        clearance(f"F19 site {i} compact vertical engagement", name, against)

    carrier = "M60 monolithic worm carrier"
    previous = 0
    for offset in [0, -3, 3]:
        if offset:
            add("solid.move", bodies=[carrier], translate=[offset-previous, 0, 0])
        for i, x in enumerate([-64, 64]):
            name = f"Review F02 head {i}"
            if offset == 0:
                cylinder(name, 10, x, 64, 13.6, 19.6)
            clearance(f"F02 head {i} at carrier X{offset}", name, [carrier])
        previous = offset
    return commands, labels


def compact(row):
    if "hits" in row:
        return {"first_hits": [
            {"body": hits[0]["body"], "depth_mm": round(hits[0]["depth"], 6)} if hits else None
            for hits in row["hits"]
        ]}
    return {
        "nearest": [[p["body"], round(p["distance_mm"], 6)] for p in next(iter(row["nearest"].values()))],
        "overlaps_mm3": [[p["a"], p["b"], round(p["volume_mm3"], 6)] for p in row["overlaps"]],
        "unchecked": row["unchecked"], "truncated": row["truncated"],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, default=ROOT / "michelaingelo.sc")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    commands, labels = probes()
    with TemporaryDirectory(prefix="rt01-recheck-") as directory:
        probe, raw = (Path(directory) / name for name in ("probe.json", "raw.json"))
        probe.write_text(json.dumps({"commands": commands}))
        subprocess.run(["solidcraft-cli", "run", str(probe), "--in", str(args.model.resolve()),
                        "--results", "--quiet", "--json-out", str(raw)], check=True)
        measured = read(raw)
    results = {
        "native_sha256": hashlib.sha256(args.model.read_bytes()).hexdigest(),
        "solidcraft": subprocess.check_output(["solidcraft-cli", "--version"], text=True).strip(),
        "checks": {label: compact(measured[index]) for index, label in labels.items()},
    }
    args.out.write_text(json.dumps(results, indent=2) + "\n")
