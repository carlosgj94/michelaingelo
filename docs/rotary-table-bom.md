# RT-01 parts and purchasing notes

This is the prototype bill of materials, reconciled with `cad/parts.json`. The assembly contains five custom aluminium parts and three steel stand pieces; two additional steel backing strips are supplied as separate fabrication geometry. Other metal bodies are stock, purchased components or machining references. Do not order solely from the simplified gear, bearing, motor or electronics envelopes. Confirm supplier drawings and the release items in the [specification](specs/rotary-table.md).

## Printed parts

| Part | Quantity | Purpose |
| --- | ---: | --- |
| P11–P14 | 4 | Covers/location sleeves around the steel columns |
| P20 | 1 | Axially adjustable worm cartridge sled |
| P21 left/right | 2 | Worm bearing supports |
| P22 left/right | 2 | Bearing retainers |
| P23 | 1 | Motor-pod foundation |
| P24 | 1 | NEMA17 mounting bracket |
| P25 | 1 | M8 home-sensor mounting provision |
| P30 | 1 | Output hub with captive nuts and metal neck sleeves |
| P31–P34 | 4 | Ribbed platter quadrants |
| P41–P44 | 4 | Fixed enclosure quadrants with gutter |
| P45 | 4 | Bolted seam backing strips |
| P46 | 1 | Removable motor hood |
| P50–P52 | 3 | Electronics box, removable tray and lid |
| P53 | 4 | Electronics feet |
| Coupon | 1 | Bearing, nut, insert and screw-fit calibration |

Total: **33 assembly pieces plus one coupon**. Use the oriented STLs and print manifest; do not slice the purchased component envelopes.

## Metal and bought components

| Reference | Qty | Baseline / status |
| --- | ---: | --- |
| M01 | 1 | Aluminium base, 164 × 184 × 8 mm; custom machined |
| M02 | 1 | Aluminium bearing seat, OD156 / ID94 × 8 mm; custom machined |
| M30 | 1 | Aluminium heat spreader, 118 × 76 × 3 mm; custom machined |
| M40 | 1 | Aluminium motor sole, 172 × 82 × 4 mm, underside M5 countersinks and core-gasket reliefs; custom machined |
| M41–M42 | 2 | Steel motor-anchor sleeves, OD12 / ID6.6 × 8 mm |
| B41–B42 | 2 | M6 washers, OD18 / ID6.6 × 1.6 mm |
| M50 | 1 | Aluminium SO100 mounting plate, 228 × 116 × 8 mm, four M4 arm holes, four M6 stand-flange holes and ten lid-tool holes; custom machined |
| M51 left/right | 2 | Welded 4 mm steel side channels: 116 deep × 136 high, 28 mm top/bottom flanges; finish-machined top datum |
| M52 | 1 | Steel front X brace, 228 × 128 × 4 mm; weld to side channels |
| M55 backing strips | 2 | Steel 40 × 136 × 3 mm, two Ø6.6 holes 96 apart; separate STEP, installed below actual bench |
| B51–B54 | 4 | M6 washers, OD18 / ID6.6 × 1.6 mm |
| M03–M06 | 4 | Metal bench spacers, OD18 / ID6.6 × 4 mm |
| M11–M14 | 4 | Steel compression tubes, OD10 / ID6.2 × 70 mm, square matched ends |
| M21–M24 | 4 | Steel hub sleeves, OD8 / ID5.5 × 36 mm |
| M31–M34 | 4 | Metal compression-stop washers, OD6.5 / ID3.4 × 0.75 mm |
| B01 + B10 | **1 set** | RU85-size crossed-roller bearing, 55 × 120 × 15 mm; rings are one purchased bearing. Confirm exact hole layout, sealing and preload variant |
| B02 left/right | 2 | 7202-size 15 × 35 × 11 mm angular-contact bearings; matched/preload-suitable arrangement still to select |
| B03 | 1 | Steel worm-shaft reference, Ø15 × 177 mm. Shoulders, key, locknuts and preload stack need a manufacturing drawing |
| B04 | 1 | KHK KWGDL2-R1 duplex worm; proposed finish bore/key to 15 mm must be agreed with supplier |
| B11 | 1 | KHK AGDL2-40R1 duplex wheel; proposed four M5 tapped attachment holes on 30 mm PCD and pilot need machining review |
| B05 | 1 | Low-backlash metal clamp coupling, 15/5 mm bores, ≤Ø25 × 40 mm envelope; final SKU unselected |
| B06 | 1 | Closed-loop NEMA17 motor/encoder, ≤42.3 mm square × 80 mm rear length, 5 mm shaft; final SKU unselected |
| B12 + sensor | 1 each | Steel target and M8 radial home sensor provision; select sensing distance and dry/wet rating together |
| B07 | Optional | Output encoder reserved Ø40 × 16 mm; mounting/interface not designed |
| B22, B23 | 1 each | Driver ≤118 × 76 × 35 mm; controller ≤80 × 55 × 20 mm. Packaging reservations, not selected boards |
| B26, B27 | 1 each | External aluminium heat sink ≤98 × 54 × 18 mm and 0.5 mm thermal adhesive pad; thermal sizing and retention unverified |
| External supply | 1 | Enclosed 24 V DC supply, current matched to final drive; kept outside the printed box |
| Cable glands | Up to 5 | Two motor-pod and three electronics-box provisions, nominal 16.5 mm cutouts; confirm gland sealing washer/cable ranges |

