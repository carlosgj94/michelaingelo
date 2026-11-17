# Rotary table specification — RT-01 revision 4

2026-11-17. **Prototype for review; not fabrication released.** The [audit response](../rotary-table-audit-response-2026-11-17.md) records each finding, decision, evidence and remaining acceptance test. The original [revision 3 specification](../archive/rotary-table-spec-rev3.md) is historical. This document governs the current geometry.

## 1. Scope and architecture

A 320 mm horizontal platter rotates about vertical Z. The existing SO100 stays on a fixed, bench-anchored steel stand above the controller box. The arm's imported geometry and relative pose are preserved; revision 4 raises the whole arm and its mounting plate by 8 mm for driver removal. Neither the printed enclosure nor its lid carries arm load.

The user approved printed parts with a metal core. Audit fixes expand that core: a machined output hub, one-piece worm-bearing carrier, metal retainer caps and integral motor foundation replace the corresponding printed precision/clamp interfaces. There are **25 printed assembly pieces**, 17 metal fabrication bodies and purchased/reference parts. The aluminium/steel parts require machining or fabrication; this is no longer a two-plate-only metal kit. Scaling preserves the load path and drive arrangement, then requires new sizing; it is not uniform CAD scaling.

Workpiece load path: fixture → printed platter/metal fixture bosses → M20 metal hub → inner bearing ring → outer ring → M02 seat → four locating steel columns → M01 base → rigid bench. Motor torque path: motor → coupling → supported worm shaft → duplex worm/wheel → metal face joint and M21 drive pin → hub → platter. No belt or assumption of worm self-locking.

## 2. Baseline and performance targets

| Item | Requirement / nominal geometry |
| --- | --- |
| Platter | Ø320, four 12 mm thick ribbed sections; deck Z116–128 |
| Housing | Ø308 main wall, Ø328 gutter; indirect splash labyrinth |
| M01 | 164 × 184 × 8 aluminium base at Z4–12; local lower thread bosses and upper guide tongue |
| M02 | Ø156 / Ø94 × 8 seat at Z82–90; interrupted bearing register and sensor nut pad |
| Bearing reference | RU85 size, Ø55 / Ø120 × 15, Z90–105; actual preload/seal variant must be selected |
| Columns | Four Ø10 / Ø6.2 × 72 steel columns, Z11–83; 1 mm recess in each plate, 70 mm exposed span |
| Printed column sleeves | Ø22 / nominal Ø10.30 × 69.5, Z12–81.5; nominal 0.5 mm clamp relief |
| M20 | Ø150 × 10 flange at Z106–116, Ø76 bearing face at Z105, registered neck/wheel pilot, four raised fixture bosses to Z121 |
| Worm axis | X direction; Y55.500, Z50.000; wheel axis Z through X0/Y0 |
| Gear pair | KHK KWGDL2-R1 + AGDL2-40R1, module 2, RH, 40:1, centre distance 55.5 |
| Motor provision | Closed-loop NEMA17; face X130, 42.3 square, rear length ≤80 plus 20 cable space; 5 mm shaft |
| Arm plate / stand | M50 228 × 116 × 8 at Z144–152; two 144 mm high welded steel channels and front brace |
| Workpiece + fixture target | ≤5 kg initially foam; offset ≤80 mm; cutting height ≤150 above table |
| Cutting-force assumption | 10 N at R160; 1.60 N·m tangential torque before friction/acceleration |
| Speed / acceleration | Initial 0.1–2 rpm; ≤0.2 rad/s² subject to commissioning |
| Torque target | ≥4 N·m continuous / ≥8 N·m brief peak after friction; not inferred from motor holding torque |
| Reversal error | ≤0.10° at the platter; aspirational ≤0.05° after adjustment |
| Runout / stiffness | ≤0.20 mm axial TIR at R140; ≤0.20 mm tangential deflection at R140 under 10 N, both directions |
| Environment | Fine dust and incidental splashes; no machine IP rating, immersion or hose-washing claim |

All performance rows are **acceptance targets, not measured results**. Payload moment is 5 × 9.81 × 0.08 = 3.924 N·m; the lateral force adds 1.50 N·m. An initial factor of two gives 10.85 N·m overturning before additional real arm/tool/fixture loads. Measure rotating inertia and friction before final drive selection. Stand bracing does not smooth the purchased arm's commands or remove its internal backlash.

## 3. Metal location, machining and inspection

Dimensions below are project inspection requirements, **not manufacturer-approved fits**. Obtain the actual bearing/gear drawings first; final shop drawings must state material, GD&T, roughness, threads, corner relief and permissible preload. Nominal STEP geometry does not encode these tolerances. Inspect near 20 °C, then verify at the maximum intended operating temperature.

