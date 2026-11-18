# RT-01 printing and assembly — revision 5

Use the [specification](specs/rotary-table.md), [BOM](rotary-table-bom.md) and [fastener register](rotary-table-fasteners.md). The exports are prototype geometry. CAD clearance does not certify cutting precision, payload, water resistance or real print fits.

## Files and printer setup

- `exports/rotary-table/stl/`: **25** assembly STLs, millimetres, oriented and placed on Z0. Do not use retired P20/P21/P22/P23/P25/P30 files from older packages.
- `fit-coupon.stl`: **150×100×24** coupon; feature map in [cad/fit-coupon-features.json](../cad/fit-coupon-features.json).
- `print-manifest.json`: dimensions, brim footprint, bed-contact area, mesh/CAD volume checks and hashes.
- `metal/`:17 custom metal body STEPs plus one backing-strip drawing (make two). These require the separate machining/fabrication requirements.
- `rt01-assembly.step`:81 table/support/reference bodies; excludes arm. Cyan spaces are reservations, not physical parts.
- `seal-profiles.step`: compressed thicknesses; cut uncompressed gasket stock from the BOM.

A1 Mini baseline is dry PETG with a 0.4 mm nozzle and 0.20 mm layers. Start from the filament profile and calibrate flow, first layer and elephant foot. The largest dimension is 168 mm. With a 5 mm brim on each side it occupies 178 mm on the 180 mm bed. Inspect purge lines, support expansion and placement in the slicer. Print one large quadrant per plate. Slicing and physical printing are pending.

For platter, motor bracket and column sleeves, start with six walls,eight top/bottom layers, 35–45% infill and solid regions around clamps. Covers/service box:four walls, 20–25%. These are starting profiles, not strength qualifications. Keep supports/brim residue off functional lands. Metal components are not printable substitutes.

## Coupon and correction route

View from above with the notch at lower left (X0/Y0). Let it cool before measuring. Nominal clearances are diametral, not per-side. Do not uniformly scale parts; correct the parameter, regenerate and recheck. For nonstructural clearance holes, controlled drilling/reaming is an alternative after measuring wall thickness. Repeat calibration after changing material/nozzle/process.

| Coupon feature | Centres/options, mm | Production correction |
| --- | --- | --- |
| Vertical screw holes | Y15; X15/35/55/75:Ø3.4/4.5/5.5/6.6 | `rt_m3`, `rt_m4`, `rt_m5`, `rt_m6`; trial actual bolts, enlarge parameter or drill if needed |
| Horizontal screw trials | Y75–95,Z15; X15/30/45:Ø3.4/3.5/3.6; X60/75/90:Ø4.5/4.6/4.7; X105/120/135:Ø5.5/5.6/5.7 | `rt_m3_h`, `rt_m4_h`, `rt_m5_h`; calibrate separately from upright holes |
| Insert pilots | Y15; X100/120/140:Ø4.0/4.2/4.4, 7 deep | `rt_insert`; actual RX-M3x5.7 insertion and pull-out/clamp test |
| Column bores | Y42; X15/35/55:Ø10.2/10.3/10.4, 8 long | `rt_column_bore`; confirm with full 69.5 mm P11 bore |
| Fixture-boss pockets | Y42; X85/110/135:Ø16.1/16.3/16.5, 5.2 deep | `rt_fixture_boss_bore`; actualØ16 metal boss must clear without forcing |
| F21 captive nut and washer slot | X30/Y62, AF7.4, 2 mm side opening toward −X | Slide the actual seal and washer into the slot, drop the AF7 nut into the trap and trial a sealed low-preload clamp. Adjust `rt_anchor_nut_af` from the result. |

Machine and inspect the bearing seats, hub pilots and carrier guide to the specified metal fits. The coupon covers the current printed interfaces.

Required first articles before the full print set:

