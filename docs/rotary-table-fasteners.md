# RT-01 assembly fastener register — revision 4

Updated 2026-11-17. **This replaces the earlier incomplete fastener notes.** It covers every currently designed assembly joint, including the arm-to-stand bolts, and excludes the arm’s internal screws. Unfinished component interfaces are listed at the end: the whole machine is not yet an order-ready screw kit.

All dimensions are mm. Coarse threads: M3×0.5, M4×0.7, M5×0.8, M6×1. Length is under-head except countersunk screws, where it includes the head. Use exact head styles: a cap head cannot replace a recessed platter button head. Countersinks are for DIN7991 heads (M3 <=Ø6; M5 <=Ø10); do not substitute larger ISO10642 heads without revising the recess. Nominal fits are checked in CAD; printed tolerances require the coupon.

Prototype baseline: corrosion-protected class 8.8 steel bolts / compatible nuts for metal frame and datum joints; A2-70 stainless for cover/electronics fasteners. Bearing screws must follow the selected bearing supplier’s class and torque. Keep coatings out of bearing seats; select corrosion protection compatible with aluminium and the wet environment. Do not use metal-joint torque tables on PETG, heat-set inserts or the printed arm. Final preload/torque requires supplier data and coupon/assembly checks. Use a validated anti-loosening method for metal joints, compatible with nearby PETG and seals. The former printed captive-nut joints have been removed.

## Installed quantities by joint

| ID | Joint | Qty | Screw | Mating hardware per screw | Status |
| --- | --- | ---: | --- | --- | --- |
| F01 | Core columns: M02 / locating columns / M01 | 4 | M6 × 90, ISO 4762 socket cap | 1 × M6 small washer ID6.4 OD11 x 1.6 | Defined geometry |
| F02 | Core to bench | 4 | M6 × L(T), ISO 4762 socket cap | 1 × M6 washer ID6.6 OD18 x 1.6; 1 × M6 fender washer ID6.6 OD24 x 2; 1 × M6 DIN 985 nyloc nut h6 | Bench thickness required |
| F03 | Outer bearing to M02 | 8 | M5 × 25, ISO 4762 socket cap | 1 × M5 washer ID5.3 OD10 x 1; 1 × M5 DIN 934 plain nut AF8 h4 | Confirm purchased bearing drawing |
| F04 | M20 to inner bearing | 8 | M5 × 20, ISO 4762 socket cap | Tapped metal; no washer | Confirm purchased bearing drawing |
| F05 | M20 metal hub to wheel | 4 | M5 × 45, ISO 4762 socket cap | Tapped metal; no washer | Confirm wheel machining and preload |
| F06 | Four platter quadrants to M20 | 8 | M5 × 16, ISO 7380-1 button | Tapped metal; no washer | Defined geometry |
| F07 | Monolithic worm carrier to M01 | 4 | M5 × 16, ISO 4762 socket cap | 1 × M5 washer ID5.3 OD10 x 1 | Defined geometry |
| F09 | Metal worm bearing retainers to carrier | 8 | M4 × 12, ISO 4762 socket cap | 1 × M4 washer ID4.3 OD9 x 0.8 | Defined geometry |
| F10 | Printed motor bracket to M40 metal riser | 4 | M5 × 20, ISO 4762 socket cap | 1 × M5 washer ID5.3 OD10 x 1 | Defined geometry |
| F11 | NEMA17 face to bracket | 4 | M3 × 10, ISO 4762 socket cap | 1 × M3 washer ID3.2 OD7 x 0.5 | Confirm motor SKU |
| F13 | M40 stepped support to M01 | 2 | M5 × 12, DIN 7991 90-degree countersunk | Tapped metal; no washer | Defined geometry |
| F14 | Integral metal motor support to bench | 2 | M6 × L(T), ISO 4762 socket cap | 1 × M6 washer ID6.6 OD18 x 1.6; 1 × M6 fender washer ID6.6 OD24 x 2; 1 × M6 DIN 985 nyloc nut h6 | Bench thickness required |
| F15 | Fixed housing seam strips | 16 | M4 × 25, ISO 4762 socket cap | 2 × M4 washer ID4.3 OD9 x 0.8; 1 × M4 DIN 985 nyloc nut h5 | Defined geometry |
| F16 | Fixed housing to bench | 4 | M5 × L(T), ISO 4762 socket cap | 2 × M5 DIN 9021 washer ID5.3 OD15 x 1.2; 1 × M5 DIN 985 nyloc nut h5 | Bench thickness required |
| F17 | Motor hood to integral metal support | 4 | M4 × 95, ISO 4762 socket cap | 1 × M4 washer ID4.3 OD9 x 0.8 | Defined geometry |
| F18 | Electronics lid | 10 | M3 × 10, ISO 7380-1 button | 1 × M3 washer ID3.2 OD7 x 0.5; 1 × ruthex RX-M3x5.7 heat-set insert | Defined geometry |
| F19 | Controller tray | 4 | M3 × 10, ISO 7380-1 button | 1 × M3 washer ID3.2 OD7 x 0.5; 1 × ruthex RX-M3x5.7 heat-set insert | Defined geometry |
| F20 | Heat spreader to box floor | 4 | M3 × 16, DIN 7991 90-degree countersunk | 1 × M3 washer ID3.2 OD7 x 0.5; 1 × M3 DIN 985 nyloc nut h4; 1 × EPDM seal washer OD7 ID3.2 x 1 (0.75 compressed); 1 × Metal compression shim OD6.5 ID3.4 x 0.75 | Defined geometry |
| F21 | Electronics feet and box to bench | 4 | M4 × L(T), ISO 4762 socket cap | 1 × M4 washer ID4.3 OD9 x 0.8; 1 × M4 fender washer ID4.3 OD12 x 1; 1 × M4 DIN 985 nyloc nut h5 | Bench thickness required |
| F22 | M50 to steel stand top flanges | 4 | M6 × 25, ISO 4762 socket cap | 2 × M6 washer ID6.6 OD18 x 1.6; 1 × M6 DIN 985 nyloc nut h6 | Defined geometry |
| F23 | Steel stand bottom flanges to bench | 4 | M6 × L(T), ISO 4762 socket cap | 2 × M6 washer ID6.6 OD18 x 1.6; 1 × M6 DIN 985 nyloc nut h6 | Bench thickness required |
| F24 | SO100 base to M50 | 4 | M4 × 35, ISO 4762 socket cap | 2 × M4 washer ID4.3 OD9 x 0.8; 1 × M4 DIN 985 nyloc nut h5 | Verify physical arm foot |
| F25 | Steel home target to M20 | 1 | M3 × 8, DIN 7991 90-degree countersunk | Tapped metal; no washer | Defined geometry |