| Interface | Geometry and acceptance requirement |
| --- | --- |
| Base datums | M01 top is datum A; bearing axis is datum B; carrier guide establishes X direction. Base flatness ≤0.05; M02 bearing seating land ≤0.03, or tighter supplier requirement. Finish mating datums after fabrication/coating. |
| Columns and plate location | Ground, square ends, 72.000 nominal, matched within 0.01. One Ø10.02 round recess at (66, 0), one 10.52 × 10.02 X slot at (−66, 0); other recesses Ø10.4. Finish locating clearance to 0.015–0.020 diametral against measured columns. Round/slot references in both plates prevent using screw clearance as the XY datum. Recess depths 1.000 nominal; verify the assembled 70 mm separation and parallelism. |
| Outer bearing on M02 | Four interrupted pads, effective locating diameter Ø120.02, relieved Ø121.6 for the lower corner. Finish to measured ring OD +0.010–0.030. The seating plane carries load, not the corner radius. Confirm actual chamfer/seal envelope. |
| Inner bearing on M20 | Ø54.98 pilot at Z90–104, Ø53.5 relief at the shoulder. Finish pilot to measured bearing bore minus 0.020–0.030 diametral. Wheel pilot and bearing pilot total indicated concentricity ≤0.01; flange face runout ≤0.02 to the pilot datum. |
| Wheel on M20 | Ø14.98 × 7 nominal pilot; finish to measured wheel bore minus 0.010–0.025 diametral. Relief Ø14.5 × 0.5 at the shoulder. Inspect wheel bore/tooth datum runout after secondary machining; target ≤0.03 radial TIR before setting mesh. |
| M60 guide | Integral M01 tongue 60 × 6 × 2; groove 68 × 6.02 × 2.2. Finish measured side clearance to 0.010–0.020 total, straight/parallel to worm X axis within 0.01 over 60. At ±3 travel, ≥1 mm end clearance remains. Tighten F07 after adjustment. |
| Worm-bearing seats | Both Ø35.01 × 11.05 deep in one setup in M60; finish to measured outer rings +0.005–0.015 diametral. Coaxiality ≤0.015; shoulder perpendicularity ≤0.01. Verify the supplier permits this retained clearance fit for the selected load arrangement. |
| Assembled worm location | Measure centre distance 55.500 ±0.030, worm height relative to wheel tooth midplane ±0.030 and axis squareness ≤0.02 over 100. These are assembled acceptance limits, not independent tolerances to add blindly. Correct/rework datums if the stack fails; X adjustment cannot repair Y/Z misalignment. |
| Bearing caps | M61 is 4 mm metal with a 0.10 annular outer-race boss, Ø34.9 outside / Ø28 inside, shaft hole Ø16. Confirm the annulus contacts only the real outer race. M62 shim nominal 0.05, selected after measurement. |

For each cap, axial outer-ring clearance is **pocket depth − bearing width + shim thickness − boss height**. Nominally 11.05 − 11 + 0.05 − 0.10 = 0. Select/lap shims for 0–0.005 mm clearance without distorting the outer ring; use blue/contact and indicator checks. This controls outer-ring retention only. Shaft shoulders, spacers and locknuts must separately define the angular-contact pair's inner-ring retention/preload. That shaft drawing remains a fabrication gate.

The radial location budget is an inspection chain: bearing/pilot clearance, pilot concentricity, column location, guide clearance, bearing-seat alignment and thermal expansion all contribute. Passing each nominal CAD feature is insufficient; accept the assembled centre distance, wheel TIR and running torque through 360°. The small metal fits above are not PETG print allowances.

## 4. Wheel attachment and workholding

M20 is 6061-T6 aluminium. Four F05 M5×45 cap screws clamp a **solid 36 mm metal grip** into the wheel, with 9 mm nominal thread engagement. The old equal-length printed stack and four hub compression sleeves are removed. Specify wheel material, tap depth, thread capacity, bolt preload and an anti-loosening method with the fabricator; do not choose torque from the screw diameter alone.

M21 is a ground hardened-steel Ø4×12 drive pin at R15/45°. It presses 6.5 mm into M20 and projects 5.5 into a 6.2 mm deep **radial slot** in the wheel. Match press interference to 0.005–0.012 mm and total tangential slot clearance to 0.005–0.010. The radial slot avoids competing with the concentric pilot; bottom clearance is 0.7 mm. The pin provides a positive torque path; the bolts keep the faces seated.

