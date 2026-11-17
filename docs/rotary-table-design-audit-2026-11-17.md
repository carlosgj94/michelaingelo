# RT-01 independent design audit — 2026-11-17

> **Revision 4 implementation update:** This document preserves the original audit of revision 3 (`a403195`). Each finding has now been checked and addressed in the revised CAD/source/exports. Read the [finding-by-finding response](rotary-table-audit-response-2026-11-17.md) and [current validation](rotary-table-validation.md) before interpreting the original disposition below. Physical qualification and explicitly unfinished interfaces remain open. Original line-number references and probes refer to the baseline commit, not the revised source.

**Disposition: resolve the two confirmed assembly blockers before printing the complete assembly or releasing metal fabrication.** The nominal assembly is coherent, and its print meshes fit the A1 Mini, but the current fastener schedule cannot be assembled as drawn. Several locating and torque-transfer interfaces also lack the tolerances needed to support the stated precision targets.

This is an audit only. No existing CAD, generator, export, BOM, assembly guide, or validation file was edited. Recommendations below are proposed work, not implemented changes.

## Scope and evidence

Reviewed the current `michelaingelo.sc`, the RT-01 generators and generated commands, all current mechanical documents, the fastener register, print manifest, oriented STLs, packaged files, and assembly illustrations. The reviewed native file has SHA-256 `fc5b4c1079a4e5d9955af6266879d54597708b663fdfc605825a25b65dd6eb23`. The same file is present in commit `a403195` at audit completion. All 11 hashes recorded in the existing validation results matched the current files.

Independent checks used disposable headless SolidCraft models with the current native assembly as input and **without `--save`**. Conservative hardware probes were added only in memory. Measurements and probe scripts are retained in [the audit evidence folder](audit-evidence/2026-11-17-rt01/summary.json). Findings distinguish:

- **Confirmed:** a source/document mismatch, measured geometry, or actual intersection in a stated probe.
- **Conditional:** a conflict or performance risk for a stated hardware envelope, fit, or preload condition. These are not predictions of measured machine performance.
- **Known incomplete work:** already disclosed release gates, listed separately below.

Severity means **Blocker** = specified assembly cannot be completed; **High** = credible loss of intended movement, alignment, or precision; **Medium** = manufacturing, service, or verification issue requiring resolution. All dimensions are millimetres.

## Findings at a glance

| ID | Severity | Finding | Evidence status |
| --- | --- | --- | --- |
| A01 | Blocker | Eight retainer screws cross the bearing-block bolts | Confirmed, eight exact intersections |
| A02 | Blocker | Four housing anchor heads/washers occupy the enclosure wall | Confirmed, four exact intersections |
| A03 | High | Output hub has no defined concentric register to the bearing | Confirmed geometry; operational effect conditional |
| A04 | High | Wheel-to-hub torque path and sleeve clamp stack are uncontrolled | Confirmed dimensions; slip conditional |
| A05 | High | Representative M8 sensor nuts collide with rotating geometry | Confirmed for stated nut; final SKU unselected |
| A06 | Medium | Worm radial location and outer-race retention lack a tolerance definition | Confirmed nominal fit; movement conditional |
| A07 | Medium | Seam fasteners assume an outer flat washer seat that does not exist | Confirmed nominal seating intersections |
| A08 | Medium | Driver replacement has no demonstrated route with the arm plate installed | Confirmed straight-lift conflict for full reservation |
| A09 | High | Fixture bolt tails can strike fixed screw heads during rotation | Confirmed probes; limit depends on fixture stack |
| A10 | Medium | Coupon and fit parameters do not cover several production interfaces | Confirmed coverage and parameter gaps |
| A11 | Medium | Two seam-strip STLs contradict their stated print orientation | Confirmed mesh/export mismatch |
| A12 | Medium | Collision validation omits critical hardware and differs from the written sampling gate | Confirmed coverage/document mismatch |

## A01 — Retainer screws intersect the block-fixing bolts

