# RT-01 printing and assembly

Use the [specification](specs/rotary-table.md) and [BOM](rotary-table-bom.md) with this guide. The STLs are prototype parts, not evidence of validated cutting accuracy or payload. Print the coupon and obtain the bought-component drawings before printing the entire assembly.

## Files and printer setup

- `exports/rotary-table/stl/`: 33 individual assembly parts, already rotated into the proposed print orientation and placed at Z0. Units: **millimetres**. Import individually; do not apply uniform scaling.
- `exports/rotary-table/fit-coupon.stl`: separate 140 × 70 × 8 mm calibration coupon.
- `exports/rotary-table/print-manifest.json`: per-part dimensions, orientation, triangle count, volume check and checksum.
- `exports/rotary-table/metal/`: five aluminium parts as STEP machining references.
- `exports/rotary-table/rt01-assembly.step`: complete table with named bought-component envelopes; excludes the arm. Cyan packaging volumes are not physical components.
- `exports/rotary-table/seal-profiles.step`: gasket profiles shown at **compressed** thickness. Cut sheet stock at the uncompressed thickness in the BOM.

Bambu A1 Mini: 180 × 180 × 180 mm, 0.4 mm nozzle, 0.20 mm layers, dry PETG. Use the matching manufacturer filament profile as a starting point. Calibrate flow, first layer and elephant-foot compensation. Keep functional faces free of brim residue. The largest part dimension is 168 mm; a 5 mm brim on each side gives a 178 mm footprint. Check the slicer's purge line, skirt and any support expansion against the remaining bed margin. Print one large quadrant per plate.

For the hub, platter, supports, foundation, motor bracket and column sleeves, start with six walls, eight top/bottom layers and 35–45% infill. Add solid modifier regions around clamps and captive nuts. For covers and the service box, start with four walls and 20–25% infill. These are process starting points, not calculated structural ratings. Slicing and physical printing have not been performed for this revision.

## Fit coupon

Keep the corner notch at the lower-left when identifying features. The STL coordinates below are in millimetres. One, two and three small dots distinguish the bearing pockets.

| Feature | Location / options | Check |
| --- | --- | --- |
| Bearing slip pockets | Centres (25,25), (70,25), (115,25); Ø35.2 / 35.3 / 35.4, 4 mm deep | Try the actual Ø35 bearing; choose a removable slip fit without forcing or wobble |
| Screw holes | X35 / 60 / 85 / 110, Y48; Ø3.4 / 4.5 / 5.5 / 6.6 | Actual M3 / M4 / M5 / M6 screws pass freely |
| M5 nut pockets | X15 / 40 / 65, Y58; 8.2 / 8.4 / 8.6 across flats | Nut seats without splitting the wall and cannot turn under light tightening |
| Insert pilots | X90 / 110 / 130, Y58; Ø4.0 / 4.2 / 4.4 | Nominal RX-M3x5.7 pilot is Ø4.0; choose from actual insertion/pull-out tests, not nominal hole size alone |

Measure after the part cools. The baseline `rt_fit = 0.30 mm` is a **diametral** allowance, not 0.30 mm per side. Change the named fit parameters and regenerate/recheck the model if the coupon demands it. Reaming a small number of holes is preferable to scaling an entire part. Repeat after changing filament, nozzle or process settings.

## Orientation and supports

| Parts | Supplied orientation | Slicer attention |
| --- | --- | --- |
| P11–P14, P53 | Tube/foot axis vertical | Brim if needed; no support inside bores |
| P20 | Flat sled underside down | Captive-nut mouths must remain accessible |
| P21 left/right | Bearing pocket opens upward | Keep the bearing seat free of support scars |
| P22 left/right | Retainer flange flat | Verify screw and shaft bores |
| P23 | Flat underside down | Revised flat platform; insert its captive nuts before attaching the continuous metal sole |
| P24 | L-shaped side down | Local support/cleanup at motor pilot if needed |
| P25 | Side down | Small sensor-bore wall: inspect first article before mounting sensor |
| P30 | Flange face down, neck upward | Review neck-bore counterbores and nut-pocket bridging; use local support only where needed |
| P31–P34 | Flat work surface down, ribs/skirt up | Clean the mating seams and fixture holes |
| P41–P44 | Floor down | Support the outside gutter underside; remove completely from drain outlets |
| P45 | Broad flat face down | Keep bolt holes clear |
| P46 | Roof down | Inspect screw columns and cable-gland apertures |
| P50 | Box upright | Support under the inward top rim; remove through the service opening without damaging gasket groove |
| P51, P52 | Flat | Keep lid sealing face flat; avoid excessive first-layer squish |

Orientations reduce support demand; they are not a claim that every part is support-free. Review layer previews at all pockets, transitions and horizontal holes. Do not auto-orient away from the supplied functional face without checking the consequences.

## Assembly sequence