At 8 N·m, pin tangential force is 533 N, average single-shear stress 42.4 MPa, and average wheel-slot bearing stress 24.2 MPa over the 5.5 mm engagement. A deliberately conservative tip-load bending estimate is 467 MPa (about 473 MPa combined with shear); require certified pin yield/proof strength ≥1000 MPa for an initial factor >2 on that estimate, and review fatigue/contact/fit with the supplier. These calculations are demands and preliminary sizing, not a validated pin rating. Maximum geometric slot contribution is 0.010/15 radians = **0.0382°**; bearing, mesh, shaft, printed platter and bolted-joint errors remain separate. Check reversal under load, temperature and repeated cycling.

Eight F06 M5×16 button screws attach platter quadrants into M20, with 7 mm metal engagement. The deck remains printed and its creep/deflection must be tested.

Four fixture points at (±47,±47) now use **blind M6 metal threads** in Ø16 raised bosses. Boss face Z121, 9 mm full thread to Z112, tap-drill cylinder to Z110, drill tip Z108.5. At least 2.5 mm metal remains above the Z106 underside. Platter pockets clear the bosses at nominal Ø16.30. Do not reintroduce through-holes or captive nuts.

Require **8–9 mm actual screw engagement**: under-head bolt length minus fixture/washer stack above Z128 must equal **15–16 mm**. Example: M6×20 requires a 4–5 mm upper stack. Never force a bolt against a blind bottom. Four maximum-depth screw tips are included in rotation checks; actual clamps, workpiece, seal washers and their upper collision envelope are not yet designed. Seal unused fixture holes.

## 5. Drive and home sensor

The KHK wheel envelope is Ø86, toothed face Z41–59, hub Z59–74, nominal bore 15. The worm envelope is Ø35, tooth length 36 and hub length 14. It needs supplier-approved finish boring/keying from the catalog bore 14 to the proposed shaft 15. These are purchased tooth envelopes, not printable gears or a meshing simulation. Buy the specified duplex pair together; follow KHK arrow/reference-tooth alignment, axial adjustment and lubrication instructions.

M60's integral blocks eliminate F08 completely. F09 is eight M4×12 screws into metal, nominal 7.15 engagement; require ≥9 full thread and 10 drilled depth. The two 15×35×11 angular-contact bearing references sit at X±60.45. Select an opposed/preload-suitable pair and finish the shaft/retention drawing. Adjust the carrier ±3 along X, then measure running torque at every angle; do not preload to binding.

M40 now combines the 4 mm sole and 8 mm riser in metal. F14 bench bolts clamp metal directly. Old P23 and motor anchor sleeves are removed. P24 remains a printed motor bracket: verify its horizontal holes, pilot and clamp retention on a first article. Motor face is X130; 40 mm coupling envelope spans X78–118. Shaft-end gap is nominal 7 mm, minimum 4 at +3 cartridge shift. Select the coupling's actual insertion depth, clamps and flexible alignment limits.

Home sensor mechanical reference: **SICK IME08-02BPSZT0S, 1040870**, M8×1, 50 long with 34 threaded length, PNP normally open, 10–30 VDC. It mounts axially through M02 at **R73, 210°**, face Z98.5. A local Ø18 metal pad supports two AF13 nuts modeled conservatively 4 mm thick; confirm the supplied thickness. The cable/connector reservation extends below the body; select the M8 cordset and check its actual bend radius.

A mild-steel Ø12×3 target at Z99.7–102.7 is retained with upward F25 M3×8 in the hub boss. Head is recessed 0.1, hub engagement 5.1. Nominal face gap is **1.2 mm**; adjust/test throughout 0.9–1.5 under actual runout and load. Supplier safe sensing distance is 1.62 for the specified standard target. The disc surrounds an 8×8 target square, but its countersink and the assembled background still require a real signal test. Ordinary hub background is 7.5 above the sensing face. Bearing OD is 9 mm from the sensing-face edge; the layout conservatively allows the drawing's 8 mm lateral and 6 mm overhead restrictions. Verify exactly one home event per revolution. Homing is not output-angle feedback. Only the selected sensor has a published IP67 rating; the machine does not.

## 6. Electronics, stand and service

P50/P52 enclosure is 168×112×80 including lid, at Z28–108 on four 28 mm feet. Reserve driver 118×76×35 at Z36–71 and controller 80×55×20 on the removable tray. M30 is a 118×76×3 aluminium spreader; external heat sink envelope 98×54×18 with a 0.5 thermal pad. Driver attachment/contact, heat-sink retention, board standoffs and wiring are unselected; an adhesive-pad envelope is not a retention design. Use an external enclosed 24 V supply, matched to the final motor/drive; keep mains outside this box. Validate temperature with the lid closed at maximum intended duty.

