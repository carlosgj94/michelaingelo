# Rotary table specification — RT-01

Status: revision 3 prototype; not fabrication released. Hardware quantities and defined stack-ups are in [the fastener register](../rotary-table-fasteners.md). The design baseline was written before the CAD rebuild on 2026-11-17 and the dimensions below were reconciled with the finished model. The requirements below are engineering targets, not measured performance. Geometry and print checks are recorded separately in `docs/rotary-table-validation.md`.


## Revision 3 — braced arm stand and assembly fasteners

Recorded before the CAD changes on 2026-11-17. The arm has **not** been tested on this assembly: the concern is the purchased arm's abrupt motion and the resulting reaction loads, not an observed failure of this stand.

- Retain the arm mounting face at Z144 and the service box underneath. Replace the four tall round posts with two **welded 4 mm steel side channels**, 116 mm deep and 136 mm high, with 28 mm top/bottom flanges, and a **4 mm front X brace**. The rear stays open for removing the lid and accessing cables. These are metal fabrication parts, not A1 Mini prints. Weld dimensions/process and load capacity require review against the actual arm/tool loads; the CAD is a fabrication concept, not a rated stand.
- Keep the 228 × 116 × 8 mm aluminium arm plate. Attach it to the steel flanges using four M6 × 25 bolts at X±98, Y−272/−176. Use separate bench bolts through the bottom flanges, with two 40 × 136 × 3 mm steel backing strips below the bench. No arm load passes through the printed box or lid.
- Anchor the stand and rotary table to the **same rigid, braced workbench** using through-bolts. A loose wood block is not the design basis. Bench thickness is unknown: the fastener register must give a length formula, not invent a final anchor length. Backing strips are supplied as separate fabrication geometry because their assembly height depends on that thickness.
- Extend M01 to 164 × 184 × 8 mm (Y−82 to102) and P20 to 156 × 94 × 8 mm (Y6.5 to100.5). Move cartridge anchors to X±52/Y18 and X±70/Y92, outside the bearing supports, and add Ø25 access openings over the two covered core bench bolts. The original 164 mm square gasket still seals the floor opening.
- Audit every designed joint for screw diameter, length, head, washers, nuts/inserts, thread engagement and assembly access. Exclude screws inside the purchased arm; include its four base attachments. Explicitly list unfinished purchased-component interfaces rather than imply that the entire machine is order-ready.
- Correct the wheel-hub bolts to M5 × 45, recess the worm-block bolt heads, provide bolt-tip clearance in the base/motor sole, move the home bracket clear of the column bolt, and use flush heat-spreader clamp screws outside the thermal opening. Keep all sealing and tool-access provisions compatible with these changes.
- Check the stand, fastener envelopes, full table rotation and lid removal in CAD; regenerate affected print/manufacturing files and the hardware register. Physical stiffness, bolt preload, thermal behaviour and motion accuracy remain to be tested. A stiffer stand does not correct servo backlash or abrupt motion commands.

Revision 3 supersedes the four-post support and provisional fastener list in Revision 2 below.

## Revision 2 — motor support and arm above the controller box (superseded support)

Requested on 2026-11-17 after reviewing the motor-pod overhang. These decisions are recorded before changing the CAD:

- Replace the printed underlapping motor tab with a **continuous 172 × 82 × 4 mm aluminium sole plate**, on the bench at Z0. The printed motor platform rests on it at Z4. Two underside countersunk M5 screws join the sole to the main core; their centres move to X72, Y20/48, clear of the core gasket. Add two M6 bench anchors at X220, Y35/77, with 8 mm metal compression sleeves through the printed platform. This removes the unsupported overhang and gives the screw heads a defined recess.
- Fit the existing SO100 above the electronics box, facing +Y toward the platter. A **228 × 116 × 8 mm aluminium arm plate at Z136–144** is carried by four independent **Ø20 / Ø6.6 × 136 mm steel standoffs** at X±102, Y−272/−176. M6 through-bolts anchor the plate/standoffs directly to the bench. The electronics enclosure and its lid carry none of the arm load.
- Seat the arm's measured base underside at Z144, centred at X0/Y−224. Keep the imported arm geometry and joint pose intact; apply one rigid placement transform. Use the four existing nominal Ø5 mounting passages measured from the imported base, with M4 clearance in the metal plate; verify the owned revision and screw seating before drilling metal.
- Preserve **28 mm between the lid top (Z108) and arm-plate underside (Z136)**. Ten tool-access holes in the arm plate align with the lid fasteners. The lid lifts and withdraws rearward between the external standoffs without removing the arm. Keep gland access and the external heat sink unobstructed.
- Verify nominal contacts, new part/arm overlaps, lid withdrawal, fastener alignment, all printable envelopes, and fresh-build/export consistency. The mounted pose does not certify the arm's full workspace or loaded stiffness.

