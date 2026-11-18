# RT-01 printing and assembly — revision 5

Use the [specification](specs/rotary-table.md), [BOM](rotary-table-bom.md) and [fastener register](rotary-table-fasteners.md). The exports are prototype geometry. CAD clearance does not certify cutting precision, payload, water resistance or real print fits.

## Files and printer setup

- `exports/rotary-table/stl/`: **25** assembly STLs, millimetres, oriented and placed on Z0. Do not use retired P20/P21/P22/P23/P25/P30 files from older packages.
- `fit-coupon.stl`: **150×100×24** coupon; feature map in [cad/fit-coupon-features.json](../cad/fit-coupon-features.json).
- [P54 removable drain catch](../exports/rotary-table/drain-catch/p54-removable-drain-catch.stl): print four copies, one per outlet.
- `print-manifest.json`: dimensions, brim footprint, bed-contact area, mesh/CAD volume checks and hashes.
- `metal/`:17 custom metal body STEPs plus one backing-strip drawing (make two). These require the separate machining/fabrication requirements.
- `rt01-assembly.step`:81 table/support/reference bodies; excludes arm. Cyan spaces are reservations, not physical parts.
- `seal-profiles.step`: compressed thicknesses; cut uncompressed gasket stock from the BOM.

A1 Mini baseline is dry yellow PETG with a 0.4 mm nozzle and 0.20 mm layers. Assign yellow PETG in Bambu Studio for the 25 assembly STLs, the fit coupon and the four drain catches. Start from the filament profile and calibrate flow, first layer and elephant foot. The largest dimension is 168 mm. With a 5 mm brim on each side it occupies 178 mm on the 180 mm bed. Inspect purge lines, support expansion and placement in the slicer. Print one large quadrant per plate. Slicing and physical printing are pending.

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
5. **Build worm shaft.** Assemble the approved shaft, key and inner-ring retention stack. Fit M61 caps and M62 shims and verify outer-ring contact. Set the duplex mesh per KHK's markings and instructions, then tighten the front F07 screws using the [worm adjustment tool procedure](#worm-adjustment-tool). For the [foam-trial pair](specs/rotary-table.md#foam-trial-drive-alternative), use axial movement to centre the tooth face and measure backlash directly. Mark the carrier position and check running torque through 360° after tightening. Follow the selected pair's lubrication instructions.
6. **Fit motor and sensor.** Anchor integral M40 directly through metal; no P23 or anchor sleeves. Bolt P24 and motor with confirmed engagement, align coupling and retain shaft insertion over±3 cartridge travel. Fit the axial sensor through M02 with both nuts; set 1.2 mm gap to the retained steel target, verify cable route and one event per revolution under actual variation. Use a PNP-compatible input.
7. **Close covers.** Fit the housing and seam strips. Apply a continuous, replaceable compatible RTV barrier through the platter seams and seal unused fixture holes and recesses. Keep the swept gaps clear of squeeze-out. Fit the hood gasket against the metal stops and seal the curved joint. Place one [removable catch](#drain-catches) below each drain. Verify the fixture's 8–9 mm screw engagement and its full rotation sweep.
8. **Build stand and electronics.** Install both M55 strips with the scallops inward toward the electronics bolts. Fit all four [P55 arm seats](#prototype-arm-seats) before clamping the arm. F24 threads into M50 from above with at least 1 mm tip recess. For each F21, slide the seal and metal washer through the inward slot, drop in the captive nut and tighten the reversed bolt from below. The uncompressed seal and washer have 0.20 mm nominal loading allowance. Trial assembly and retention on the coupon first. Fit and seal the spreader, heat sink, driver, controller and cable hardware after anchoring the box.
9. **Commission.** First unpowered ingress and hand-rotation checks. Then unloaded low speed, followed by progressive load/stopping, reversal/TIR/deflection, sensor, temperature and dust/splash tests. Do not infer a carving rating from the animation.

Load F21 seals and washers before the nuts, with the tray and electronics removed. Enter through the opening above the tray posts, shift toward the anchor rows below the rim, and lower the washer stack beside the posts. Slide it outward into the slot and lower the nut into the trap. Inspect the seal imprint and nut retention on the real print before enclosing it.

Use the common flat bench plane in CAD for the layout. The **30 mm top** in the fastener register is an example. Before ordering through-bolts, use the actual thickness T and the hole-by-hole formulas. Both M55 backing strips need full contact and clear space under the bench. [Bench anchor formulas](rotary-table-fasteners.md#bench-anchors)

## Service with the arm installed

Power off, disconnect and label device leads, then release the brackets and driver thermal interface. Remove ten lid screws through the Ø8 plate access holes. Lift the lid and gasket 8 mm and slide them rearward 140 mm. Follow the [F19 tool procedure](#tray-screws-f19) to release and retrieve all four tray screws. Lift the tray and controller 27 mm and slide them rearward 140 mm. Lift the driver 70.5 mm to Z106.5–141.5 and move it rearward 140 mm. The raised envelope has 2.5 mm nominal clearance above the rim and below M50. The initial lift passes the tray posts with 1 mm nominal clearance per side. Prove the route with the selected device, connectors, tools and thermal interface in place before accepting service access.

For motor service, remove all four F17 screws, free the curved RTV joint and disconnect or release the gland cables. Slide the hood 70 mm along +X before lifting it. Use a replacement B25 gasket when the old seal is dragged, torn or compressed out of shape. Inspect the four screw-post seats and verify a new seal after reassembly.

### Tray screws (F19)

Use the four specified **M3 × 10 captive-washer assemblies**. Each washer can float up to 0.25 mm, then the rolled-thread stop carries it with the screw. Before installing the tray, check that the washers turn freely and remain captured on the screws. [F19 screw drawing requirements](rotary-table-fasteners.md#stack-location-and-assembly-access)

1. Park the disconnected leads clear of both rear paths with the lid and gasket off. The checked AF2 lever has a stem within Ø2.31 × 22 mm, a hub within Ø8 mm and a 65 mm lever with an 8 × 8 mm section. Enter from Y−306 with the tip at Z106.5 and the lever pointing rearward. Lower it into the socket. Loosen counterclockwise from rearward to inward at X−65 and from inward to rearward at X+65. Lift 2.5 mm out of the socket before resetting the lever. Follow the screw up to about 7 mm above its seated height, until all threads release.
2. Lift the driver 2.5 mm out of the socket, clock it rearward while low, then raise the tip to Z106.5 and withdraw it. The free screw can settle at the insert mouth. The checked tip range there is Z78.5–79.5. Insert a rear-operated mechanical gripper with an open and closed upright envelope within Ø8. Its rear bridge reaches 145 mm from the screw axis, fits within an 8 × 4 mm section and starts 17.5 mm above the head underside. Grip the lower head wall with the lower jaw edge at least 0.10 mm above the head underside. Trial the selected jaws for grip and clean release before using them over the electronics.
3. Lift the screw and captive washer until the screw tip reaches Z106.5, then withdraw them straight rearward. Remove all four assemblies and set them outside the tray path. Lift the tray 27 mm and withdraw it rearward. Return the tray and controller to their original posts before refitting.
4. Bring each assembly back above its hole in reverse removal order. Lower until the screw meets the insert mouth, release the jaws, then raise and withdraw the empty gripper. Use the AF2 lever to start the thread lightly and tighten clockwise through the same 60° sector. Keep the washer flat under the head and apply the clamp load qualified on the tray insert. Confirm removal and refitting at all four sites on the fitted assembly with the actual tools and leads. **Physical trial pending.** [Tool dimensions and clearances](../cad/hardware-check-coverage.json)

### Arm mounting screws (F24)

Isolate power and support the arm in the saved folded pose before using this route. The checked AF3 tool has a shaft within Ø3.47 × 25 mm from the engaged tip, an Ø8 mm bend or hub and an outboard 65 mm handle within an 8 × 5 mm section. Approach from the corresponding side at X−90 or X+90 with the tip clear of the screw. Rotate to the start angle while raised. Drop into the socket, tighten clockwise, lift 3 mm before resetting and return to the outboard orientation before withdrawing. The nominal check uses a head seat at Z168.8. Recheck the route and actual engagement after fitting the four matched seats.

Angles are measured counterclockwise from +X, viewed from above. The front row is closest to the table. [Tool envelope and hole coordinates](../cad/hardware-check-coverage.json)

| Site | Clockwise tightening stroke |
| --- | --- |
| X+ front | 60° to 0° |
| X+ rear | 0° to −60° |
| X− front | 180° to 120° |
| X− rear | 240° to 180° |

### Prototype arm seats

Print one [front right](../exports/rotary-table/arm-seats/p55-front-right.stl), [rear right](../exports/rotary-table/arm-seats/p55-rear-right.stl), [front left](../exports/rotary-table/arm-seats/p55-front-left.stl) and [rear left](../exports/rotary-table/arm-seats/p55-rear-left.stl) P55 seat in yellow PETG. The STL orientation places the flat washer land on the bed. Start with a 0.4 mm nozzle, 0.10 mm layers including the first layer, four walls, 100% concentric infill and no supports. Use a 3 mm outer brim. The minimum thickness beneath the washer land is about 0.44 mm at the front seats and 0.78 mm at the rear. Keep the seats labelled by side and row through printing and fitting. The front row faces the table and the right seats go on the +X side. [Print manifest](../exports/rotary-table/arm-seats/p55-seat-manifest.json) · [Editable seats](../exports/rotary-table/arm-seats/p55-fitted-seats.sc)

Dry-fit each contour against the foot with the flat land beneath the Ø9 metal washer. Use a contact mark to find high spots, then lightly sand only those spots on the contoured PETG seat. Keep the washer land flat and preserve the arm's support on the 8 mm M50 plate at Z152. Each washer should sit flat and each saddle should bear stably without rocking. Recheck grip after fitting, cut and deburr each screw as needed, and check the tip stays recessed. Recheck contact and clamp retention after dwell and after the spindle-off stop trial.

### Worm adjustment tool

Isolate power, free the hood glands and curved seam, and remove the motor hood, fixed housing quadrants and seam backing strips. Keep the hub, wheel, bearing and columns installed. Secure the harness clear of the tool route. Fit a compact AF4 key within the checked envelope. It uses a Ø5 mm shaft envelope and a 5 × 5 mm handle section reaching 65 mm from the stem, with **12 mm from the engaged tip to the top of the handle**. Match the real bend and verify that the tool can apply the required clamp torque.

Approach horizontally from −Y with the handle pointing −Y and the tip raised 5 mm above its fully engaged position. The probe moves the stem from Y−62 to Y18. Looking down, turn the tool at X−52 60° counterclockwise while raised, engage it and tighten clockwise toward −Y. At X+52, engage with the handle pointing −Y and tighten clockwise 60° toward the centre. Lift the key 5 mm clear before resetting for the next stroke. After the last stroke, return to the −Y orientation while lifted and pull the key out along the entry route. The two screw paths have 0.50 mm minimum sampled clearance at carrier X = −3, 0 and +3. Verify the actual key and demonstrate two successive tightening strokes to the required clamp torque on each screw.

## Drain catches

Print four P54 catches upright with the open side up. Each catch is nominally **70 × 40 × 24 mm**. Place them on the flat bench beneath the four Ø5 drain axes at R161 and 45°, 135°, 225° and 315°. Centre the raised inlet under the bore and face the pour notch away from the table. The bore's nominal projection clears the inlet's inward wall by 0.50 mm, so check centring with the first-article tracer before marking the positions on the bench. Leave room to slide each cup radially outward. [P54 print file](../exports/rotary-table/drain-catch/p54-removable-drain-catch.stl)

Empty each cup before the **20 mL** nominal mark. The calculated capacity is **19.87 mL at the mark** and **26.30 mL at the pour notch**. Stop the machine, slide the cup 20 mm outward and lift 30 mm. Pour away from the machine and clean the open channel and sump. The printed gutter has a local **0.50 mm radial lip** at each bore. Inspect it in the layer preview and on a first article before using a cleaning tool.

Use an unpowered tracer to centre all four cups and check collection, splash, pooling and leakage. Mark each cup's footprint on the bench. During the same trial, empty each cup and return it to its marks. Repeat the tracer at all four outlets and confirm every stream enters the opening. A 1 mm outward shift can put part of the discharge over the inlet rim. [Installed placement](audit-evidence/2026-11-18-rt01/service-follow-up/drain-catch-placement.png) · [Corrected capacities](audit-evidence/2026-11-18-rt01/service-follow-up/drain-catch-summary.json)

## Prototype foam fixture

Print one [P56 base](../exports/rotary-table/foam-fixture/p56-foam-fixture-base.stl), two [P57 jaws](../exports/rotary-table/foam-fixture/p57-sliding-jaw.stl) and one [P58 keeper](../exports/rotary-table/foam-fixture/p58-top-keeper.stl) in yellow PETG. The supplied orientations sliced on two A1 Mini plates with the 0.4 mm nozzle, 0.20 mm layers, six walls, eight top and bottom layers and 40% infill. Inspect the underside grooves and nut-loading openings in the layer preview and on the first print. The four P55 seats sliced on a separate plate. [A1 Mini slicing results](audit-evidence/2026-11-18-rt01/prototype-fit/a1-mini-slice.results.json)

Use the hardware listed in the [BOM](rotary-table-bom.md#bought-hardware-for-the-first-foam-fixture). Assemble the sliding jaws with their retainers and nuts. Route two 4.8 mm cable ties through the matching base slots and underside grooves, one tie per side, before attaching the base to the platter. Seat the base with four M6 × 20 screws and 1.6 mm washers. The 3.0 mm fixture plate gives 8.4 mm nominal thread engagement. With the 2 mm EVA bottom pad fitted, support the 50 × 50 × 40 mm foam block against the padded fixed datums. Snug both adjusters and lock the sliding jaws with the M3 retainers. Attach the pads to the fixture and inspect contact without crushing the foam. [Editable assembly](../exports/rotary-table/foam-fixture/foam-fixture-prototype.sc) · [Installed layout](audit-evidence/2026-11-18-rt01/service-follow-up/foam-fixture-placement.png)

Fit the EVA-lined keeper over the blank. Bring each tie up its side, bend it around the outside edge and over the keeper rail, then tighten and trim the tails outside the working opening. The keeper supplies vertical restraint independently of jaw friction. Use the central **30 × 30 × 20 mm** window at the top of the foam for the first path. Keep the tool and cables clear of jaws, keeper, screws and ties. Check clamp retention and hand-turn the loaded fixture through a full revolution. Then dry-run the intended arm path with the spindle off. Replace ties after removing the blank. This fixture clamps through the printed deck and requires a fit and creep check at the trial loads.

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
python3 scripts/build_drain_catch.py --model /tmp/rt01-review.sc
/Applications/SolidCraft.app/Contents/MacOS/solidcraft-cli run cad/stand-backing-strip.json --quiet
/Applications/SolidCraft.app/Contents/MacOS/solidcraft-cli run cad/fastener-clearance-checks.json --in /tmp/rt01-review.sc --results --quiet
/Applications/SolidCraft.app/Contents/MacOS/solidcraft-cli run cad/support-access-checks.json --in /tmp/rt01-review.sc --results --quiet
```

The rebuild script replaces only RT01 components/parameters, preserves the arm and places it at the recorded absolute transform. Do not replay the one-time `cad/mount-so100.json` migration on an already mounted arm. The standalone `cad/rotary-table-build.json` intentionally contains no arm. Verify candidates and exports before replacing the main native file. Do not add `--save` to disposable collision/service probes.

The exporter removes obsolete STLs recorded by the previous manifest, applies proper rotations and Z0 placement, checks paired edges/winding/volume/brim footprint and verifies all four P45 strips are flat. The separate `cad/stand-backing-strip.json` regenerates one metal drawing; make two. See the [validation report](rotary-table-validation.md) for current evidence and remaining gates.