1. One complete P11 for the long bore, length and at least 0.3 mm actual axial clamp relief (nominal 0.5). If relief fails, adjust sleeve length in the generator or face the printed sleeve; do not shorten matched steel columns.
2. P24 for the horizontal 22.6 pilot (`rt_motor_pilot_h`), M3 motor holes, M5 foot holes and sustained bolt clamp retention. Its supplied rotation makes the assembly-vertical foot holes horizontal during printing.
3. One platter quadrant on M20: boss pocket diameter/depth, fixture passage, deck seating, fastener-head recess and seam. Pocket depth must leave no contact on the boss top while the deck underside seats atZ116; the nominal gap is 0.2. If print error consumes it, revise pocket depth in the generator and repeat the section check.
4. P50/P52 with actual inserts and gasket: flat sealing land, flush insert depth, compression to 1.5, leakage and repeated service. Groove/land changes require explicit source edits and a regenerated seal profile; screw-hole calibration does not validate sealing.

The current parameters were exercised together with larger hole/boss/insert values in a disposable model. That demonstrates they drive the intended geometry; it does not determine the correct settings for your printer.

## Supplied orientation

| Parts | Bed orientation / attention |
| --- | --- |
| P11–P14,P53 | Axis vertical; no support inside bores |
| P24 | L-shaped side down; motor bore/pilot horizontal, inspect support removal |
| P31–P34 | Work face down, ribs/skirt up; clean seams and underside boss pockets |
| P41–P44 | Floor down; local support under gutter, keep drains clear; seam holes horizontal |
| P45 all four | Broad face down, 24×84 footprint, 8 high; holes vertical in the print |
| P46 | Roof down; inspect long screw columns and gland apertures |
| P50 | Upright; support under inward rim. Inspect the F21 loading slots for bridge sag and clear supports from the access passages, nut traps and gasket groove. |
| P51,P52 | Flat; protect lid sealing land from first-layer distortion |

Orientations reduce support demand; they do not make every feature support-free. Review layer previews at pockets, bridges and horizontal holes. Export checks catch strip orientation, topology and envelope errors, not layer adhesion or physical fit.

## Assembly order

1. **Finish drawings and inspect metal.** Select actual bearings/motor/coupling; approve shaft keys, shoulders, retention/preload, wheel secondary machining and drive-pin strength. Machine/inspect M01/M02/M20/M60/caps/columns using the specification. Match cap shims to measured outer rings. Protect precision fits from coatings, swarf and slurry.
2. **Install concealed base hardware.** Fit the F13 countersunk screws joining M40 to M01. Tighten all four F02 core anchors through the metal spacers before fitting M60. The Ø25 recesses in M60 leave 1.4 mm over the screw heads; the blocks cover the key paths. For retorque, unload the table and open the drive, then remove the carrier and any obstructing shaft, rotor or bearing-seat stack. Recheck guide alignment and backlash after refitting. Use OD11 F01 washers beside the bearing.
3. **Fit cartridge and columns.** Seat M60 on its metal guide, install F07 loosely for axial adjustment. There are no F08 block bolts. Fit matched 72 mm locating columns and shorter printed sleeves, then M02 onto the round/slot datums. Check metal-only column clamp path and assembled worm/bearing alignment.
4. **Build rotor.** Fit the bearing rings to their designated seat/hub without bridging them; pilot M20 into the inner ring. Press M21 into M20 with a controlled fixture, align the wheel radial slot/pilot and clamp F05. Fit the mild-steel target with recessed F25 before access is obstructed. Inspect pilot/tooth runout and free rotation. Platter screws are now M5×16 into metal, not the old 25 mm nut stack.
5. **Build worm shaft.** Assemble the approved shaft/key/inner-ring retention stack. Fit M61 caps and M62 shims and verify outer-ring contact. Set duplex backlash with the housing open. Approach the front F07 screws from the side with a short-leg 4 mm hex key. The probe used a 5 mm-wide handle reaching 65 mm, with 15 mm from the engaged tip to the top of the handle. Swing toward the centre and withdraw in the straight orientation. Verify the actual key with the hub, bearing and selected harness in place. Tighten F07, mark the carrier position and check torque through 360°. Follow KHK markings and lubrication instructions.
6. **Fit motor and sensor.** Anchor integral M40 directly through metal; no P23 or anchor sleeves. Bolt P24 and motor with confirmed engagement, align coupling and retain shaft insertion over±3 cartridge travel. Fit the axial sensor through M02 with both nuts; set 1.2 mm gap to the retained steel target, verify cable route and one event per revolution under actual variation. Use a PNP-compatible input.
7. **Close covers.** Fit the housing and seam strips. Apply a continuous, replaceable compatible RTV barrier through the platter seams and seal unused fixture holes and recesses. Keep the swept gaps clear of squeeze-out. Fit the hood gasket against the metal stops and seal the curved joint. Direct the four drains through the floor notches into a cleanable external catch. Verify the fixture's 8–9 mm screw engagement and its full rotation sweep.
8. **Build stand and electronics.** Install both M55 strips with the scallops inward toward the electronics bolts. Measure and fit all four F24 bearing seats before clamping the arm. F24 threads into M50 from above with at least 1 mm tip recess. For each F21, slide the seal and metal washer through the inward slot, drop in the captive nut and tighten the reversed bolt from below. The uncompressed seal and washer have 0.20 mm nominal loading allowance. Trial assembly and retention on the coupon first. Fit and seal the spreader, heat sink, driver, controller and cable hardware after anchoring the box.
9. **Commission.** First unpowered ingress and hand-rotation checks. Then unloaded low speed, followed by progressive load/stopping, reversal/TIR/deflection, sensor, temperature and dust/splash tests. Do not infer a carving rating from the animation.