This revision supersedes the earlier instruction to keep the arm unmounted and separate. The original reference file remains archived.

## 1. Scope and decisions

Replace the old stationary 450 mm base with a single horizontal platter rotating around vertical Z (C axis). Mount the existing SO100 above the controller box on the independent metal braced stand described in Revision 3. The bridge, box and rotary table are each anchored to the bench. Arm internals, spindle and workpiece-clamp design are outside this revision.

The user approved a printed assembly with a metal core: two small aluminium datum plates, purchased bearings and metal gearing, printed platter sections, housings, mounts and electronics enclosure. The motor sole and arm adapter are aluminium; Revision 3 adds welded steel side channels and a front X brace. Additional stock metal hardware includes compression tubes, shafts, couplings, nuts and a controller heat spreader. Do not print bearing races, worm teeth or shafts for the precision version.

Use a 320 mm platter instead of the earlier 450 mm estimate. Four quadrant sections fit the A1 Mini without outsourcing a large print. Scaling means retaining this load path and replaceable drive cartridge, then resizing the bearing, gearing and structure; do not uniformly scale bought components, holes or print clearances.

## 2. Design envelope and acceptance targets

| Item | Baseline |
| --- | --- |
| Platter | 320 mm diameter, four sections, 12 mm deck with underside ribs |
| Rotating tabletop | Z = 116–128 mm; right-hand rotation about Z |
| Fixed enclosure | 308 mm main outside diameter; 328 mm including drainage gutter |
| Core base plate | 164 × 184 × 8 mm aluminium, X±82 / Y−82 to102, underside Z = 4 mm |
| Bearing seat | 156 mm OD × 8 mm aluminium ring, 94 mm central opening; Z = 82–90 mm |
| Bearing | RU85-size preloaded crossed-roller ring; nominal 55 × 120 × 15 mm, Z = 90–105 mm |
| Output support | Inner bearing ring carries a bolted output hub and four platter sections |
| Load | 5 kg maximum workpiece + fixture target, initially foam; rotating hardware added separately in sizing |
| Workpiece assumptions | Centre-of-mass offset ≤80 mm; cutting height ≤150 mm above the table |
| Cutting-force assumption | 10 N at up to 160 mm radius; foam commissioning only |
| Working speed | 0.1–2 rpm initially; controlled acceleration ≤0.2 rad/s² |
| Output torque | Design for ≥4 N·m continuous and ≥8 N·m short peak after measured friction; do not infer this from motor holding torque |
| Reversal error target | ≤0.10° at the platter (0.28 mm tangential error at R160); aspirational ≤0.05° after adjustment |
| Load deflection target | ≤0.20 mm measured at R140 under a 10 N tangential force; test in both directions |
| Runout target | ≤0.20 mm axial TIR at R140 after assembly and shimming |
| Maximum printed-part envelope | 168 × 168 × 168 mm in the specified orientation; normally ≤164 mm in X/Y |
| Environment | Fine dust and incidental splashes; no immersion, hose washing or certified IP rating |

The 5 kg payload at 80 mm eccentricity creates 3.92 N·m of overturning moment. A 10 N lateral cutting force at 150 mm adds 1.50 N·m. Use at least 10.84 N·m as the initial factored overturning design case (factor 2), plus the actual fixture geometry. Tangential cutting torque is 1.60 N·m before friction and acceleration. These are load cases, not a structural verification. Measure rotating inertia and drive friction before selecting final motor current, speed and acceleration.

## 3. Mechanical architecture

Load path: fixture → ribbed platter sections → output hub → bearing inner ring → bearing outer ring → aluminium seat → four steel compression tubes → aluminium base plate → bench bolts. Printed covers do not carry the workpiece. The printed hub and deck remain structural prototype parts and must pass the load tests; larger versions need a metal hub and platter.

Motion path: closed-loop NEMA17 motor → metal clamp coupling → supported steel worm shaft → duplex worm → metal worm wheel → bolted output hub → platter. The worm shaft has bearings on both sides of the mesh to react axial force in both directions. No belt and no assumption of worm self-locking.

