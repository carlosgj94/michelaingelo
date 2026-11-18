# Rotary table specification — RT-01 revision 5

2026-11-18. **Foam prototype for review. Fabrication release is pending.** The [current audit response](../rotary-table-design-audit-2026-11-18.md#revision-5-response-for-review) records the service, fastening and seal changes. The [previous response](../rotary-table-audit-response-2026-11-17.md) records the earlier precision-core changes.

## 1. Scope and architecture

A 320 mm horizontal platter rotates about vertical Z. The existing SO100 mounts to a fixed, bench-anchored steel stand above the controller box. M50 supports the arm at Z152. Its four top-down mounting screws have recessed tips to clear the driver during withdrawal. The steel stand transfers the arm load to the bench independently of the enclosure.

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

The column pattern is a bolted metal joint. Check the −Y row's hold-down and the bearing-seat bending under the +Y eccentric load. At the 58 mm row spacing, 10.85 N·m corresponds to opposing ±187 N reaction increments at the two rows in the simple screening model. Verify preload and no slip/separation under load, then measure M02 relative to M01 and the tool relative to the fixture. Include both horizontal axes and the actual stand and bench. Record transient peak and settling before changing plate thickness or arm height.

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

Load the rim, quadrant centres and both sides of each seam during the printed-deck test. Measure differential height and local vertical displacement in addition to the specified tangential deflection. The fixture design must account for the 7 mm printed layer above each metal boss. Define a hard clamp load path, anti-rotation and restraint for the intended workpiece before rock trials. The cosmetic column sleeves need free clearance from the metal clamp stack. Inspect them for movement and fretting during the prototype test.

Four fixture points at (±47,±47) now use **blind M6 metal threads** in Ø16 raised bosses. Boss face Z121, 9 mm full thread to Z112, tap-drill cylinder to Z110, drill tip Z108.5. At least 2.5 mm metal remains above the Z106 underside. Platter pockets clear the bosses at nominal Ø16.30. Do not reintroduce through-holes or captive nuts.

Require **8–9 mm actual screw engagement**. Under-head bolt length minus the fixture and washer stack above Z128 must equal **15–16 mm**. For the first foam fixture, the 3.0 mm base and 1.6 mm metal washers give 8.4 mm nominal engagement with M6 × 20 screws. Tip Z112.6 is inside the full-depth threads. Confirm printed thickness before tightening and seal unused fixture holes. [Fixture installation](../rotary-table-printing.md#prototype-foam-fixture)

The prototype fixture locates a **50 × 50 × 40 mm** rigid foam blank against two padded datums. Two adjustable jaws resist rotation and a tied top keeper restrains lift. The proposed upper working zone is **30 × 30 × 20 mm**. The base clamps through the 7 mm printed layer. Verify the light-load preload and printed creep before cutting and test the complete tool and cable path once the spindle is chosen.

## 5. Drive and home sensor

The KHK wheel envelope is Ø86, toothed face Z41–59, hub Z59–74, nominal bore 15. The worm envelope is Ø35, tooth length 36 and hub length 14. It needs supplier-approved finish boring/keying from the catalog bore 14 to the proposed shaft 15. These are purchased tooth envelopes, not printable gears or a meshing simulation. Buy the specified duplex pair together; follow KHK arrow/reference-tooth alignment, axial adjustment and lubrication instructions.

M60's integral blocks eliminate F08 completely. F09 is eight M4×12 screws into metal, nominal 7.15 engagement; require ≥9 full thread and 10 drilled depth. The two 15×35×11 angular-contact bearing references sit at X±60.45. Select an opposed/preload-suitable pair and finish the shaft drawing with positive worm torque transfer and axial retention of both inner rings. Adjust the carrier ±3 along X, then measure running torque over a revolution. Mark the carrier and check its X position after reversing under load.

M40 now combines the 4 mm sole and 8 mm riser in metal. F14 bench bolts clamp metal directly. Old P23 and motor anchor sleeves are removed. P24 remains a printed motor bracket: verify its horizontal holes, pilot and clamp retention on a first article. Motor face is X130; 40 mm coupling envelope spans X78–118. Shaft-end gap is nominal 7 mm, minimum 4 at +3 cartridge shift. Select the coupling's actual insertion depth, clamps and flexible alignment limits.

Home sensor mechanical reference: **SICK IME08-02BPSZT0S, 1040870**, M8×1, 50 long with 34 threaded length, PNP normally open, 10–30 VDC. It mounts axially through M02 at **R73, 210°**, face Z98.5. A local Ø18 metal pad supports two AF13 nuts modeled conservatively 4 mm thick; confirm the supplied thickness. The cable/connector reservation extends below the body; select the M8 cordset and check its actual bend radius.

A mild-steel Ø12×3 target at Z99.7–102.7 is retained with upward F25 M3×8 in the hub boss. Head is recessed 0.1, hub engagement 5.1. Nominal face gap is **1.2 mm**; adjust/test throughout 0.9–1.5 under actual runout and load. Supplier safe sensing distance is 1.62 for the specified standard target. The disc surrounds an 8×8 target square, but its countersink and the assembled background still require a real signal test. Ordinary hub background is 7.5 above the sensing face. Bearing OD is 9 mm from the sensing-face edge; the layout conservatively allows the drawing's 8 mm lateral and 6 mm overhead restrictions. Verify exactly one home event per revolution. Homing is not output-angle feedback. Only the selected sensor has a published IP67 rating; the machine does not.

### Foam-trial drive alternative

KHK's **SWG2-R1 and AG2-40R1** are a matched right-hand, module 2 pair with one worm start, 40 wheel teeth and a 55.5 mm centre distance. The worm drawing gives a Ø31 pitch diameter, Ø35 outside diameter, 32 mm tooth face and 50 mm overall length. The wheel has a Ø80 pitch diameter, Ø86 maximum outside diameter and a 33 mm H4 body with an 18 mm aluminium bronze tooth face and an FC200 cast-iron hub. The existing shaft axis at Y55.5/Z50 and M20 wheel seat at Z74 can carry those envelopes. [Catalogue](https://khkgears.net/pdf/2025/worm-gears.pdf) · [Editable gear layout](../../exports/rotary-table/drive-study/swg2-r1-ag2-40r1-layout.sc)

Both stock bores are Ø12. The fit model clears the retained assembly and fasteners after enlarging the worm bore to Ø15, using a Ø11.98 nominal wheel pilot and adding the F05 and M21 features in the wheel boss. The conservative wheel sweep clears the fixed carrier by 4.44 mm. Match the actual H7 wheel bore with 0.010–0.025 mm diametral pilot clearance and check concentricity to the bearing pilot. Keep all machining away from the induction-hardened worm teeth and roots. Ø15 equals 60% of the Ø25 worm hub and is at the upper end of KHK's general keyed-bore guidance. Approval of the finished bore, key, wheel machining and shaft shoulder/retention stack remains a gate. [Envelope checks](../audit-evidence/2026-11-18-rt01/prototype-fit/prototype-worm-fit.results.json)

The alternative uses standard ground gearing. Axial carrier travel can centre the worm on the wheel face. Backlash is set by the actual pair and assembly and needs a full-turn check under load. KHK's 0.06–0.16 mm catalog backlash converts to 0.086–0.229° at the wheel pitch radius of 40 mm. The main duplex design retains its adjustable mesh for the 0.10° reversal target. KHK lists 64.0 N·m wheel torque at 100 rpm worm speed for the AG pair. That figure covers the gears. Keep the assembled torque, lubrication, duty, reversal and running-temperature checks.

SKF **7202 BEGAP** fits the nominal Ø15 × Ø35 × 11 window. Its two opposed bearings need a finished shaft stack. The datasheet calls for an inner-ring abutment diameter of at least 19.2 mm. The current Ø15.3 carrier throat and Ø16 cap shaft holes need checking against the real abutments, spacers and installation sequence before the carrier and caps are machined. Finish outer-ring contacts and preload for the selected arrangement. [SKF datasheet](https://docs.rs-online.com/17e8/A700000013821028.pdf)

## 6. Electronics, stand and service

P50/P52 enclosure is 168×112×80 including lid, at Z28–108 on four 28 mm feet. The F21 anchor heads and fender washers are below the bench. Inside P50, each printed nut trap holds an AF7 nut above a sealed washer stack. Check trap torque retention and seal compression on the coupon and first article.

Reserve **118 × 80 × 35 mm** for the driver at Z36–71 and **118 × 70 × 20 mm** for the controller on the removable tray. These checked boxes include any rigid connectors that stay attached during removal. The controller box has 2 mm nominal overhead clearance with the lid on, 3.16 mm minimum in the lift and 5 mm in rear withdrawal. The cyan bodies in revision 5 record the earlier 118 × 76 × 35 and 80 × 55 × 20 examples. [Device envelope checks](../audit-evidence/2026-11-18-rt01/prototype-fit/electronics-space.results.json)

M30 is a 118×76×3 aluminium spreader. B27 is the 0.5 mm thermal pad below M30. The driver-side 0.25 mm nominal allowance requires a selected thermal interface and measured contact pressure. Design positive heat-sink retention, board mounts and cable restraints around the selected parts, then verify service, stop and isolation behaviour and closed-lid temperature at intended duty. Use an external enclosed 24 V supply matched to the final drive.

M50 underside is Z144, 40 mm above the open rim and 36 mm above the closed lid. The 144 mm steel channels have 4 mm webs and 28×116×4 flanges. The front brace is 228×136×4 at Z4–140. Weld, inspect distortion and finish the upper datum. Size welds and anchors for actual reactions. Bolt the stand and core to the same rigid braced bench. Use measured thickness T in the anchor formulas. Install the two 40×136×3 backing strips with their Ø16 scallops toward the box and verify the F21 and F23 washer seats.

F24 uses four M4×0.7-6H through threads in M50. The four prototype P55 seats match the imported foot contours and give the Ø9 washers a flat support. Require 6.5–7.0 mm screw penetration, at least 6.0 mm effective full engagement and tip Z≥145 after fitting. Inspect the real contact imprint and torque/preload retention before powered trials. [Seat fitting](../rotary-table-printing.md#prototype-arm-seats)

For service, release cables and thermal attachments, then withdraw the lid and tray as in the assembly guide. Lift the full driver 70.5 mm to Z106.5–141.5 and slide it rearward 140 mm. The hardware-aware CAD check covers both translating segments. Nominal withdrawal margins are 2.5 mm at the rim and M50. The lift has 1 mm nominal side clearance at the tray posts. Gauge the actual route with the selected device and handling provisions. Arm, tool, workpiece and moving cable clearance require a separate articulated workspace study.

## 7. Covers, dust and splash control

Retain the overlapping rotating skirt, fixed upstand and external gutter: nominal 2 mm radial skirt gap and 2 mm deck/upstand gap. Rotating ribs end inside R146.2 versus wall R150; ribs start Z98 above seam structures ending Z96. The hub flange stays 1 mm above the stationary bearing envelope. Lowest target is Z99.7 versus column cap-head top 97.6, nominal 2.1; other hub bosses are higher. These are continuous geometric bounds, not allowances already proven under distortion/load.

Housing anchors move to (88, 108) rotated by quadrant. Their OD15 washer footprint is supported: minimum nominal wall gap 3.19, and 3.0 from the motor-foundation opening at the closest edge. F15 seam washers seat on new Ø10 flat pockets at local Y153/X153, retaining 16 mm grip and the M4×25 stack. Remaining outer wall below the pocket is nominally at least 3.0 mm in the washer footprint. Use low clamp force and seal every seam.

Apply removable compatible RTV continuously through the seams. The platter seams are inside the peripheral labyrinth. Verify seal continuity and clear squeeze-out from the swept envelope. The four drain bores discharge through notches in the lower flange. Place one removable cup at each outlet, with its raised inlet below the bore and its pour lip pointing radially outward. Verify placement and removal on the actual bench. Test the gutter, inlet and collection path for pooling, clogging and clean-out access. [Drain catch installation](../rotary-table-printing.md#drain-catches)

Core and hood use 2 mm EPDM at 1.5 mm installed thickness. Cut the lid ring from 2 mm EPDM sheet with a 2 mm ring width. Its 3.5×1.5 mm groove has 76.19% nominal volume fill. Approve the compound, squeeze and worst-case gland fill with tolerances and swell. For the spreader use 1 mm gasket compressed to 0.75 mm. Seal the F21 and F20 penetrations and fit sized glands or blanking plugs. Inspect gland lands, gaskets and printed porosity with unpowered tracer and witness media. Use the BOM for uncompressed cut sizes.

## 8. Printing and acceptance gates

A1 Mini baseline: 180³ volume, 0.4 nozzle, 0.20 layers, dry PETG. Maximum assembly-part dimension 168; 5 mm brim each side gives 178. Check purge lines/support expansion in the slicer. Use the [printing guide](../rotary-table-printing.md), revised coupon and full-size first articles. Never scale the whole part to correct a fit.

Printed holes use separate vertical/horizontal parameters; metal fits use the inspection table above. Main walls are 4, housing floor 2.5. Start load-carrying printed parts at six walls/eight top-bottom layers/35–45% infill; covers at four walls/20–25%. These are process starting points, not strength ratings. No printed threads are used for durable joints. Actual torque must respect PETG creep and insert pull-out.

CAD acceptance includes 81 closed table/support bodies, constrained sketches, the 23 fastener groups through rotation and carrier travel, service with retained hardware, supported anchor footprints, and 25 oriented STLs plus the coupon. Check named source, native and STEP geometry together. See [validation](../rotary-table-validation.md) for the checks and their limits.

Physical release still requires final bearing and drive drawings, pin/wheel strength and preload approval, actual devices and cables, fixture qualification, bench thickness and weld review, sliced/printed fit calibration, full travel and hand rotation, sensor signal testing, progressive loads and stopping, reversal, runout, stiffness, temperature and dust/splash tests. The audit’s ideal-contact stand simulation is a screening comparison. Revision 5 has no structural rerun or physical print or carving qualification.

## Sources

- [KHK duplex catalog](https://khkgears.net/pdf/agdl.pdf): selected pair, dimensions and adjustment restrictions.
- [THK RU dimensional table](https://tech.thk.com/en/products/pdfs/en_a18_022.pdf): RU85 dimensions and mounting-hole reference. Obtain the final variant drawing.
- [SICK IME08-02BPSZT0S datasheet](https://www.sick.com/media/pdf/6/86/386/dataSheet_IME08-02BPSZT0S_1040870_en.pdf): dimensions, safe sensing range, installation and electrical requirements. Nut thickness is not specified; 4 mm here is a conservative allowance to confirm.
- [Bambu A1 Mini technical specification](https://store.bblcdn.com/1531c9726f6b41fba4594d5b47966ee0.pdf): printer envelope/nozzle.

Other tolerances and acceptance targets are project choices, not attributed supplier guarantees.
