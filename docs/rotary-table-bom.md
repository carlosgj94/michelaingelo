# Bill of materials — RT-01 revision 5

For **one rotary table, its electronics enclosure and its fixed arm mounting stand**. The robotic arm, its motors, its electronics and all of its internal hardware are excluded. **The four bolts attaching the existing arm to M50 are included.** Dimensions are millimetres unless stated otherwise.

In SolidCraft, expand the **Bodies** folder in a subassembly to see its sourcing groups. Use this BOM for the quantities, specifications and ordering notes behind those labels. Quantities are installed totals with **no spares**. The [parts list](../cad/parts.json), [print manifest](../exports/rotary-table/print-manifest.json) and [fastener register](rotary-table-fasteners.md) supply the underlying data.

| SolidCraft group | Display color | What it covers |
| --- | --- | --- |
| **To Be Printed** | Yellow | 25 yellow PETG assembly bodies. Section 1 also lists the separate fit coupon. |
| **To Be Bought** | Black | Bearings, gear pair, motor, coupling, sensor, spacers, washers and seals. Check the notes for stock that needs cutting and parts that need secondary machining. |
| **To Be Fabricated** | Grey | 17 custom metal bodies and the B03 shaft reference. Section 2 also lists the two separate bench backing strips. |
| **Space Reservations** | Cyan | Driver, controller and sensor cordset envelopes for parts still to be selected. The optional output encoder has no quantity in the baseline order. |
| **Existing Arm Reference** | Imported appearance | The mounted SO100 and its internal components. Only its mounting hardware appears in the RT-01 order. |

Section 7 lists bought hardware even when it has no permanent CAD body. The assembly uses **97 specified-length screws, four arm screws to fit, and 18 bench bolts to size for the actual bench**. The fastener CSV gives the same quantities for purchasing.

