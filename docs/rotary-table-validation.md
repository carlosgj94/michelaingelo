# RT-01 validation — revision 5, 18 November 2026

**The corrective CAD passes the checks below.** The [audit response](rotary-table-design-audit-2026-11-18.md#revision-5-response-for-review) records the disposition of each finding. Fabrication release and physical tests are pending.

The sourcing colors are a display update to revision 5. The native archive matches the tested candidate with its display appearances excluded. The validation record identifies both the current colored file and the file used for the mechanical checks.

| Check | Result and scope |
| --- | --- |
| Native model | 741 timeline entries, zero failed features, 11 sketches with zero degrees of freedom. All 81 table and support bodies closed. 100 placed bodies including the arm. |
| Arm and joints | The 19 arm body measurements and bounds equal the revision 4 baseline in the same SolidCraft build. C axis at zero and rigid arm mount intact. No joint errors or floating groups. The imported open surface and tolerance warnings are retained. |
| Hardware and motion | 23 groups, 119 screws and bolts, plus four deepest permitted fixture-tip probes. All 26 rotation poses and both ±3 mm carrier limits completed with zero unexpected intersections and zero unchecked pairs. |
| Service | All 586 clearance checks passed with zero overlaps or unchecked pairs, including 184 for removal and refitting of the four F19 captive-washer assemblies and tray. The service replay includes the repeated worm-key cycle and arm screw tool paths. The driver test covers both full rectangular sweeps of the nominal bare envelope. Raised withdrawal clears both rim and plate by 2.5 mm and the F24 tip envelope by 3.5 mm. |
| Anchor seats | Eight positive bearing-area probes support the nominal F21 seal lands and F23 washer footprints. F21 washer-to-M55 clearance is 2 mm. M60 leaves 1.4 mm above the two concealed F02 heads. |
| Hood and drains | The hood slides +X70 before lifting, with a 0.90 mm minimum measured critical washer gap at X+49. The post-to-roof continuity and all four clear drain rays were checked on the corrected geometry. |
| P54 drain catches | At each of the four positions five discharge rays hit the catch floor. All four outward and upward removal sweeps clear. The minimum installed clearance is 1.44 mm to the housing when rounded down. The liquid solids clear the cup walls and give 19.87 mL at the fill mark and 26.30 mL at the pour notch. The closed mesh has an 80 × 50 mm footprint including a 5 mm brim. |
| Gasket | 1,912 mm³ of B24 stock in a 2,509.5 mm³ nominal gland. Fill is 76.19%, with 2 mm of inner land at the opening. |
| Generator and STEP | All 81 table and support bodies match the independent rebuild in volume and bounds. STEP reimport returns all 81 with maximum deltas of 2.24×10⁻⁹ mm³ in volume and 1.85×10⁻¹³ mm in bounds. |
| Prints | 25 assembly STLs and one fit coupon, with paired edges, consistent winding, positive volume and matching manifest hashes. Maximum assembly dimension is 168 mm and the largest footprint with 5 mm brim is 178 mm. Maximum mesh/CAD volume delta is 0.017425%. All four seam strips are broad face down. |
| Fit trial | Twelve printed fit parameters enlarged together. 241 features rebuilt with zero errors. The F21 nut trap and loading slot are represented on the fit coupon. |

[Results and hashes](../cad/validation-results.json) · [Revision 5 evidence](audit-evidence/2026-11-18-rt01/revision5/) · [Service follow-up](audit-evidence/2026-11-18-rt01/service-follow-up/service.results.json) · [Catch check](audit-evidence/2026-11-18-rt01/service-follow-up/drain-catch-summary.json) · [Print manifest](../exports/rotary-table/print-manifest.json)

The service checks remove F17 for hood service, F18 for lid service and F19 for tray and driver service. F24 is represented by its permitted tip and provisional upper hardware envelope. The real matched seats and upper screw stack depend on the owned arm foot. The below-bench checks use an illustrative common Z plane. Bench thickness changes anchor length, while bench frame clearance and access depend on the installed bench. The eight seat probes intentionally intersect half of a thin annulus to check the bearing area.

Nominal contact, torque capacity, pressure and creep are separate. The retained hardware probes exclude named thread and press fits, the bought tooth blanks and the imported arm's self-contacts. Actual components and allowance for distortion, machining, runout, lubricant or debris affect the usable margins. [Probe population and exclusions](../cad/hardware-check-coverage.json)

## Repeating the CAD checks

Run in disposable in-memory sessions from the repository root.

```sh
solidcraft-cli run cad/fastener-clearance-checks.json --in michelaingelo.sc --results --quiet
solidcraft-cli run cad/support-access-checks.json --in michelaingelo.sc --results --quiet
solidcraft-cli run docs/audit-evidence/2026-11-18-rt01/revision5/fit-parameters.probe.json --in michelaingelo.sc --results --quiet
```

Run `python3 scripts/build_drain_catch.py` to regenerate the editable accessory, print mesh and placement evidence against the current model. Run `python3 scripts/record_rotary_table_validation.py --replay-service` to refresh the installed-service evidence and validation record. Without `--replay-service`, the recorder checks the saved results against the probe and native geometry digests. The original 18 November audit and its initial replay inputs record revision 4 hardware. [Revision 4 evidence](audit-evidence/2026-11-17-rt01/revision4/) · [Independent audit](rotary-table-design-audit-2026-11-18.md)

## Physical acceptance pending

- Measure the four owned SO100 foot seats, fit their bearing details and size the recessed F24 screws. Prove contact, preload retention and the fixture-to-tool response to abrupt stops using the actual bench and welds.
- Finish the worm/shaft/bearing retention drawing, choose the motor, coupling and electronics, and verify actual running clearances, thermal contact, wiring, service access and stopping.
- Confirm the selected F07, F19 and F24 tools, actual screw engagement and lead routing. Demonstrate two successive tightening strokes on each front F07 screw. On the fitted machine check F19 washer retention and gripper release, remove and refit all four assemblies, and service the tray and driver.
- Slice and print the coupon and first articles. Verify the anchor seal, nut trap, gasket, insert fits, clamp loads and sensor signal. In the unpowered tracer trial, centre and mark all four drain cups, empty and return them to their marks, and check collection at every outlet again.
- Design and sweep the actual fixture, tool and articulated arm. Measure load, reversal, TIR, stiffness, temperature and ingress in the intended foam use. The audit's ideal-contact stand simulation is a comparative screening study. Revision 5 has no new structural simulation or rock-use qualification.