**Confirmed assembly blocker.** F08 uses four vertical M5 bolts at X±53, Y31.5/79.5. F09 uses horizontal M4 screws at Y32.5/78.5, Z27/73, passing through the same X positions. The closest axes are only **1 mm apart**, while their nominal shank radii total **4.5 mm**.

Disposable exact CAD checking found **eight shank-to-shank intersections**, with zero unchecked pairs. Conservative overlap volumes were approximately **45.036–49.005 mm³ each**. A second probe including existing F08 head/washer envelopes increased the upper conflicts to approximately 71.754 mm³.

Assembly order, reaming, and print compensation cannot resolve crossed metal shanks. The holes must be separated geometrically and the revised cap/block/sled joint checked with its complete hardware.

**References:** [block and cap geometry](../scripts/build_rotary_table.py#L126), [F08/F09 assembly stacks](rotary-table-fasteners.md#L54). Evidence: `fastener-crossings.probe.json` and `fastener-crossings.results.json` in the evidence folder.

## A02 — Housing bench fasteners cannot seat against the floor

**Confirmed assembly blocker.** Each F16 hole is at (105,105), rotated by quadrant. Its radius is **148.492 mm**, but the housing cavity ends at **R150**. The outward gap to the wall is therefore only **1.508 mm**.

The specified M5 cap head needs approximately 4.25 mm radius; the specified top washer is **OD15**, needing 7.5 mm. Both extend into the vertical housing wall when seated on the Z2.5 floor. Exact checking found **four intersections of 136.860488 mm³ each**, zero unchecked pairs.

Changing bolt length does not solve the seating obstruction. Define a usable anchor location or a deliberate clearance and bearing seat, then recheck wall strength, sealing, and the full fastening stack.

**References:** [housing wall and fixing-hole construction](../scripts/build_rotary_table.py#L207), [F16 hardware](rotary-table-fasteners.md#L28), [F16 stack](rotary-table-fasteners.md#L70). Evidence: `housing-anchors.probe.json` and `housing-anchors.results.json`.

## A03 — The output hub is not positively centered on the bearing

**High; geometry confirmed, actual eccentricity conditional.** The bearing bore is Ø55 and the printed hub neck is Ø44, leaving **5.5 mm radial clearance**. The Ø76 raised bearing-contact boss is a face land, not a locating spigot. The eight hub mounting holes are Ø5.5 around nominal M5 screws.

There is consequently no defined feature or assembly procedure that establishes the wheel/hub axis concentrically with the bearing axis. The nominal screw clearance alone permits approximately **0.25 mm translation** before print error is considered. The Ø14.8 printed wheel pilot in a Ø15 bore introduces another nominal **0.10 mm radial allowance** at that interface; these are individual allowances, not a guaranteed additive runout value.

If the wheel is mounted 0.25 mm off the rotation axis, its effective distance from the fixed worm varies by approximately ±0.25 mm through a revolution. Axially adjusting a duplex worm does not correct that eccentricity. Tight and loose mesh regions can result even though the ideal animation is perfectly concentric.

Define a concentric locating interface, or a documented centering procedure with measurable acceptance limits. Inspect wheel radial runout and mesh running torque before setting backlash. No actual binding was measured in this audit.

**References:** [bearing and hub geometry](../scripts/build_rotary_table.py#L174), [hub mounting requirement](specs/rotary-table.md#L74).

## A04 — Wheel torque transfer and metal sleeve compression need a deliberate design

**High; dimensions confirmed, motion estimate conditional.** Four Ø8 steel sleeves sit in printed Ø8.30 holes on a **30 mm PCD**. Each sleeve is **36 mm long**, exactly matching the nominal printed clamp stack from Z74 to Z110. There is no specified sleeve/print length tolerance, deliberate face compression, keyed torque connection, or separate locating/shear feature.

A short printed stack can let the screws clamp the metal sleeves without establishing the intended friction on the printed hub. A tall printed stack initially loads PETG; creep can change that condition. Merely showing touching faces in CAD does not define either result.

If torque transfers through sleeve contact with the hole walls after friction is lost, the nominal available reversal clearance is approximately:

`0.30 mm / 15 mm = 0.020 rad = 1.146°`

This is a **conditional geometric clearance bound**, not measured backlash. It excludes additional screw-to-sleeve clearance. It is substantially larger than the stated **0.10°** reversal target. Define how torque is transmitted, how the printed faces are clamped, and what controls slip after sustained loading and temperature exposure.

The motor anchor sleeves similarly equal the printed platform height exactly (**8 mm versus 8 mm**). Contrast the core columns, which explicitly provide **70 mm metal tubes versus 69.5 mm printed sleeves**. These interfaces need separate tolerances; copying a nominal zero difference does not guarantee a metal clamp path in a real print.

**References:** [hub stack and sleeves](../scripts/build_rotary_table.py#L179), [motor platform](../scripts/build_rotary_table.py#L144), [motor sleeves](../scripts/build_rotary_table.py#L334), [core sleeve relief](../scripts/build_rotary_table.py#L98), [precision target](specs/rotary-table.md#L56).

## A05 — Sensor retention hardware has insufficient room beneath the platter

**High; conditional on actual sensor hardware.** The sensor axis is **Z109.5**, and the platter underside is **Z116**, leaving 6.5 mm. The register expects two sensor jam nuts, but the assembly checks omit them.

A representative **AF13 × 3 mm M8 inner nut** needs at least 6.5 mm above its axis even with horizontal flats, giving **zero nominal running clearance**. With a corner upward, its top reaches Z117.00555. A disposable probe seated against the inner bracket face found:

- **5.254026 mm³** intersection with P32 platter.
- **1.854537 mm³** intersection with the steel home target.
- Zero unchecked pairs.

The printed bracket itself has only **1.0 mm measured clearance** beneath the platter, rather than the 2 mm used for the main labyrinth. Select the actual sensor, nuts, sensing gap, target retention, and cable exit together. Recheck the complete package through rotation. A different nut or mounting method may work; the probe does not establish that every M8 sensor is impossible.

**References:** [sensor bracket and axis](../scripts/build_rotary_table.py#L166), [target geometry](../scripts/build_rotary_table.py#L189), [pending jam nuts](rotary-table-fasteners.md#L107). Evidence: `sensor-nut.probe.json`, `sensor-nut.results.json`, and `local-measurements.results.json`.

## A06 — Worm bearing fit does not establish the required axis location

**Medium; nominal clearance confirmed, operational movement conditional.** The Ø35 bearings sit in Ø35.30 printed pockets, allowing **0.15 mm radial clearance** before printing error. The axial pocket depth and bearing width are both nominally 11 mm; the cap lands on the printed block at the bearing face plane. No controlled outer-race clamping allowance is specified.

The cartridge slots move along X to adjust duplex backlash. They provide no dedicated Y/Z adjustment or precision locating datum to establish and retain the nominal **Y55.5/Z50** worm axis. Shaft preload hardware controls the inner-ring stack, not the outer-ring location in loose printed pockets.

Define an allowable axis-position/alignment budget, bearing seat tolerances, outer-race retention, and a method to achieve them. Check both support alignment and running torque after tightening. The coupon instruction to seek a fit without wobble helps, but its shallow trial does not define loaded axis stability.

The selected pair and nominal 55.5 mm center distance match the [KHK duplex catalog](https://khkgears.net/pdf/agdl.pdf). KHK distinguishes axial backlash adjustment from center distance and requires correct reference-tooth/arrow orientation. Those facts do not qualify the printed support tolerances.

**References:** [adjustment slots and bearing seats](../scripts/build_rotary_table.py#L116), [shaft and bearing provisions](specs/rotary-table.md#L80).

## A07 — Seam washers are seated inside the curved housing surface

**Medium; nominal seating conflict confirmed.** F15 assumes a 16 mm printed stack and an exterior washer plane at local Y153. Across the OD9 washer footprint at X±6, the OD308 shell actually extends to approximately **Y153.64–153.99**.

All **16 nominal seam hardware envelopes** intersect housing material by approximately **40.0958 mm³ each**. This is primarily an exterior washer-seat conflict. Moving the hardware outward to about Y154 consumes approximately 1 mm of the documented 2.4 mm screw projection and leaves the washer bearing against a curved surface.

This is less absolute than A01/A02 because the hardware can move outward, but the stated flat stack is incorrect. Define a usable flat land or a deliberate alternative seat and recalculate bolt engagement, local wall compression, tool access, and seam sealing.

**References:** [housing flanges and seam strips](../scripts/build_rotary_table.py#L207), [F15 stack](rotary-table-fasteners.md#L68). Evidence: `omitted-hardware.probe.json` and `omitted-hardware.results.json`. Expected motor screw thread engagement in that result is not counted as a defect.

## A08 — Lid access does not establish driver replacement access

**Medium; straight-lift conflict confirmed for the full reservation.** The driver reservation is **118 × 76 × 35 mm** at Z36–71. The box rim is Z104, and M50 starts at Z136, leaving **32 mm** above the open box. The driver is 35 mm tall.

Lifting the driver straight upward until its bottom reaches Z104 places its top at Z139 and intersects the arm plate by **26,713.148 mm³**, zero unchecked pairs. The 140 × 84 opening leaves only 4 mm fore/aft clearance around the 76 mm envelope while it is inside the opening. The existing service tests demonstrate lid/tool access, not extraction of this driver.

Validate a removal route for the selected driver, wiring and thermal attachment. A smaller driver, a demonstrated tilted path, or a procedure that removes M50/the enclosure could resolve serviceability. This audit did not exhaust every possible tilted path. Document which service operations require unloading/removing the arm plate.

**References:** [box opening](../scripts/build_rotary_table.py#L258), [driver reservation](../scripts/build_rotary_table.py#L292), [box elevation](../scripts/build_rotary_table.py#L315), [arm plate](../scripts/build_rotary_table.py#L338). Evidence: `driver-removal.probe.json` and `driver-removal.results.json`.

## A09 — Fixture bolt tails need an explicit rotating clearance limit

**High; collisions confirmed for the stated example.** The four M6 fixture holes orbit at **R66.468**. Their screw tails sweep past fixed hardware, including the F01 column heads and F12 home-bracket heads. A bolt that tightens successfully at one table angle can obstruct movement at another.

An M6 × 35 shank with its head seated at the Z128 work surface has a tip at Z93. Disposable rotation probes found:

| Obstacle | Table angle | Overlap with example fixture tail |
| --- | ---: | ---: |
| F01 column screw head, top Z97.6 | 315° | 130.061936 mm³ |
| F12 home-bracket screw head, top Z98.15 | 94.899092° | 10.521455 mm³ |

Both checks had zero unchecked pairs. For **2 mm nominal clearance against these checked head envelopes**, the tighter restriction is:

**Fixture bolt tip Z ≥100.15**, equivalent to **under-head bolt length − fixture/washer stack above the work surface ≤27.85 mm**.

That permits at most **15.85 mm projection below the Z116 deck underside**. For example, M6 × 35 needs at least 7.15 mm of fixture/washer stack above the work surface; M6 × 30 needs at least 2.15 mm. These are geometric examples, not a finished workholding specification: engagement, actual heads, fixture loads, and any further obstructions must also be checked.

The existing register correctly leaves fixture lengths pending, but “do not bottom against fixed core” does not communicate this rotational tail limit. Specify the permitted projection and test the actual workholding through a full revolution.

**References:** [fixture-hole location](../scripts/build_rotary_table.py#L188), [deck fixture passage](../scripts/build_rotary_table.py#L201), [fixed screw envelopes](../scripts/build_assembly_checks.py#L31), [pending workholding](rotary-table-fasteners.md#L104). Evidence: `fixture-column-tail.*` and `fixture-home-tail.*`.

## A10 — The fit coupon does not represent several critical production fits

**Medium; confirmed.** The supplied coupon represents shallow Ø35 bearing pockets, vertical clearance holes, M5 nut pockets, and insert pilots. It does not directly validate:

- The M4 AF7.4 pockets used in P21/P23 or M6 AF10.4 fixture nut pockets in P30.
- Horizontal clearance holes used in P21/P24 and the two edge-oriented seam strips.
- The actual Ø8.3, Ø10.3, and Ø12.3 sleeve fits, long bores, or the Ø14.8 male wheel pilot.
- The 11 mm-deep bearing seat or a representative lid/insert sealing land under assembly load.

The M4 nut pockets use the literal expression **`7.4 mm+rt_fit*0`**. Changing `rt_fit` cannot correct those fits; no dedicated M4 nut-fit parameter exists. Thus the guide's named-parameter correction workflow is incomplete for those features.

Use representative additional coupons or explicit first-article checks, with a defined correction route for each fit. Calibrate horizontal and vertical holes separately. A passed shallow pocket or vertical through-hole does not certify all production orientations and depths.

**References:** [coupon features](../scripts/build_fit_coupon.py#L13), [M4 pockets](../scripts/build_rotary_table.py#L133), [foundation M4 pockets](../scripts/build_rotary_table.py#L151), [coupon instructions](rotary-table-printing.md#L29).

## A11 — Two seam strips are exported edge down

**Medium; confirmed.** Assembly placement rotates each P45 strip about Z, but all four then receive the same `[90,0,0]` export rotation. The resulting supplied STLs differ:

| Strip | Actual print bounds | Bed orientation |
| --- | --- | --- |
| 1 and 3 | 24 × 84 × 8 | Broad face down |
| 2 and 4 | 8 × 84 × 24 | Edge down |

The guide promises a broad flat face down for all four. Strip 2/4 have horizontal M4 holes and approximately one-third the first-layer contact area (**672 versus 1952.5 mm²** measured from the meshes). This changes adhesion, hole shape/support needs, and layer loading.

Choose the intended orientations deliberately and reconcile the export transform, manifest and guide. All four meshes remain closed and fit the printer; topology checks cannot detect an orientation instruction mismatch.

**References:** [strip construction and rotation](../scripts/build_rotary_table.py#L228), [export rotation](../scripts/export_rotary_table.py#L26), [print orientation instructions](rotary-table-printing.md#L45), [manifest](../exports/rotary-table/print-manifest.json#L581).

## A12 — Existing collision results cover an incomplete hardware population

**Medium assurance gap; confirmed.** The existing critical-envelope script includes F01/F02/F04/F05/F06/F07/F08/F10/F12/F13/F17/F20/F22/F23/F24. It omits the F03/F09/F11/F15/F16/F18/F19/F21 groups and the F14 screw heads. Its result is valid for the included envelopes, but does not verify every register row.

An audit rerun of that unchanged script completed all **15 interference calls** (13 table positions plus two cartridge offsets) with **zero overlaps and zero unchecked pairs**. The independent omitted-hardware probes still produce the collisions above. Both results are retained in the evidence folder.

The omitted F09 and F16 groups directly explain why A01/A02 were absent from the reported “zero unintended overlaps.” The report does disclose that only selected fasteners are modeled; the newly demonstrated conflicts show why the rest need explicit checks before release. Additional audit probes for F03/F11/F18/F19 found no unexpected interference; intended motor thread engagement was excluded from defects.

The governing specification also requires **17 sampled positions**, while the actual loop checks **13 positions in 30° steps**, as the validation report correctly states. Analytic sweep bounds help cover continuous rotating ribs/labyrinth geometry, but do not reconcile the written sampling gate or include absent hardware/fixtures.

Expand checks to the complete installed hardware, selected purchased devices, workholding, and operating/service poses. Keep thread/contact exclusions narrow and explicit. Reconcile the written sampling requirement, and use analytic sweeps or targeted angles for narrow obstacles such as the A09 fixture-head crossings.

**References:** [probe population](../scripts/build_assembly_checks.py#L31), [rotation loop](../scripts/build_assembly_checks.py#L61), [written gate](specs/rotary-table.md#L145), [reported scope](rotary-table-validation.md#L26).

## A1 Mini fit and tolerance assessment

Independent checks of **33 assembly STLs plus the coupon** passed paired-edge closure, consistent winding, positive signed volume, and nonnegative Z placement. All 33 assembly STL hashes matched the manifest. The largest part dimension is **168 mm**; the largest rectangular footprint with a 5 mm brim allowance on each side is **178 mm**. This fits the manufacturer's **180 × 180 × 180 mm** volume, leaving only 1 mm per side for that largest brim footprint if centered. PETG and the baseline 0.4 mm nozzle agree with the [Bambu A1 mini technical specification](https://store.bblcdn.com/1531c9726f6b41fba4594d5b47966ee0.pdf).

That is an envelope check, not a sliced job or a printer accuracy guarantee. Purge lines, support expansion, bed placement and brim removal still need review in the actual A1 Mini profile. No slicer or physical print was run for this audit.

| Interface | Nominal condition | Audit implication |
| --- | --- | --- |
| Metal columns / printed sleeves | 70 / 69.5 long | Deliberate 0.5 mm relief is sensible; verify actual matched lengths and square metal ends |
| Hub sleeves / printed clamp stack | 36 / 36 long | No tolerance separation; see A04 |
| Motor anchor sleeves / platform | 8 / 8 long | Define length tolerances and clamping behavior; see A04 |
| Worm bearing seats | Ø35.30 / Ø35 | 0.15 mm radial allowance before print error; see A06 |
| Hub-to-bearing screw fit | Ø5.5 / M5 | Nominal 0.25 mm radial translation allowance without a register; see A03 |
| Wheel pilot | Ø14.8 / Ø15 | Nominal 0.10 mm radial allowance; requires concentricity/runout acceptance |
| Housing/platter seams | 0.40 total | Sealant and print distortion consume the intended gap; check cumulative quadrant assembly |
| Main skirt and deck/upstand | 2 radial / 2 axial | Reasonable nominal separation, but no completed distortion/runout/deflection budget |
| Hub flange / stationary bearing envelope | 1 axial | Smaller local margin than the main labyrinth; verify the actual ring/seals and loaded stack |
| Sensor bracket / deck | 1 axial, measured | Smallest checked printed stationary/deck margin; complete sensor hardware makes it worse, A05 |

For rotating clearances, allocate a worst-case budget for print form error, assembly/runout, metal length/flatness tolerances, load deflection, sealant protrusion and retained debris. The stated 0.20 mm TIR/deflection targets are acceptance targets, not measurements to subtract as if already achieved. Do not use uniform model scaling to correct fits.

## Movement, load, sealing and service flows

The load-path concept is appropriate for a prototype: bearing and core plates use metal columns; the arm has its own welded stand and bench anchoring; the electronics lid carries no arm load. The nominal wheel/worm dimensions and center distance are consistent with the selected KHK reference pair. The [THK mounting-hole dimensional table](https://tech.thk.com/en/products/pdfs/en_a18_022.pdf) lists the same nominal 65 mm inner PCD with eight M5 holes and 105 mm outer PCD with eight Ø5.5/counterbored holes used here. That does not select a final bearing/seal/preload variant or validate the simplified ring profiles.

The THK table was available in its indexed manufacturer PDF; direct access to that per-page URL redirects by region. Obtain the final supplier drawing before machining. The Bambu and KHK PDFs were read directly.

The nominal rotating skirt/upstand and external gutter provide a plausible indirect splash path. The gutter outlets are external, and the electronics heat sink is outside its gasketed floor. No new definitive drain-to-electronics routing conflict was established. However, flat gutter drainage, slurry retention, printed porosity, seam movement, curved motor-hood sealing, gland washer lands and gasket compression must be tested on the assembled parts. Neither a static Boolean check nor a manifold STL establishes ingress resistance.

Lid/tool access has nominal room, but driver replacement is distinct (A08). Cable routes remain reservations: actual gland nuts, connectors, bend radii, strain relief, wiring above the controller and service loops need checking with selected parts. Maintain access to the rear lid-withdrawal path. The 35 mm driver reservation excludes wiring and does not establish a complete installation envelope.

The folded arm illustration and table revolute joint do not establish tool reach, approach angles, joint limits or collision-free carving motion. A complete articulated arm/tool/workpiece study remains necessary, especially around the stand, platen edge, motor hood and the proposed maximum workpiece height. No loaded stiffness, drivetrain efficiency, backlash, dynamic stopping or 5 kg payload test was performed.

## Known release blockers already acknowledged in the project

These are not newly discovered mistakes, but remain necessary before fabrication/operation can be treated as qualified:

1. **Finish the drivetrain.** Actual bearing variant and supplier requirements; worm bore/key approval; shaft keys, shoulders, locknuts/spacers and bidirectional bearing preload/retention; wheel machining and attachment tolerances. Preserve KHK's tooth geometry and assembly markings. A plain shaft envelope does not retain or drive the worm.
2. **Select actual devices.** Motor/encoder, coupling, sensor, glands, driver/controller, thermal interfaces and board mounts. Verify supplier screw engagement limits and connector service space. The screw kit remains conditional on these selections.
3. **Finish workholding.** Clamp/fixture geometry, bolt lengths, nut retention, sealing and full rotational clearance, including A09. Four fixture holes alone do not secure a workpiece.
4. **Qualify the stand and bench.** Actual bench thickness/stiffness, anchor lengths/backing, weld sizing/process/distortion and arm/tool reaction loads. The documented 10.84 N·m initial overturning case is a design load case, not a passing structural result.
5. **Complete thermal/electrical integration.** Driver-to-spreader contact, heat-sink retention, closed-lid temperature test, cable restraint, emergency-stop/control behavior and coordinated motion. A thermal adhesive pad envelope is not a verified structural attachment.
6. **Print and test.** Representative fit/strength/insert trials, first articles, sealing, free rotation and running torque through 360°, progressive load tests, reversal error, radial/axial runout and loaded deflection. Verify after temperature exposure and repeated service.

## Recommended resolution order

1. Resolve A01/A02 and the A07 seating stack; check all installed fasteners together before committing to a full print set.
2. Define hub centering, torque transfer, sleeve tolerances and bearing location/retention (A03/A04/A06).
3. Select and fit-check sensor and workholding hardware, including their full sweeps (A05/A09).
4. Resolve driver service access; select actual electronics, glands and cable paths (A08).
5. Reconcile orientations and coupon coverage, slice every part with the intended A1 Mini profile, and measure representative first articles (A10/A11).
6. Expand/reconcile validation (A12), regenerate only after approved design changes, then complete the physical release gates above.

## Reproducing the audit probes

The original probes use revision 3 body names and intentionally reproduce its failures. Extract that baseline first, then replace `PROBE` with an evidence-folder `*.probe.json` file. Do not add `--save`:

```sh
git show a403195:michelaingelo.sc > /tmp/rt01-audit-baseline.sc
/Applications/SolidCraft.app/Contents/MacOS/solidcraft-cli run \
  docs/audit-evidence/2026-11-17-rt01/PROBE.probe.json \
  --in /tmp/rt01-audit-baseline.sc --results --quiet
```

`omitted-hardware.probe.json` builds on the existing disposable fastener check population; its full commands are retained. Some probes intentionally create known collisions to reproduce findings. A positive result there confirms the audit defect rather than passing the design. Evidence is nominal geometry, not a physical fit, strength or safety certification.

## Revision 4 re-review handoff

The [implementation response](rotary-table-audit-response-2026-11-17.md) records the verdict, applied fix, verification and remaining gate for A01–A12 individually. It preserves the distinction between confirmed assembly/coverage defects and conditional performance estimates. Current hardware checks cover all 23 active screw groups, 26 rotation poses and both carrier limits; source/STEP, service, coupon/parameter and print-orientation evidence is retained separately under `revision4/`.

A01/A02/A07/A08/A11 have concrete geometry/export remedies with passing nominal checks. A03/A04/A05/A06/A09/A10/A12 have implemented interfaces/coverage and passing CAD evidence, with explicit fabrication, supplier, real-fixture or physical-test gates. Neither this update nor the new zero-intersection result is a precision, strength or water-resistance certification. The original audit evidence above has not been overwritten.