Core coordinates are millimetres; Z0 is the bench. Four support columns are centred at (66,0), (-66,0), (36,-58), (-36,-58). Steel tubes are 10 mm OD, ≥6.2 mm ID, 70 mm long. Printed sleeves are 69.5 mm long, leaving 0.5 mm clearance so that metal carries the clamp load. The metal bearing seat rests on the tubes, not on soft printed layers. M6 through bolts clamp into tapped holes in the aluminium base.

The bearing outer-ring attachment reference is eight M5 positions on 105 mm PCD; the inner-ring reference is eight M5 positions on 65 mm PCD. Confirm the purchased RU85 variant's hole types, angular phase, preload grade, shoulder requirements and permitted bolt torque against its drawing. Bearing reference bodies show envelopes and interfaces, not internal rollers. Do not use printed clearance fits to establish bearing preload. Machine the datum faces flat and parallel; initial drawing targets are 0.03 mm bearing-seat flatness and 0.05 mm base flatness, subject to the bearing supplier's requirements.

The output hub has a 150 mm flange, a raised 76 mm bearing-contact boss and a neck passing through the bearing bore. Keep the flange 1 mm above the stationary outer ring. Attach the worm wheel to the neck with four M5 fasteners on a 30 mm PCD, using metal compression sleeves through the printed neck. The soft wheel hub requires a concentric pilot and tapped attachment holes; retain the manufacturer's tooth geometry. This secondary machining and the shaft drawing must be checked by the fabricator before ordering.

Each platter quadrant bolts to the hub at two positions. Four M6 fixture points on a 94 × 94 mm square pass through the deck into captive metal nuts in the hub. They are an attachment interface, not a complete workholding system. Seal unused holes; use bonded sealing washers or a gasketed fixture when wet.

## 4. Drive and controller provisions

Reference gear pair: **KHK KWGDL2-R1 + AGDL2-40R1**, module 2, right hand, single start, 40:1. Nominal centre distance 55.5 mm. Wheel pitch diameter 80 mm, maximum OD 86 mm, toothed face 18 mm, hub 15 mm, total height 33 mm. Worm OD 35 mm, toothed length 36 mm, hub length 14 mm, total length 50 mm. Worm axis: X, Y=55.5, Z=50. Wheel teeth span Z=41–59; hub spans Z=59–74. Reference tooth is placed at X0.

Model the purchased tooth bodies as labelled envelopes. They are not printable gears or a tooth-contact simulation. Specify the manufacturer's duplex pair together; ordinary worms of the same module are not substitutes. The worm's stock bore is 14 mm and the wheel's is 15 mm. The proposed shaft interface needs the worm finish-bored/keyed to 15 mm by the supplier or machinist. Final key, shaft shoulders, bearing retention, preload nuts and machining tolerances are procurement-release items.

Provide a replaceable worm cartridge and axial adjustment slots ±3 mm. Adjustment changes backlash, not centre distance. Measure running torque through a full revolution; do not preload to binding. KHK's maximum permitted shift is not a recommended assembly setting. Mount both arrow markings in the specified direction. Lubrication must follow the gear and bearing suppliers, with lubricant compatible with enclosure seals.

Two 7202-size angular-contact bearings (15 × 35 × 11 mm) are the space reference, arranged to react reversing thrust; use a matched/preload-suitable pair and a metal shaft-retention stack. Printed bearing blocks have a slip-fit seat and bolted retainers; they do not establish precision preload. Bearing centres are X=±60.5, Y=55.5, Z=50.

Motor provision: NEMA17 face 42.3 mm square, 31 mm mounting square, M3 screws, 22 mm pilot, 5 mm shaft. Reserve 80 mm behind the motor face for body and encoder, plus 20 mm for a rear connector/cable bend. Motor face X=130; shaft points toward −X. Allow a 40 mm long, 25 mm OD clamp coupling with 5/15 mm bores. Coupling and motor are purchased components; simplified CAD envelopes must be checked against the final part drawing. Use a closed-loop drive with a matched motor/encoder; reserve room for an output-angle encoder, but do not claim motor feedback measures platter error.

Electronics service box: 168 × 112 × 80 mm including lid, behind the table on its own four 28 mm feet. The box spans Z28–108; the external heat sink has 14.25 mm clearance above the bench. Separate screw-down lid, replaceable 2 mm EPDM gasket, gland entries and removable controller tray. Reserve a 118 × 76 × 35 mm motor-driver envelope, an 80 × 55 × 20 mm motion-controller envelope, and wiring/service space. These are packaging envelopes, not selected boards or a wiring design. Use slotted tray mounting, then drill the final board pattern from its drawing. Keep a route for motor power, encoder, home sensor and external emergency-stop wiring.