Load F21 seals and washers before the nuts, with the tray and electronics removed. Enter through the opening above the tray posts, shift toward the anchor rows below the rim, and lower the washer stack beside the posts. Slide it outward into the slot and lower the nut into the trap. Inspect the seal imprint and nut retention on the real print before enclosing it.

Bench anchor lengths depend on measured T; use the register formulas. Do not use a loose wood block as a precision foundation. A rigid stand does not change the purchased arm's controller behavior.

## Service with the arm installed

Power off, disconnect and label device leads, then release the brackets and driver thermal interface. Remove ten lid screws through the Ø8 plate access holes. Lift lid/gasket 8 mm and slide rearward 140 mm. Release the tray screws, lift tray/controller 27 mm and slide rearward 140 mm. Lift the driver 70.5 mm to Z106.5–141.5 and move it rearward 140 mm. The raised envelope has 2.5 mm nominal clearance above the rim and below M50. The initial lift passes the tray posts with 1 mm nominal clearance per side. Prove the route with the selected device, connectors, tools and thermal interface in place before accepting service access.

For motor service, remove all four F17 screws, free the curved RTV joint and disconnect or release the gland cables. Slide the hood 70 mm along +X before lifting it. Use a replacement B25 gasket when the old seal is dragged, torn or compressed out of shape. Inspect the four screw-post seats and verify a new seal after reassembly.

## Regeneration and checks

From the repository root, generate a separate candidate to preserve the mounted arm:

```sh
python3 scripts/build_rotary_table.py
python3 scripts/build_fastener_register.py
python3 scripts/build_assembly_checks.py
python3 scripts/build_fit_coupon.py
python3 scripts/rebuild_assembly.py --in michelaingelo.sc --out /tmp/rt01-review.sc
/Applications/SolidCraft.app/Contents/MacOS/solidcraft-cli run cad/fit-coupon-build.json --save exports/rotary-table/fit-coupon.sc --out exports/rotary-table/fit-coupon.stl --quality fine --quiet
python3 scripts/export_rotary_table.py --in /tmp/rt01-review.sc
/Applications/SolidCraft.app/Contents/MacOS/solidcraft-cli run cad/stand-backing-strip.json --quiet
/Applications/SolidCraft.app/Contents/MacOS/solidcraft-cli run cad/fastener-clearance-checks.json --in /tmp/rt01-review.sc --results --quiet
/Applications/SolidCraft.app/Contents/MacOS/solidcraft-cli run cad/support-access-checks.json --in /tmp/rt01-review.sc --results --quiet
```

The rebuild script replaces only RT01 components/parameters, preserves the arm and places it at the recorded absolute transform. Do not replay the one-time `cad/mount-so100.json` migration on an already mounted arm. The standalone `cad/rotary-table-build.json` intentionally contains no arm. Verify candidates and exports before replacing the main native file. Do not add `--save` to disposable collision/service probes.

The exporter removes obsolete STLs recorded by the previous manifest, applies proper rotations and Z0 placement, checks paired edges/winding/volume/brim footprint and verifies all four P45 strips are flat. The separate `cad/stand-backing-strip.json` regenerates one metal drawing; make two. See the [validation report](rotary-table-validation.md) for current evidence and remaining gates.