F08 (separate block bolts) and F12 (printed sensor bracket bolts) are deleted in revision 4; IDs are not reused.

## Other retained hardware

- **H01**: 2 × M8x1 sensor jam nut AF13, thickness <=4 mm. Supplied with selected SICK sensor; modeled at 4 mm.
- **H02**: 1 × Ground steel drive pin nominal diameter 4 x12. M21, matched press fit and tangential slot clearance.
- **H03**: 2 × Metal retainer shim M62, nominal 0.05 mm, select after measurement. Outer-race axial retention; not shaft preload.

## Stack, location and assembly access

**F01 — Core columns: M02 / locating columns / M01.** Head seat 91.6; tip 1.6. Columns72 locate 1 into each plate; visible span 70. Local M01 bosses provide 9 mm full M6 engagement below the locating recess. Clamp the matched metal columns, not the 69.5 mm printed sleeves. Location: (66,0), (-66,0), (36,-58), (-36,-58).

**F02 — Core to bench.** L >= T + 23.6; round up to next available 5 mm. Includes core/spacer 12, washers 3.6, nut 6, two pitches 2. M60 has Ø25 head access openings over Y+64; tighten these before the shaft/bearings are fitted. Nominal head top 19.6 is 0.4 below blocks. Location: X +/-64, Y +/-64.

**F03 — Outer bearing to M02.** Head seat Z99.6; tip 74.6; underside washer 81-82, nut 77-81. 2.4 mm projection. No washer in bearing head counterbore. Fit nuts before enclosing the core. Location: PCD105, phase 22.5 deg.

**F04 — M20 to inner bearing.** Head seat 110, tip 90;15 mm engagement in the bearing reference. M20 has a measured-fit bearing pilot. No head washer. Verify purchased ring tapping and bolt class/torque. Location: PCD65, phase 0 deg.

**F05 — M20 metal hub to wheel.** Seat110; solid metal grip 36 down to wheel face 74; tip 65 gives 9 mm thread engagement and 3 mm blind-bottom clearance. No sleeves or head washers. M21 drive pin supplies positive torque transfer; pilots locate the axes. Final wheel thread capacity and preload require fabricator approval. Location: PCD30 cardinal points.

**F06 — Four platter quadrants to M20.** Seat125; tip 109 gives 7 mm engagement below the Z116 hub face. Button head <=2.75 high in 3 mm recess. No captive nuts or head washers. Do not substitute the old 25 mm screws. Location: ( +/-65, +/-22 ) and ( +/-22, +/-65 ).