Use an external enclosed 24 V DC supply for initial packaging. No mains supply is placed in the printed enclosure. Include a 118 × 76 × 3 mm aluminium heat spreader and a 98 × 54 × 18 mm external finned heat-sink provision below the sealed floor. A 0.5 mm thermal adhesive pad is represented; final heat-sink retention and driver thermal contact must be designed for the selected parts. The heat-spreader gasket is 1 mm nominal compressed to 0.75 mm against metal shim stops. Keep its four clamp penetrations sealed. Validate temperatures with the lid shut and at maximum intended current. Sealed air volume alone is not adequate cooling evidence. Ground/bond exposed metal as required by the final electrical design. Electrical integration and coordinated robot control are not implemented in this revision.

## 5. Dust and splash resistance

1. Rotating skirt: downward overhang around the platter. Fixed upstand sits inside it, with nominal 2 mm radial and axial running clearance. The two turns in the entry path reject direct splash; this is not a contact seal.
2. Rib clearance: all rotating ribs end below R146.2; the main fixed wall starts at R150. Seam braces end at Z96 and ribs start at Z98, preserving 2 mm vertically as they sweep. The upstand ends at Z114 beneath the Z116 deck.
3. Outside gutter: catches water outside the drive space and drains through downward/outward outlets. No drain empties into the electronics box. Avoid recesses that retain slurry.
4. Static joints: seal the four housing seams and platter seams with removable neutral-cure RTV/appropriate sealant, backed by bolted seam strips. Printed seam gaps are 0.4 mm; they are not watertight without sealing.
5. Motor pod: a separate screw-down hood, 2 mm EPDM compressed to 1.5 mm against hard stops, and RTV at the curved transition to the main enclosure. Two 16.5 mm gland provisions are on the stationary rear wall.
6. Electronics: three 16.5 mm gland provisions, a continuous EPDM gasket, compression stops and cable glands with their own seals. Nominal gasket thickness 2 mm, compressed to 1.5 mm (25%); choose material with an appropriate compression range. Lid bolts sit outside the wet-to-dry seal where possible. Use gland manufacturer's cable range and cutout, not generic thread assumptions.
7. Bearing and gearbox: choose sealed bearing variants; protect grease behind covers. The rotating labyrinth does not replace bearing seals. Seal printed walls if a coupon shows leakage through layers. Recheck after service.
8. Do an unpowered dust/splash ingress check with absorbent indicators before installing electronics. Repeat after assembly changes. No IP65 or waterproof claim follows from CAD.

## 6. A1 Mini fabrication specification

Printer envelope: 180 × 180 × 180 mm. Baseline 0.4 mm nozzle, PETG, 0.20 mm layer height. Use dry filament, calibrated flow and elephant-foot compensation. PLA may be used for dimensional coupons, not as the thermal/wet baseline. Do not assume the open A1 Mini can reliably print large ABS/ASA structural parts.

| Interface | Nominal design allowance before coupon correction |
| --- | --- |
| Two printed mating parts | 0.25 mm per side; 0.50 mm total across a sliding fit |
| Housing/platter section seams | 0.40 mm total gap, backed and sealed after assembly |
| Printed cylindrical slip seat | Purchased OD +0.30 mm **diametral**; coupons +0.20/+0.30/+0.40 mm |
| Rotating splash labyrinth | 2.0 mm radial and axial; do not tighten to printer nominal resolution |
| M3 printed through hole | 3.4 mm |
| M4 printed through hole | 4.5 mm |
| M5 printed through hole | 5.5 mm |
| M6 printed through hole | 6.6 mm |
| M5 hex-nut pocket | 8.4 mm across flats ×4.4 mm deep, validate actual nut |
| M6 hex-nut pocket | 10.4 mm across flats ×5.4 mm deep, validate actual nut |
| M3 heat-set insert trial pilot | 4.0 mm for RX-M3x5.7; **verify purchased insert and printed coupon** |
| Metal plate fastener holes | Standard clearance/tapped dimensions; do not apply printed-fit allowance |

