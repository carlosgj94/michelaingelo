# RT-01 validation — revision 4, 2026-11-17

**The audit corrections pass the listed CAD checks; the prototype is not fabrication released.** No physical arm/print/load/precision/ingress test was run. The [audit response](rotary-table-audit-response-2026-11-17.md) separates each original defect, applied change and remaining qualification.

Evidence: [results and hashes](../cad/validation-results.json), [raw revision 4 records](audit-evidence/2026-11-17-rt01/revision4/), [print manifest](../exports/rotary-table/print-manifest.json). The revision 3 audit/probes remain unchanged in the parent evidence folder; its old passing subset was not a complete hardware check. The previous validation report is [archived](archive/rotary-table-validation-rev3.md).

## Passed

| Check | Result / scope |
| --- | --- |
| New geometry | 81/81 table/support bodies closed; 100 world bodies including 19 imported arm bodies; no failed features |
| Sketches / joints | 7/7 sketches have zero DOF; C axis at 0°, rigid arm mount present; no reported joint conflicts/floating groups |
| Arm preservation | All 19 volumes and bounds match revision 3 after +8 mm Z shift; max volume difference 3.09e−9 mm³, bound error 3.42e−13 mm |
| Full screw population | All 23 register groups, 119 screws (101 fixed, 18 bench), plus selected permanent retention and four deepest permitted fixture tips |
| Rotation / carrier travel | 17 unique uniform samples plus targeted crossings/closure = 26 poses, then ±3 mm carrier limits; all 28 checks have zero unexpected intersections/unchecked pairs, no budget truncation |
| Service | 13 checks for ten lid-tool shafts and sequential lid, controller/tray and 35 mm driver extraction; zero overlaps/unchecked pairs |
| Selected interfaces | Exact-face gaps: target/sensor 1.2, sensor/bearing 9.0, stationary bearing/hub flange 1.0, upper sensor nut/hub 8.7, pin/slot side approximately 0.005 mm |
| Source consistency | All 81 fresh standalone bodies match the native candidate; volume and bound deltas 0 |
| STEP round trip | All 81 bodies return; max volume delta 0.00003394 mm³, bound error 1.85e−13 mm |
| Print meshes | 25 assembly STLs plus coupon; paired edges, consistent winding, positive volume and bed placement; hashes match manifest |
| A1 Mini allowance | Largest assembly dimension 168; largest footprint with 5 mm brim per side 178 within 180 bed |
| Tessellation agreement | Worst assembly mesh/CAD volume difference 0.040419%, below 0.25% export limit |
| Seam strip orientation | All four 24×84×8 with 1952.4855 mm² bottom contact; explicit exporter regression gate |
| Fit parameter trial | Eleven parameters enlarged together; 214 features rebuilt with no errors, expected print bodies changed; coupon 150×100×24 |

Geometry comparison limits are 0.01 mm³/body and 1e−6 mm per bound coordinate. Source comparison concerns geometry, not identical feature history or saved UI state. The original imported arm's one open surface body and import tolerance warnings remain; no new body inherits them. Model density defaults are not a validated material/mass or structural model.

The hardware probes use shanks, specified heads/washers and conservative nut envelopes. Retained sensor nuts/pin/shims are already part of the design. Thread engagement, press interference, purchased tooth blank contact and unchanged arm self-contact have narrowly named exclusions in [coverage](../cad/hardware-check-coverage.json). Excluding a screw/tapped-body pair is not a thread strength check; the separate stack calculation must still be met. Below-bench bolt lengths, actual insert retention and unselected hardware are outside this result. No disposable screw/test body is saved in the main native file.

Continuous nominal bounds supplement the sampled angles: rib radius≤146.2 versus fixed wall 150; rib bottom 98 above seam top 96; skirt/wall radial gap 2; deck/upstand axial gap 2; target bottom 99.7 above column-head top 97.6. Printed distortion, metal tolerances, TIR, load deflection, sealant and debris consume those margins. The one-millimetre hub/bearing gap needs the actual ring/seal drawing and measured axial stack. The full articulated arm/tool/workpiece motion envelope has not been analyzed.

## Retained evidence and reproduction

The `revision4/` evidence folder contains raw CLI results, measurements, probe inputs for health/parameter/interface checks and a compact summary. The complete rotation/service scripts live in `cad/`. All tests run headlessly in disposable models without `--save`.

```sh
/Applications/SolidCraft.app/Contents/MacOS/solidcraft-cli run cad/fastener-clearance-checks.json --in michelaingelo.sc --results --quiet
/Applications/SolidCraft.app/Contents/MacOS/solidcraft-cli run cad/support-access-checks.json --in michelaingelo.sc --results --quiet
/Applications/SolidCraft.app/Contents/MacOS/solidcraft-cli run docs/audit-evidence/2026-11-17-rt01/revision4/fit-parameters.probe.json --in michelaingelo.sc --results --quiet
```

`python3 scripts/record_revision4_validation.py` checks and summarizes the retained files; **it does not rerun CAD**. Refresh the raw evidence and measurements before using it to report a changed design. `native.measure.json` is the reviewed native measurement, `fresh.measure.json` a clean standalone build, `step.measure.json` the exported STEP reimport, and `arm-baseline.measure.json` the original revision 3 assembly for the translation comparison. Snapshots are regenerated from the final candidate with temporary visibility changes.

## Not run / release gates

1. Machine/inspect measured bearing/hub/column/guide fits, pilot and wheel runout, axis location and outer-race retention; obtain actual bearing drawings and finish shaft keys/shoulders/preload/locknuts. Approve pin/wheel/thread strength, clamping and fatigue. The machining table is a requirement, not a measured result.
2. Select motor/coupling, cordset/glands, actual driver/controller and thermal attachments. Prove connector/service-loop access and sensor signal with the steel target. Homing is not platter-angle feedback.
3. Finish workholding, enforce the blind-thread engagement rule and check the actual fixture/workpiece upper sweep. Specify the actual bench T, backing, weld details and stand capacity against arm/tool reactions.
4. Slice and print the revised coupon/first articles; measure fits, insert retention, PETG creep, sealing lands and support removal. No radius/scalability range was qualified; the evidence applies to the 320 mm baseline.
5. Commission unloaded, then progressively loaded: free rotation, torque, backlash/reversal, radial/axial TIR, stiffness, stopping, thermal behavior and dust/splash ingress. No FEA, structural rating, machine IP claim or stone-carving qualification.
