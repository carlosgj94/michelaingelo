# RT-01 parts and purchasing notes — revision 4

Reconciled with [cad/parts.json](../cad/parts.json): **81 table/support bodies: 25 printed, 17 metal fabrication bodies, 35 purchased/reference bodies and 4 space reservations**. Bearing rings represent one purchased set. Two bench backing strips are separate fabrication geometry because bench thickness is unknown. Simplified bought-part envelopes are not manufacturing drawings or a complete order release.

Audit fixes deliberately replace printed alignment and sustained-clamp interfaces with metal. Read the [machining/inspection requirements](specs/rotary-table.md#3-metal-location-machining-and-inspection) before requesting quotations. More machining is required than the original two-datum-plate concept.

## Printed parts

| Part | Qty | Purpose |
| --- | ---: | --- |
| P11–P14 | 4 | Covers around locating steel columns; 69.5 mm long |
| P24 | 1 | NEMA17 mounting bracket; first-article clamp/pilot check |
| P31–P34 | 4 | Ribbed platter quadrants with clearance over metal fixture bosses |
| P41–P44 | 4 | Fixed enclosure quadrants, supported anchor locations and flat seam seats |
| P45 | 4 | Seam backing strips; all supplied broad-face down |
| P46 | 1 | Removable motor hood |
| P50–P52 | 3 | Electronics box, tray and lid |
| P53 | 4 | Electronics feet |
| Coupon | 1 extra | Vertical/horizontal screw fits, inserts, columns and fixture-boss pockets |

Total **25 assembly prints plus one coupon**. P20/P21/P22/P23/P25/P30 are retired; do not print their revision 3 STLs. All generated stale files are removed from the current package.

## Metal fabrication and bought interfaces

| Reference | Qty | Baseline / remaining requirement |
| --- | ---: | --- |
| M01 | 1 | Aluminium base 164×184×8, local underside thread bosses, locating recesses and integral carrier guide |
| M02 | 1 | Aluminium seat Ø156/Ø94×8, interrupted outer-bearing register and sensor nut pad |
| M11–M14 | 4 | Steel locating columns Ø10/Ø6.2×72; finish round/slot fits and matched ground ends |
| M20 | 1 | 6061-T6 registered output hub; bearing/wheel pilots, blind fixture threads and target boss |
| M60 | 1 | One-piece 6061-T6 worm carrier, base 156×94×8 with integral blocks; line-bored seats and guide |
| M61 | 2 | Machined metal bearing caps 54×54×4 with outer-race contact boss; drawing checked against real bearing |
| M30 | 1 | Aluminium driver spreader 118×76×3 |
| M40 | 1 | Integral aluminium motor support: sole 172×82×4 plus 8 mm riser; hood stops and tapped motor/hood holes |
| M50 | 1 | Aluminium arm plate 228×116×8 at Z144–152; four arm holes, four stand holes, ten lid-tool holes |
| M51 | 2 | Welded4 mm steel channels 116 deep×144 high, 28 mm flanges |
| M52 | 1 | Steel front X brace 228×136×4; weld to side channels |
| B12 | 1 | Mild-steel targetØ12×3, M3 countersink; not stainless unless sensing is requalified |
| M55 | 2 separate | Steel backing strips 40×136×3, twoØ6.6 holes 96 apart; under the actual bench |
| M03–M06 | 4 | Metal bench spacersØ18/Ø6.6×4 |
| M21 | 1 | Ground hardened-steel drive pinØ4×12; matched interference/slot clearance and certified strength per specification |
| M62 | 2 | Retainer shims, nominal 0.05; select/lap from measured bearing/cap/pocket stack |
| M31–M34 | 4 | Spreader compression stopsØ6.5/Ø3.4×0.75, counted once in fastener register |
| B01 + B10 | **1 set** | RU85-size crossed-roller bearing 55×120×15; final sealing/preload/hole variant to confirm |
| B02 | 2 | Angular-contact bearing 15×35×11; opposed/preload-suitable selection and shaft retention still required |
| B03 | 1 | Ø15×177 shaft reference; keys, shoulders, locknuts, spacers and preload drawing unfinished |
| B04 / B11 | 1 each | KHK KWGDL2-R1 / AGDL2-40R1; supplier-approved bore/key, wheel pilot/slot and tapped-hole machining |
| B05 | 1 | Metal clamp coupling, 15/5 bores, ≤Ø25×40; actual SKU/clamps/insertion depth pending |
| B06 | 1 | Matched closed-loop NEMA17 motor/encoder,≤42.3 square×80 rear length, 5 mm shaft; SKU pending |
| B08 / B13 | 1 / 2 | SICK IME08-02BPSZT0S reference plus supplied AF13 nuts; require nut thickness≤4; matching cordset pending |
| B41–42 / B51–54 | 2 / 4 | M6 washersØ18/Ø6.6×1.6; included once in F14/F22 hardware |
| B22 / B23 | 1 each | Driver≤118×76×35, controller≤80×55×20; reservations, not selected devices |
| B26 / B27 | 1 each | External heat sink≤98×54×18 and 0.5 thermal pad; thermal performance/retention pending |
| B07 | optional | Ø40×16 output-encoder space; device/mount not designed |
| External supply | 1 | Enclosed24 V supply matched to selected drive; outside printed box |
| Cable glands | up to 5 | Two motor-hood and three electronics provisionsØ16.5; actual glands/seals/cable ranges pending |

The 17 fabrication bodies are M01/M02, four columns, M20, M60, two caps, M30/M40/M50, two channels, brace and steel target. Exported STEP references do not specify tolerances or approve machining of purchased components.

Each side channel uses two 28×116×4 flange blanks and one 116×136×4 web between them, overall 144. Make four flanges/two webs plus the front brace. Weld before finishing the top datum and matched holes; weld sizing/process and arm-reaction capacity require fabricator review. No weld beads are modeled.

## Seals and fastening

| Item | Quantity / stock thickness |
| --- | --- |
| B20 core gasket | One164 square outside/152 inside ring, 2 EPDM compressed 1.5 |
| B25 motor gasket | One curved profile, 2 EPDM compressed 1.5; verify curved transition and use compatible RTV |
| B24 lid gasket | One151×95 outside/145×89 inside ring, 2 EPDM compressed 1.5 |
| B21 spreader gasket | One108×64 outside/102×58 inside ring, 1 closed-cell material compressed 0.75 |
| Screw seals | Four EPDM washersOD7/ID3.2×1 compressed 0.75 at spreader penetrations |
| Static seam sealant | Removable neutral-cure RTV compatible with PETG, water and lubricant |

The [fastener register](rotary-table-fasteners.md) and [purchasing CSV](../cad/fastener-shopping-list.csv) cover **23 active groups, 101 fixed-length screws and 18 bench bolts**. Arm internals are excluded; four arm-base screws are included. F08/F12 are deleted; F25 is new. There are no hub/motor compression sleeves or printed captive-nut joints in revision 4. Keep conditional supplier interfaces and actual fixture/board/coupling/shaft hardware separate from the known installed quantities.

[Arm mounting coordinates](../cad/arm-mount-reference.json) preserve the measured nonrectangular four-hole pattern. Verify the physical purchased arm before drilling M50. The complete machine bolts to a shared rigid bench; choose anchor lengths only after measuring its thickness.