**F07 — Monolithic worm carrier to M01.** Seat21, tip 5;7 mm engagement in M01. Four X slots permit +/-3 mm adjustment; the machined tongue/groove controls Y and yaw. No separate bearing-block bolts. Location: Front X +/-52,Y18; rear X +/-70,Y92.

**F09 — Metal worm bearing retainers to carrier.** Cap4 + selected shim nominal 0.05 + washer 0.8 gives 7.15 mm thread engagement. Specify9 mm full M4 thread and 10 mm drilled depth in the carrier. Select shim from measured pocket/bearing/boss stack; do not set shaft preload with the cap screws. No nuts. Location: Both X faces; Y32.5/78.5,Z27/73.

**F10 — Printed motor bracket to M40 metal riser.** Seat21, tip 1;11 mm thread engagement in the integral metal riser/sole. No captive nuts. Tightening is limited by the printed bracket and must be validated on a first article. Location: X116/138,Y32/79.

**F11 — NEMA17 face to bracket.** Bracket6 + washer 0.5; motor thread penetration 3.5. Confirm permissible depth with selected motor. Location: AxisX; Y40/71, Z34.5/65.5.

**F13 — M40 stepped support to M01.** Overall length includes head. Head recessed ~0.2 from underside Z0; tip~12.2, full 8 mm thread in M01. M60 has 1 mm underside tip-relief slots allowing +/-3 axial adjustment. Head diameter <=10; no washer. Install from underside before bench anchoring. Location: X72, Y20/48.

**F14 — Integral metal motor support to bench.** L >= T +23.6. Integral metal support is 12 mm at these holes. No printed clamp stack or compression sleeves. B41-42 top washers counted here once. Location: X220,Y35/77.

**F15 — Fixed housing seam strips.** Strip8 + housing flange 8 =16 grip. Outer washer seats on the new diameter 10 flat at local Y153. Washers1.6 + nut 5 leave 2.4 mm tip projection. Use low clamp force and seal the static seams. Location: Four seams; X +/-6, Z25/90 in each local seam frame.

**F16 — Fixed housing to bench.** L >= T +11.5. Floor2.5, washers 2.4,nut 5,two pitches 1.6. Entire OD15 top washer sits on the floor, clear of the motor passage and curved wall. Location: (88,108) rotated 0/90/180/270 deg.

**F17 — Motor hood to integral metal support.** Seat96.3; tip 1.3;12.2 mm thread engagement below the Z13.5 hard stop. No captive nuts. Cut/deburr100 mm to 95 only if required; keep at least 16 mm threaded tip. Location: X171/225,Y21/91.

**F18 — Electronics lid.** Seat108.5; tip 98.5; insert flush 104 down 98.3, engagement 5.5. 7 mm pilot depth. Fit inserts flush and coupon-check retention. Location: Ten lid points; matching Ø8 access holes in M50.

**F19 — Controller tray.** Seat82.5; tip 72.5. Insert79 down 73.3, engagement 5.7; tip remains 1.5 above pilot floor 71. Location: X +/-65, Y-258/-190.

**F20 — Heat spreader to box floor.** Head diameter <=6, recessed ~0.2 below spreader top 35.75. Tip~19.55, nut 22.75-26.75. Seal washer and metal washer below floor 28; shim above floor 32. Shim M31-34 counted here. Keep screw flush below driver envelope. Location: X +/-55.5, Y-258.5/-189.5.

**F21 — Electronics feet and box to bench.** L >= T + 40.2 (feet 28 + floor 4 + washers 1.8 + nut 5 + two pitches 1.4). Install before electronics; avoid compressing PETG. Location: X +/-75, Y-271/-177.

**F22 — M50 to steel stand top flanges.** Plate8 + flange 4 + washers 3.2 + nut 6; projection 3.8. Head seat 153.6, tip 128.6. Existing B51-54 top washers counted here once. Location: X +/-98,Y-272/-176.

**F23 — Steel stand bottom flanges to bench.** L >= T + 18.2 (flange 4, washers 3.2, backing strip 3, nut 6, two pitches 2). Two shared steel strips 40x136x3 under bench, holes 96 apart. Location: X +/-98, Y-272/-176.

**F24 — SO100 base to M50.** Imported foot 16 + plate 8 + washers 1.6 + nut 5; projection 4.4. Head seat 168.8,tip 133.8. Arm bottom is nowZ152. Verify physical foot and washer seating; internal arm screws excluded. Location: Nonrectangular pattern in arm-mount-reference.json.