1. **Prepare hardware.** Confirm the bearing bolt pattern and motor/coupling drawing; finish the shaft/key/preload stack and wheel attachment drawing. Machine M01/M02 flat, with parallel bearing datums. Cut all four steel columns to matched lengths with square ends. Clean swarf before assembly.
2. **Prepare the core and concealed fasteners.** Fit the underside M5 × 12 sole screws before anchoring M01. Insert the plain captive nuts into the sled, motor foundation and hub before mating parts close the pockets. Tighten the two covered core bench bolts through P20’s Ø25 openings before fitting the bearing blocks. Install and tighten the recessed M5 × 65 bearing-block bolts on P20 **before** M02 covers their tool path. Cartridge adjustment screws now sit at Y18/92, clear of the supports. Fit the drive cartridge to M01, then the four steel tubes/sleeves and M02. Sleeves are 0.5 mm shorter than the tubes. F01 uses small OD11 washers to clear the bearing; larger washers collide. Anchor through the four metal bench spacers.
3. **Build the output.** Attach bearing rings to their respective seat/hub without bridging them. Insert the four steel neck sleeves, pilot the metal wheel concentrically, and fit the four wheel attachment screws. Verify screw ends cannot hit the rotating/stationary neighbour. Check free rotation before the worm is fitted.
4. **Build the drive.** Assemble the worm shaft and opposed angular-contact bearings with the approved metal preload/retention stack. The supports are already fixed to P20 from step 2; fit retainers and check preload without using the printed caps to set it. Position the worm at 55.5 mm centre distance; use the ±3 mm axial slots to set duplex backlash. Follow the KHK marking and lubrication instructions. Turn through 360° by hand while checking tight spots.
5. **Fit the motor support and motor.** Seat M40 flat on the bench. Fit its two recessed M5 core-attachment screws from below before bench mounting; the heads must be flush or recessed. Insert captive nuts into P23, fit the two steel anchor sleeves, and place the platform directly on the metal sole. Anchor through the M6 washers/sleeves into the bench. Seal the static metal/printed perimeter and anchor penetrations with compatible sealant/sealing washers; do not seal over the removable captive nuts. Bolt the NEMA17 to P24, align the coupling and retain its shaft engagement. The nominal shaft-end gap is 7 mm, reducing to 4 mm at the positive adjustment limit; verify against the selected coupling. Provide cable restraint and the reserved 20 mm rear cable bend.
6. **Close the housing.** Fit the four fixed quarters, backing strips and drain outlets. Seal their static seams. Fit the motor hood gasket against its hard stops and seal the curved transition. Fit platter sections to the hub, seal the quadrant seams and unused fixture holes, and check all around the 2 mm running gaps. Housing seams must not bulge into the moving skirt.
7. **Fit the electronics enclosure.** Anchor the box on four feet. Fit the spreader gasket and metal compression stops, clamp the spreader with sealed penetrations, and attach the selected external heat sink. Mount the selected driver with proper thermal contact; complete its bracket pattern from the drawing. Fit controller standoffs to the slotted tray. Separate power/signal wiring as required by the selected drive, add strain relief, fit glands and blank unused entries. Keep all mains outside this box.
8. **Seal and check.** Install the continuous lid gasket without stretching or gaps. Tighten evenly to the designed hard land, without crushing PETG. First perform unpowered splash/dust checks with absorbent indicators. Then commission unloaded at low speed, followed by gradual load, temperature and bidirectional accuracy tests from the specification.

Mount the arm on M50 above the controller enclosure, with its base facing the platter. Two welded steel side channels and a front X brace carry M50 to the bench; keep the printed lid unloaded. Weld the frame, finish its top datum flat and parallel to the feet, protect against corrosion, then fit M50 with four M6 × 25 bolts. Anchor the bottom flanges with separate through-bolts and the two steel backing strips below the bench. Use the [fastener register](rotary-table-fasteners.md) to select anchor length after measuring the bench. The plate has ten Ø8 mm tool-access holes aligned with the lid screws. Remove those screws, lift the lid 8 mm, then slide it rearward through the open back of the stand. Confirm cable routing does not obstruct withdrawal. Verify the full arm/spindle motion envelope before coordinated use; the displayed folded pose is not a workspace study.

## Regeneration

From the repository root:

```sh
python3 scripts/build_rotary_table.py
python3 scripts/build_fastener_register.py
python3 scripts/build_assembly_checks.py
/Applications/SolidCraft.app/Contents/MacOS/solidcraft-cli run cad/rotary-table-build.json --save /tmp/rt01.sc --json-out /tmp/rt01-measure.json --quiet
python3 scripts/build_fit_coupon.py
/Applications/SolidCraft.app/Contents/MacOS/solidcraft-cli run cad/fit-coupon-build.json --save exports/rotary-table/fit-coupon.sc --out exports/rotary-table/fit-coupon.stl --quality fine --quiet
python3 scripts/export_rotary_table.py --in /tmp/rt01.sc
```

The build script creates a **standalone table**. It does not import or reposition the arm. The main `michelaingelo.sc` contains the table and the arm mounted on its metal bridge. The arm geometry is preserved; its placement is changed. Do not replace that main file with the standalone build if you want to keep the reference. The sidecar `cad/mount-so100.json` records the one-time rigid placement and bridge joint for the original imported arm; do not replay it on an already-mounted assembly. The coupon has its own generator, `scripts/build_fit_coupon.py`, and standalone native file.

The exporter uses SolidCraft's fine tessellation, applies proper rotations (no mirroring), translates each print onto the bed, then checks manifold edges, winding, mesh volume against CAD, and footprint. It does not run a slicer or predict strength.

The stand backing strip is a separate metal part: run `cad/stand-backing-strip.json` to regenerate its STEP and make two. Its manufacturing origin does not represent an assumed workbench thickness. New metal holes and threads must be deburred; inspect the arm foot before ordering F24 and drilling its adapter. The coupon does not validate bolt preload or structural stiffness.