Each M51 side channel uses **two 28 × 116 × 4 mm flange blanks and one 116 × 128 × 4 mm web between them**, giving 136 mm overall height. Make two channels: four flange blanks and two webs, plus the front X brace. Weld, inspect distortion, then finish the top datum before drilling the matched assembly. The STEP omits weld beads; weld sizing remains part of fabrication review.

The KHK pair is 40:1, module 2, with 55.5 mm centre distance. Buying only an ordinary same-module worm is not an interchangeable substitution. See [KHK's duplex catalog](https://khkgears.net/pdf/agdl.pdf).

## Seals and fastening

| Item | Quantity / provision |
| --- | --- |
| B20 core gasket | One 2 mm EPDM sheet ring, 164 mm square outside / 152 mm inside, installed at 1.5 mm |
| B25 hood gasket | One curved EPDM gasket, 2 mm nominal / 1.5 mm installed; use STEP profile and verify against printed parts |
| B24 lid gasket | One continuous EPDM ring, 151 × 95 mm outside / 145 × 89 mm inside, 2 mm nominal / 1.5 mm installed |
| B21 spreader gasket | One closed-cell gasket, 108 × 64 mm outside / 102 × 58 mm inside, 1 mm nominal / 0.75 mm installed |
| Static seam sealant | Removable neutral-cure RTV compatible with filament, water and lubricant |
| Heat-spreader screw seals | Four EPDM washers OD7 / ID3.2 × 1 mm, compressed to 0.75 mm below box floor |

See the **[assembly fastener register](rotary-table-fasteners.md)** for all 24 joint records, exact head styles, quantities, defined lengths, washers/nuts/inserts, stack-ups and assembly access. Its [purchasing CSV](../cad/fastener-shopping-list.csv) consolidates the counts. There are **106 fixed-length screws and 18 bench bolts** in the current design; some fixed-length interfaces still require the actual supplier/arm drawing to be confirmed. Fixture bolts and unselected device hardware are explicitly pending, not included in that count.

The old M3 seam/M4 drive labels and M5 × 50 wheel screws were wrong and are superseded. The housing seams use M4; sled, block and motor-foot joints use M5; wheel screws are M5 × 45. Fasteners are checked with disposable CAD envelopes but are not all retained as assembly bodies. Fit captive nuts before closing their pockets. Do not apply steel-joint torque tables to printed parts.

Scale-up keeps the vertical bearing, independent load path, enclosed duplex worm cartridge and stationary electronics arrangement. Recalculate the bearing, shaft, coupling, gear rating and heat dissipation; replace the printed hub, platter and drive supports with metal when load/stiffness tests demand it.

The SO100 mounting-hole coordinates and source faces are recorded in [cad/arm-mount-reference.json](../cad/arm-mount-reference.json). The four passages are not a regular rectangular pattern. Verify the physical revision before drilling M50. The printed controller lid carries no arm load.