**F25 — Steel home target to M20.** Upward screw, head recessed 0.1 atZ99.8; tip 107.8. Target3 mm leaves 5.1 mm engagement into hub boss fromZ102.7. Head diameter <=6. Do not use stainless target material without rechecking sensing range. Location: Radius73, angle 210 deg.

## Bench anchors

T is the measured solid bench-top thickness at each hole. Round each minimum up to the next available length, then verify full nut engagement and underside clearance. A 30 mm top is only an example, not a chosen workbench. Use a rigid, braced table shared by the arm stand and rotary core. Through-bolts and backing hardware do not make a flexible or loose tabletop rigid. Avoid chipboard/loose timber blocks as the assumed precision datum.

| Joint | Quantity | Minimum under-head length | Example only: T=30 |
| --- | ---: | --- | --- |
| Core F02 | 4 M6 | T+23.6 | 55 |
| Motor pod F14 | 2 M6 | T+23.6 | 55 |
| Housing F16 | 4 M5 | T+11.5 | 45 |
| Box F21 | 4 M4 | T+40.2 | 75 |
| Arm stand F23 | 4 M6 | T+18.2 | 50 |

Two 40 × 136 × 3 steel backing strips go below the stand flanges. Each has two Ø6.6 holes on its centreline, 96 apart and 20 from the ends. The separate STEP is at a manufacturing origin, not positioned under an assumed bench. Add suitable backing under other anchors if the chosen top needs it and add that thickness to their formula.

## Still to finish before ordering all hardware

- **Workholding:** Four blind M6 metal threads start atZ121 with 9 mm full thread. Require8–9 mm engagement: bolt length minus fixture/washer stack aboveZ128 must be 15–16 mm. Example M6x20 requires 4–5 mm upper stack. Verify every actual clamp; never force a screw against a blind bottom. No M6 captive nuts remain.
- **Worm shaft retention:** Key sizes, shaft shoulders, bearing preload locknut(s), spacers and retaining screws require a finished shaft drawing; quantity/length unknown.
- **Coupling:** Clamping screws supplied with selected coupling; quantity and torque unknown until SKU is selected.
- **Home sensor:** Mechanical reference SICK IME08-02BPSZT0S, M8x1, two AF13 nuts and F25 retained mild-steel target. Select mating cordset, confirm supplied nut thickness <=4 mm, set gap 1.2 mm, and test one home transition per revolution. PNP output needs a compatible input interface.
- **Driver / controller:** Board mounting screw and standoff patterns unselected. The 14 lid/tray screws do not fasten the boards.
- **Heat sink:** B27 represents thermal adhesive pad, not verified structural retention. Select rated adhesive or mechanical retention and any fasteners with final heat sink.
- **Optional encoder / external devices:** Encoder mounting, PSU, E-stop and cable clamps depend on selected devices. Not included in fixed quantities.
- **Stand fabrication:** Two side channels and front brace are welded, not screwed together. Fabricator must specify weld size/process, finish datums and inspect distortion. No unlisted hidden frame screws.

## Totals and sources

[Machine-readable joint records](../cad/fasteners.json) and [consolidated purchasing CSV](../cad/fastener-shopping-list.csv) are generated by `scripts/build_fastener_register.py`. Quantities are installed counts, with no spares. Existing model washers B41–42/B51–54 and compression shims M31–34 are counted once. The CSV retains conditional screw quantities and separates thickness-dependent bench bolts.

- [ruthex RX-M3x5.7](https://www.ruthex.de/products/ruthex-gewindeeinsatz-m3-100-stuck-rx-m3x5-7-messing-gewindebuchsen): selected insert size; nominal Ø4 pilot, coupon verification required.
- [Accu DIN7991 M3 dimensions](https://www.accu.co.uk/api/product-datasheet?id=625698) and [BelMetric DIN7991 M5 drawing](https://belmetric.com/content/A-PDF_Drawings/SF5X10.pdf): head-size limits used in the countersink checks.
- [TR Fastenings cap-screw dimensional catalog](https://www.trfastenings.com/Products/Catalogue/Screws-and-Bolts/news/Hexagon-Socket-Screws/Cap-Head/Cart/TR00005910-299): ISO4762/DIN912, 95 mm is non-preferred.
- [Universal Robots stand guidance](https://www.universal-robots.com/manuals/EN/HTML/SW5_24/Content/prod-usr-man/complianceUR8Long/H_g5_sections/mechanical_interface_g5/dimension_stand.htm): moving/stopping torques act on the stand. This supports the braced/anchored load path; UR load ratings are not applied to the SO100.