**Defined** means the current drawing specifies the item; physical fit tests still apply. **Confirm** means a reference size/model exists but the supplier drawing or actual part must be checked. **TBD** means the specification, quantity or length is unfinished. The design remains a prototype; see the [machining requirements](specs/rotary-table.md#3-metal-location-machining-and-inspection) and [release gates](rotary-table-validation.md#not-run--release-gates).

## 1. To Be Printed — PETG on the A1 Mini

Print **one copy of every linked assembly STL**. The quantities below are the number of distinct listed files, including each of the four platter and housing quadrants. Sizes are rounded print envelopes; supplied STLs are already oriented. Use the [printing guide](rotary-table-printing.md) for supports, calibration and first articles.

| Component type | Qty | Print envelope per piece, mm | STL files |
| --- | --- | --- | --- |
| Column sleeves | 4 | 22 × 22 × 69.5 | [P11](../exports/rotary-table/stl/p11-column-sleeve.stl), [P12](../exports/rotary-table/stl/p12-column-sleeve.stl), [P13](../exports/rotary-table/stl/p13-column-sleeve.stl), [P14](../exports/rotary-table/stl/p14-column-sleeve.stl) |
| Motor mounting bracket | 1 | 38 × 68 × 62 | [P24](../exports/rotary-table/stl/p24-nema17-motor-bracket.stl) |
| Platter quadrants | 4 | 159.8 × 159.8 × 30 | [P31](../exports/rotary-table/stl/p31-platter-quadrant.stl), [P32](../exports/rotary-table/stl/p32-platter-quadrant.stl), [P33](../exports/rotary-table/stl/p33-platter-quadrant.stl), [P34](../exports/rotary-table/stl/p34-platter-quadrant.stl) |
| Fixed housing quadrants | 4 | 163.8 × 163.8 × 114 | [P41](../exports/rotary-table/stl/p41-fixed-housing-quadrant.stl), [P42](../exports/rotary-table/stl/p42-fixed-housing-quadrant.stl), [P43](../exports/rotary-table/stl/p43-fixed-housing-quadrant.stl), [P44](../exports/rotary-table/stl/p44-fixed-housing-quadrant.stl) |
| Housing seam backing strips | 4 | 24 × 84 × 8 | [P45-1](../exports/rotary-table/stl/p45-seam-backing-strip-1.stl), [P45-2](../exports/rotary-table/stl/p45-seam-backing-strip-2.stl), [P45-3](../exports/rotary-table/stl/p45-seam-backing-strip-3.stl), [P45-4](../exports/rotary-table/stl/p45-seam-backing-strip-4.stl) |
| Motor service hood | 1 | 115.9 × 82 × 82 | [P46](../exports/rotary-table/stl/p46-motor-service-hood.stl) |
| Electronics box | 1 | 168 × 112 × 76 | [P50](../exports/rotary-table/stl/p50-electronics-service-box.stl) |
| Removable controller tray | 1 | 138 × 80 × 3 | [P51](../exports/rotary-table/stl/p51-removable-controller-tray.stl) |
| Electronics lid | 1 | 168 × 112 × 4 | [P52](../exports/rotary-table/stl/p52-electronics-lid.stl) |
| Electronics feet | 4 | 20 × 20 × 28 | [P53-1](../exports/rotary-table/stl/p53-electronics-foot-1.stl), [P53-2](../exports/rotary-table/stl/p53-electronics-foot-2.stl), [P53-3](../exports/rotary-table/stl/p53-electronics-foot-3.stl), [P53-4](../exports/rotary-table/stl/p53-electronics-foot-4.stl) |

| Calibration part | Qty | Size, mm | File |
| --- | --- | --- | --- |
| Fit coupon | 1 initially | 150 × 100 × 24 | [fit-coupon.stl](../exports/rotary-table/fit-coupon.stl) |

Buy yellow PETG filament. The required mass is **TBD after slicing**, including supports, brim and calibration. The 25-piece total does not include extra calibration/reprint attempts. Largest assembly dimension is 168 mm; the largest footprint with a 5 mm brim is 178 mm on the 180 mm bed. Inspect actual slicer placement. Retired P20/P21/P22/P23/P25/P30 prints are not part of this BOM.

## 2. To Be Fabricated — metal structure and precision parts

Send the linked STEPs **with the specification**, not as tolerance-complete shop drawings. Plate sizes below describe finished nominal features, not sufficient raw-stock blanks: integral guides, pilots, bosses and risers require additional material. Final material grade, tolerances and coatings must be agreed with the fabricator where not yet specified.

| Reference / STEP | Qty | Component / material | Required features |
| --- | --- | --- | --- |
| [M01](../exports/rotary-table/metal/m01-aluminium-base-plate.step) | 1 | Machined aluminium base | 164 × 184 × 8 nominal plate, local thread bosses, locating recesses and integral guide |
| [M02](../exports/rotary-table/metal/m02-aluminium-bearing-seat.step) | 1 | Machined aluminium bearing seat | Ø156 / Ø94 × 8 nominal; bearing register and sensor pad |
| [M11](../exports/rotary-table/metal/m11-steel-locating-column.step), [M12](../exports/rotary-table/metal/m12-steel-locating-column.step), [M13](../exports/rotary-table/metal/m13-steel-locating-column.step), [M14](../exports/rotary-table/metal/m14-steel-locating-column.step) | 4 | Turned steel locating columns | Ø10 / Ø6.2 × 72; matched ground ends and measured locating fits |
| [M20](../exports/rotary-table/metal/m20-registered-output-hub.step) | 1 | 6061-T6 aluminium output hub | Registered bearing/wheel pilots, blind M6 fixture bosses and sensor-target mount |
| [M60](../exports/rotary-table/metal/m60-monolithic-worm-carrier.step) | 1 | 6061-T6 aluminium worm carrier | 156 × 94 × 8 base with integral bearing blocks; machine seats in one setup |
| [M61 left](../exports/rotary-table/metal/m61-worm-bearing-retainer-left.step), [right](../exports/rotary-table/metal/m61-worm-bearing-retainer-right.step) | 2 | Machined aluminium bearing caps | 54 × 54 × 4, outer-race contact boss; match to actual bearing |
| [M30](../exports/rotary-table/metal/m30-driver-heat-spreader.step) | 1 | Aluminium driver heat spreader | 118 × 76 × 3 |
| [M40](../exports/rotary-table/metal/m40-stepped-motor-support.step) | 1 | Machined aluminium motor foundation | 172 × 82 × 4 sole with integral 8 mm riser, hood stops and tapped holes |
| [M50](../exports/rotary-table/metal/m50-so100-arm-mounting-plate.step) | 1 | Aluminium arm mounting plate | 228 × 116 × 8; four Ø3.3 tap drills for M4 × 0.7-6H threads, four Ø6.6 stand holes and ten lid-tool access holes |
| [M51 left](../exports/rotary-table/metal/m51-steel-side-channel-left.step), [right](../exports/rotary-table/metal/m51-steel-side-channel-right.step) | 2 | Welded steel side channels | 4 mm plate, 116 deep × 144 high, 28 mm flanges |
| [M52](../exports/rotary-table/metal/m52-steel-front-x-brace.step) | 1 | Steel front X brace | 228 × 136 × 4; weld to the side channels |
| [B12](../exports/rotary-table/metal/b12-retained-steel-home-target.step) | 1 | Mild-steel home-sensor target | Ø12 × 3 with M3 countersink; stainless is not the specified target material |
| [M55](../exports/rotary-table/metal/m55-bench-backing-strip-make-two.step) | 2 | Steel bench backing strips | 40 × 136 × 3; two Ø6.6 holes 96 mm apart and two Ø16 scallops. Make two identical pieces and orient the scallops inward. |

The total above is **19 finished components/subassemblies**: 17 in the table assembly plus two separate under-bench strips. It does not count each welded blank as another finished part. For the two M51 channels, the shop uses **four 28 × 116 × 4 flange blanks and two 116 × 136 × 4 web blanks**, plus the M52 brace listed above. Weld before finishing datums and matched holes. Weld sizing/process remains to be approved for the actual loads.

The M50 plate, M51 channels, M52 brace and M55 strips are the new support for the existing arm; they are included even though the arm itself is excluded.

**B03 worm shaft · 1 finished shaft.** The Ø15 × 177 CAD body is an envelope. The machining drawing still needs the keys, shoulders, retention and preload stack.

## 3. To Be Bought — bearings and mechanical transmission

| Component | Qty | Reference / specification | Status / purchase note |
| --- | --- | --- | --- |
| Crossed-roller output bearing | **1 complete bearing** | RU85-size, Ø55 bore × Ø120 OD × 15 | **Confirm** exact preload, seals, ring holes and threads. B01 and B10 are the two modeled rings of this one bearing; do not order two bearings |
| Angular-contact worm bearings, B02 | 2 | 7202-size, Ø15 × Ø35 × 11 | **Confirm** opposed arrangement, preload suitability and actual supplier variant |
| Duplex worm, B04 | 1 | KHK KWGDL2-R1, module 2, right-hand | **Confirm** supplier-approved Ø15 bore/key machining and matching wheel |
| Duplex worm wheel, B11 | 1 | KHK AGDL2-40R1, 40:1 with the worm above | **Confirm** bore/pilot, four M5 hub threads and drive-pin radial slot machining |
| Motor-to-worm clamp coupling, B05 | 1 | Metal coupling, 15/5 mm bores, envelope ≤Ø25 × 40 | **TBD SKU**: verify insertion depth, clamp access and alignment allowance. Use its supplied clamp screws; their count is not in the fixed screw totals |
| Wheel drive pin, M21/H02 | 1 | Ground hardened steel, Ø4 × 12 nominal | **Confirm** certified strength and matched press/slot fits in the specification; not a generic soft pin |

The worm and wheel are **one matched gear pair**. They are not printed. Secondary machining of purchased parts needs supplier/fabricator approval. Shaft keys, locknuts, inner-ring spacers and retaining hardware are still **TBD** and are not silently included in the 119-screw count.

## 4. Buy or cut to size — spacers and precision shims

| Component | Qty | Specification, mm | Status / purchase note |
| --- | --- | --- | --- |
| Core-to-bench spacers, M03–M06 | 4 | Metal, Ø18 OD / Ø6.6 ID × 4 | **Defined size**; buy finished spacers or have them made |
| Worm retainer shims, M62/H03 | 2 fitted positions | Profile matching the 54 × 54 caps; nominal 0.05 thickness | **Confirm measured thickness**; obtain shim stock and cut/lap the correct openings. More trial stock may be needed; these set outer-race clearance, not shaft preload |
| Heat-spreader compression stops, M31–M34 | 4 | Metal shim washers, Ø6.5 OD / Ø3.4 ID × 0.75 | **Defined size**; included once here, although also listed in F20 and the fastener CSV |

## 5. Buy — actuator, controls, sensors and cooling

These items serve the **rotary table**. No arm actuator, arm controller or arm power supply is included.

| Component type | Qty | Required reference / space | Status / purchase note |
| --- | --- | --- | --- |
| Closed-loop stepper motor with motor encoder, B06 | 1 matched assembly | NEMA17, ≤42.3 square × 80 rear length, 5 mm shaft; 20 mm additional cable reservation | **TBD SKU**; select with the driver and actual speed/torque requirements |
| Motor driver, B22 | 1 | Body reservation ≤118 × 76 × 35 | **TBD SKU**; match the drive and supply. Include any connector parts that stay attached during extraction in this envelope. Select the driver-side thermal interface. |
| Motion controller, B23 | 1 | Body reservation ≤80 × 55 × 20 | **TBD SKU**; compatible motion commands and home-sensor interface. Board holes/standoffs not designed |
| Inductive home sensor, B08 | 1 | SICK IME08-02BPSZT0S mechanical reference, M8 × 1, PNP normally open | **Confirm** sensor and input compatibility. Two mounting nuts are listed in section 7 and normally supplied with it |
| Home-sensor cordset, B09 | 1 | Matching M8 connector and cable | **TBD** exact connector, length, bend radius and routing |
| External enclosed DC power supply | 1 | 24 V baseline, outside printed box | **TBD** current/power rating to match selected motor/driver; this is not an arm supply |
| External finned heat sink, B26 | 1 | Envelope ≤98 × 54 × 18 | **TBD SKU**, thermal capacity and retention method |
| Thermal interface pad, B27 | 1 fitted piece | 98 × 54 × 0.5 reference envelope | **TBD** grade/attachment; an adhesive-pad placeholder does not establish heat-sink retention |
| Platter/output encoder, B07 | Optional; 0 in baseline order | Reserved Ø40 × 16 space | **TBD** device, mount and electrical interface. Separate from the motor's encoder; homing does not provide continuous platter-angle feedback |

## 6. Buy / cut — seals, wiring and consumables

| Type | Qty | Specification / procurement note |
| --- | --- | --- |
| Core perimeter gasket, B20 | 1 | EPDM **2 mm stock**, 164 × 164 outside / 152 × 152 inside; installed thickness 1.5 |
| Motor-hood gasket, B25 | 1 | EPDM **2 mm stock**, curved profile; installed thickness 1.5. Cut the supplied profile, not a simple rectangular ring |
| Electronics lid gasket, B24 | 1 | Cut a continuous 2 mm-wide ring from 2 mm EPDM sheet, 149.5 × 93.5 outside and 145.5 × 89.5 inside. Installed thickness 1.5. Confirm compound, compression force and swell for the 3.5 mm-wide groove. |
| Heat-spreader gasket, B21 | 1 | Closed-cell **1 mm stock**, 108 × 64 outside / 102 × 58 inside; installed thickness 0.75 |
| Heat-spreader screw sealing washers | 4 | EPDM Ø7 OD / Ø3.2 ID × **1 mm stock**, compressed to 0.75; F20, counted once here |
| Electronics bench-anchor sealing washers | 4 | F21 EPDM Ø9 OD / Ø3.8 ID × 1 mm stock. Trial target of 0.75 mm installed beneath the OD9 metal washer. Confirm actual seal imprint and preload. |
| Cable glands / blanking plugs | **5 openings total** | Two motor-hood and three electronics holes, Ø16.5. **TBD** gland thread/land and cable diameters; fit compatible sealed plugs at any unused openings. Five openings does not mean five glands plus five plugs |
| Static-seam sealant | Stock quantity TBD | Removable neutral-cure RTV compatible with PETG, water and chosen lubricant |
| Gear/bearing lubricant | Type and amount TBD | Use the selected gear/bearing suppliers' lubrication requirements; do not assume one grease suits every interface |
| Motor, encoder, DC and control wiring | Lengths/quantities TBD | Match selected devices and motion/control wiring; include suitable connectors, strain relief, ferrules and cable clamps |
| Electrical protection, isolation / E-stop components | Quantities/specification TBD | Finish the electrical diagram and stopping method before selecting hardware; no completed circuit is claimed |

The [gasket STEP](../exports/rotary-table/seal-profiles.step) shows installed shapes. Cut B24 to the stock dimensions above because its width changes when compressed. Use the stock thicknesses in this table for the other gaskets. A rigid shared bench is required. Size and construction depend on the chosen bench and load case.

## 7. Buy — bolts, screws, nuts, washers and inserts

The following are **consolidated installed totals**, including the arm mounting hardware. They replace the need to add up each joint yourself. The [fastener CSV](../cad/fastener-shopping-list.csv) and [joint-by-joint register](rotary-table-fasteners.md) describe these same items.

Threads are coarse: M3 × 0.5, M4 × 0.7, M5 × 0.8, M6 × 1. Screw length is under-head except DIN 7991 countersunk lengths, which include the head. Preserve the exact head styles and washer diameters. Use the register's material/grade and torque requirements for each joint: protected class 8.8 is the metal-frame baseline, A2-70 is the cover/electronics baseline, and bearing supplier requirements take precedence. Shared size totals may need splitting by material/grade when ordering.

### Socket-head cap screws — ISO 4762

| Size, mm | Total qty | Joint allocation | Use / confirmation |
| --- | --- | --- | --- |
| M3 × 10 | 4 | F11 (4) | Confirm selected motor thread depth |
| M4 × 12 | 8 | F09 (8) | Bearing retainer caps |
| M4 × 25 | 16 | F15 (16) | Housing seams |
| M4 × 95 | 4 | F17 (4) | Motor hood; see 95 mm length note below |
| M5 × 16 | 4 | F07 (4) | Worm carrier |
| M5 × 20 | 12 | F04 (8), F10 (4) | Confirm bearing threads and engagement; Motor bracket |
| M5 × 25 | 8 | F03 (8) | Confirm bearing flange/head details |
| M5 × 45 | 4 | F05 (4) | Confirm wheel machining and preload |
| M6 × 25 | 4 | F22 (4) | Arm mounting plate to steel stand |
| M6 × 90 | 4 | F01 (4) | Core columns |

### Button-head screws — ISO 7380-1

| Size, mm | Total qty | Joint allocation | Use / confirmation |
| --- | --- | --- | --- |
| M3 × 10 | 14 | F18 (10), F19 (4) | Electronics lid; Controller tray |
| M5 × 16 | 8 | F06 (8) | Recessed platter screws; button heads required |

### Countersunk screws — DIN 7991, 90°

| Size, mm | Total qty | Joint allocation | Use / confirmation |
| --- | --- | --- | --- |
| M3 × 8 | 1 | F25 (1) | Home target; head Ø≤6 |
| M3 × 16 | 4 | F20 (4) | Heat spreader; head Ø≤6 |
| M5 × 12 | 2 | F13 (2) | Motor support to core; head Ø≤10 |

These three tables total **97 specified-length screws**, comprising 68 socket cap, 22 button and seven countersunk. The four additional F24 screws are sized after measuring the fitted arm seats in section 8. Dimensions with a supplier confirmation note are provisional. If M4 × 95 is unavailable, the register permits finishing M4 × 100 to 95 while retaining at least 16 mm of threaded tip.

### Bench through-bolts — choose length after measuring the bench

All 18 are ISO 4762 socket-head cap bolts. **T** is the actual solid bench-top thickness at the hole. Round the minimum up to the next available suitable length and check underside clearance and nut engagement. Include any extra backing thickness not already covered by the formula. A loose wood block is not the specified shared rigid bench.

| Joint | Qty | Thread | Minimum under-head length, mm |
| --- | --- | --- | --- |
| F02 — rotary core | 4 | M6 | T + 23.6 |
| F14 — motor foundation | 2 | M6 | T + 23.6 |
| F16 — fixed housing | 4 | M5 | T + 11.5 |
| F21 — electronics feet/box | 4 | M4 | T + 40.95; insert from below into the captive nut |
| F23 — steel arm stand | 4 | M6 | T + 18.2; includes the 3 mm M55 strips |

The washers/nuts for these anchors are already included below. The two M55 strips are already included in the fabrication table.

### Nuts — 50 assembly nuts plus two sensor nuts

| Item / dimensions, mm | Total qty | Use |
| --- | --- | --- |
| M3 DIN 985 nyloc nut h4 | 4 | Heat spreader |
| M4 DIN 985 nyloc nut h5 | 20 | 16 housing seams + 4 captive electronics anchors |
| M5 DIN 934 plain nut AF8 h4 | 8 | Outer bearing |
| M5 DIN 985 nyloc nut h5 | 4 | Housing bench anchors |
| M6 DIN 985 nyloc nut h6 | 14 | Core/motor/stand anchors and arm-plate mounting |
| M8 × 1 sensor jam nut, AF13, thickness ≤4 | 2 | B13/H01; normally supplied with sensor, check package before buying separately |

### Metal washers — 134 total

ID and OD are inner and outer diameter. The final dimension is thickness. The eight EPDM sealing washers and four metal compression stops appear separately in sections 6 and 4.

| Item / dimensions, mm | Total qty | Use |
| --- | --- | --- |
| M3 washer ID3.2 OD7 x 0.5 | 22 | Motor face, lid/tray and heat spreader |
| M4 fender washer ID4.3 OD12 x 1 | 4 | Under bench at electronics feet |
| M4 washer ID4.3 OD9 x 0.8 | 52 | Includes four upper arm-seat washers and four F21 washers |
| M5 DIN 9021 washer ID5.3 OD15 x 1.2 | 8 | Housing bench anchors, above and below |
| M5 washer ID5.3 OD10 x 1 | 16 | Outer bearing, worm carrier and motor bracket |
| M6 fender washer ID6.6 OD24 x 2 | 6 | Under bench at core and motor support |
| M6 small washer ID6.4 OD11 x 1.6 | 4 | Column bolts; small OD required beside bearing |
| M6 washer ID6.6 OD18 x 1.6 | 22 | Includes B41–B42 and B51–B54 modeled washers; do not add them again |

### Threaded inserts

| Item | Qty | Allocation |
| --- | --- | --- |
| ruthex RX-M3x5.7 heat-set insert | **14** | 10 electronics-lid positions + 4 controller-tray positions |

These fasten the lid and tray, **not the controller board itself**. Coupon-test the insert pilots and retention. Board mounting screws/standoffs remain TBD.

## 8. Arm-to-base attachment

The existing arm attaches with bolts to **M50, the metal mounting plate above the electronics box**. Its load passes through the metal stand to the shared bench.

| F24 attachment item | Quantity |
| --- | --- |
| M4 ISO 4762 socket-head screw, finish to measured length | **4** |
| M4 metal washer, ID4.3 / OD9 × 0.8 | **4** already included above |
| Matched supported upper bearing seat | **4 positions**, detail and material pending measurements of the owned foot |

F24 enters four tapped holes from above. Measure grip G from the top of M50 to the installed head seat at each hole. Select length L so L − G is 6.5–7.0 mm and at least 6.0 mm of full thread engages after entry and tip runout. Require at least 1 mm recess from the underside. Use the seat acceptance in the fastener register before ordering or cutting screws. [Nonrectangular four-hole pattern](../cad/arm-mount-reference.json)

## 9. Items that cannot yet be ordered to a final specification

| Interface | What remains to select / define |
| --- | --- |
| Bearings and gear machining | Actual bearing variants, approved fits/preload, finished worm/wheel bores, key and wheel attachment machining |
| Worm shaft | Finished drawing, keys, shoulders, locknuts, inner-ring spacers and any retaining screws |
| Motor / coupling / controls | Exact compatible products, coupling fasteners, board standoffs/screws, supply rating and electrical protection |
| Cooling | Driver mounting/contact, pad specification and heat-sink retention/fasteners |
| Cables and seals | Cordset and cable lengths, glands/plugs, strain relief and connector service clearances |
| Workholding | Actual clamps, workpiece fixtures and screws. Four blind M6 mounting positions exist; bolt length depends on the fixture stack, so no arbitrary clamp kit or screw length is added here |
| Bench and stand fabrication | Bench thickness/rigidity, anchor lengths, any extra backing, weld details and corrosion protection |
| Optional output encoder | Device, mounting and wiring only if this option is adopted |

For workholding, require **8–9 mm engagement** into the blind M6 bosses. Screw length minus the fixture and washer stack above Z128 must be **15–16 mm**. Fixture screws and unfinished device mounting hardware are outside the current 119-screw schedule.

## Sources and review files

- [Parts list](../cad/parts.json), [print manifest](../exports/rotary-table/print-manifest.json), [fastener data](../cad/fasteners.json) and [fastener purchasing CSV](../cad/fastener-shopping-list.csv).
- [Specification](specs/rotary-table.md), [printing/assembly guide](rotary-table-printing.md), [audit response](rotary-table-audit-response-2026-11-17.md) and [validation report](rotary-table-validation.md).
- [Current package](../exports/rotary-table/rt01-print-package.zip) includes this BOM, STLs, metal references and review evidence.

The SolidCraft groups cover 81 table and support bodies plus the existing arm. B01 and B10 represent one bearing. Modeled washers are already included in the hardware totals, and space reservations mark dimensions for parts that still need selection.