M50 underside is Z144: **40 mm above the open box rim and 36 above the closed lid**. Steel side channels are 144 high, 116 deep, with 4 mm webs and 28×116×4 top/bottom flanges; front brace is 228×136×4 at Z4–140. Weld, inspect distortion and finish the upper mounting datum. Review weld size and real arm/tool reactions before fabrication. Through-bolt stand and core to the **same rigid braced bench**; a loose timber block is not the mounting basis. Bench thickness T is unknown, so anchor lengths remain formulas in the register. Two separate 40×136×3 backing strips go beneath the stand.

Service with the arm plate installed: disconnect power/cables and release the selected device attachment; remove lid screws through the ten Ø8 tool holes; lift lid/gasket8 and slide rearward 140. Release tray screws, lift tray/controller27 and slide rearward 140. Lift the full driver 70 to Z106–141, then slide rearward 140. Its route leaves 2 mm above the rim and 3 below M50. The model proves the bare envelope route; connectors, service loops and thermal-pad separation must be demonstrated with actual electronics. Arm travel and spindle/workpiece collisions require a separate articulated workspace study.

## 7. Covers, dust and splash control

Retain the overlapping rotating skirt, fixed upstand and external gutter: nominal 2 mm radial skirt gap and 2 mm deck/upstand gap. Rotating ribs end inside R146.2 versus wall R150; ribs start Z98 above seam structures ending Z96. The hub flange stays 1 mm above the stationary bearing envelope. Lowest target is Z99.7 versus column cap-head top 97.6, nominal 2.1; other hub bosses are higher. These are continuous geometric bounds, not allowances already proven under distortion/load.

Housing anchors move to (88, 108) rotated by quadrant. Their OD15 washer footprint is supported: minimum nominal wall gap 3.19, and 3.0 from the motor-foundation opening at the closest edge. F15 seam washers seat on new Ø10 flat pockets at local Y153/X153, retaining 16 mm grip and the M4×25 stack. Remaining outer wall below the pocket is nominally at least 3.0 mm in the washer footprint. Use low clamp force and seal every seam.

Static seams use removable compatible RTV. Core/hood/lid gaskets are 2 mm EPDM, installed 1.5; spreader gasket is 1, installed 0.75 against metal stops. Cover bolts and glands need sealed penetrations. Cut gasket stock at uncompressed thickness, not STEP thickness. Check drainage, curved hood transition, gland lands, porosity and seals with unpowered absorbent indicators before installing electronics. No certified water/dust rating follows from these features.

## 8. Printing and acceptance gates

A1 Mini baseline: 180³ volume, 0.4 nozzle, 0.20 layers, dry PETG. Maximum assembly-part dimension 168; 5 mm brim each side gives 178. Check purge lines/support expansion in the slicer. Use the [printing guide](../rotary-table-printing.md), revised coupon and full-size first articles. Never scale the whole part to correct a fit.

Printed holes use separate vertical/horizontal parameters; metal fits use the inspection table above. Main walls are 4, housing floor 2.5. Start load-carrying printed parts at six walls/eight top-bottom layers/35–45% infill; covers at four walls/20–25%. These are process starting points, not strength ratings. No printed threads are used for durable joints. Actual torque must respect PETG creep and insert pull-out.

CAD acceptance: 81 new bodies closed; no failed features; constrained sketches; all 23 active fastener groups represented; 17 unique uniform angles plus targeted narrow crossings and closure; ±3 carrier adjustment; service sequence; analytical sweep bounds; 25 oriented STLs/coupon; source/native/STEP agreement. Exclude only documented thread/press-fit contacts, purchased tooth blanks and unchanged imported arm self-contact. See [validation](../rotary-table-validation.md).

Physical release still requires: final bearing and drive drawings, pin/wheel strength and preload approval, actual devices/cables, fixture design, bench T and weld review, sliced/printed fit calibration, full travel/hand-rotation test, sensor signal test, progressive loads/stopping, reversal/runout/stiffness/temperature and dust/splash tests. No FEA, physical print, carving or stone-machining qualification is implied.

## Sources

- [KHK duplex catalog](https://khkgears.net/pdf/agdl.pdf): selected pair, dimensions and adjustment restrictions.
- [THK RU dimensional table](https://tech.thk.com/en/products/pdfs/en_a18_022.pdf): RU85 dimensions and mounting-hole reference. Obtain the final variant drawing.
- [SICK IME08-02BPSZT0S datasheet](https://www.sick.com/media/pdf/6/86/386/dataSheet_IME08-02BPSZT0S_1040870_en.pdf): dimensions, safe sensing range, installation and electrical requirements. Nut thickness is not specified; 4 mm here is a conservative allowance to confirm.
- [Bambu A1 Mini technical specification](https://store.bblcdn.com/1531c9726f6b41fba4594d5b47966ee0.pdf): printer envelope/nozzle.

Other tolerances and acceptance targets are project choices, not attributed supplier guarantees.