Main enclosure walls are 4 mm; the housing floor is 2.5 mm. Local sensor and insert geometry is thinner and must be checked on the coupon/first articles. Do not extrapolate the main wall thickness to every small feature. Structural parts: 6 perimeters, 8 top/bottom layers, 35–45% infill as a starting profile; use solid modifier regions around bolted interfaces. Covers may use 4 perimeters and 20–25% infill. Fasten with metal nuts/inserts and washers, not printed threads. Compression tubes bypass plastic where sustained clamp force matters. Final screw torque must be established on coupons; metal hardware torque tables do not apply to PETG joints.

Print platter sections with the flat work surface on the bed and ribs/skirt upward. Print sleeves and bearing blocks with the bearing axis vertical where possible to keep the fit round. Print the hub flange face on the bed, neck up. Print the service box upright, lid flat, and seam strips flat. The revised motor foundation prints flat on its underside; the motor bracket and home-sensor bracket print on their sides; the motor hood prints roof-down. Housing gutters and the electronics box inward top rim need local support. Keep supports out of gasket lands and bearing seats. The largest 168 mm part with 5 mm brim each side occupies 178 mm, inside the bed; check the actual slicer footprint including skirt, purge line and orientation.

Include a compact fit coupon with the actual fastener holes, insert pilots, nut pockets and bearing-seat clearance options. Print and measure it before the full assembly. PETG shrinkage, hole bias and material brand determine the final correction; nominal CAD allowances are not guaranteed printer accuracy.

## 7. Assembly and commissioning order

1. Print/measure coupons and correct the named fit parameters. Obtain hardware drawings; finish metal datum plates, output wheel attachment and shaft/retention stack.
2. Assemble the base plate, metal compression tubes and bearing seat on a flat bench. Verify flatness and squareness before tightening the bearing.
3. Install bearing, output hub and wheel; verify outer-ring/flange clearance and free rotation before installing the worm.
4. Assemble worm shaft, opposed support bearings and retainers. Set axial preload in the metal retention stack. Bolt the cartridge down, align centre distance and adjust duplex backlash through 360°.
5. Install motor, coupling and cable restraint. Verify no shaft or motor bearing carries the platter's axial load.
6. Fit printed covers, backed seams, labyrinth, gutter and drain outlets. Fit platter quadrants and seal their seams. Install a properly secured foam fixture.
7. Assemble driver/controller on the removable tray and heat spreader. Fit glands and lid gasket; perform unpowered ingress checks first.
8. Test low-speed motion unloaded, then progressively loaded. Measure bidirectional lost motion, TIR, tangential stiffness, motor/driver temperature and ingress. Log results and revise speed/current/load limits.

A brake or table clamp can be added for stationary machining, but it cannot supply stiffness while the table is rotating. Continuous carving requires coordinated motion control and measured loaded accuracy. No carving validation is implied by the CAD joint animation.

## 8. Verification and release gates

CAD: all new bodies closed; no failed features; every printable part fits ≤168 mm in its intended orientation; mounting holes and gasket compression checked; no unintended intersections at 17 sampled positions around a revolution, with analytic radial/vertical clearances for the rib and labyrinth sweeps; bought gear-tooth envelope overlap explicitly excluded from interference results. Keep the imported arm's existing surface warnings separate from new-part health.

Do not mark fabrication released until: actual motor/driver/encoder/gland drawings are chosen; bearing variant and mounting holes confirmed; shaft/key/preload and worm-wheel secondary machining drawings agreed; print coupons passed; fastener lengths and access checked against actual hardware; dimensional and loaded tests passed. Do not claim stone-machining capability from the foam prototype.

## 9. Sources

- [Bambu A1 Mini specifications](https://bambulab.com/en/a1-mini/tech-specs): 180 mm build envelope; verify against the printer profile before slicing.
- [KHK duplex worm catalog](https://khkgears.net/pdf/agdl.pdf), printed pp. 406–409: axial backlash adjustment, KWGDL2-R1/AGDL2-40R1 geometry, supplier assembly restrictions. Gear references are purchased components, not copied tooth CAD.
- [THK RU product family](https://www.thk.com/jp/ja/products/cross_roller_ring/cross_roller_ring/ru/ru/) and [THK dimensional guide](https://tech.thk.com/upload/catalog_claim/pdf/IMTS2022_THK_Mobile_Guidebook.pdf): integrated mounting rings; confirm current purchased variant before machining.
- [Föhrenbach RT2A](https://foehrenbach.com/en/products/rotary-tables-with-worm-gear-series-rt2a): industrial bearing/worm architecture reference, not a selected table.

The tolerances and targets in this specification are project design choices unless explicitly attributed to a manufacturer. They need the listed physical validation.
