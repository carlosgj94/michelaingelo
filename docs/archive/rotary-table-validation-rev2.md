# RT-01 validation — Revision 2, 2026-11-17

**Result: prototype geometry and exports checked; not fabrication released.** The native assembly is `michelaingelo.sc`. The specification was established before replacing the previous base. Modelled interfaces were then refined during clearance checks, and the specification was reconciled with the resulting geometry.

Machine-readable evidence: [cad/validation-results.json](../cad/validation-results.json). Per-print mesh bounds and checksums: [print-manifest.json](../exports/rotary-table/print-manifest.json). Source hashes in the evidence identify the checked revision; geometry changes require renewed checks.

## Passed

| Check | Result and scope |
| --- | --- |
| Native body health | **85/85** new table bodies are closed; no failed features or new modelling warnings |
| Sketch health | **33/33** sketches solved, 0 remaining degrees of freedom |
| Reference preservation | All **19** arm bodies preserve their volume and bounds under the intended rigid transform; base underside seats at Z144 on M50. Relative joint pose and scale unchanged |
| Static separation | No arm/table overlap in the mounted pose. Minimum arm-to-rotor clearance **14.03 mm**; base-to-adapter contact 0 mm; lid-to-adapter clearance **28 mm**. Not a full arm workspace study |
| Rotary joint | Vertical Z revolute joint with a saved one-revolution motion study; returned to 0° for delivery |
| Interference | **17 sampled poses**: 0° through 337.5° at 22.5° spacing, plus 16.7°. Zero unintended overlaps, zero unchecked pairs, no budget truncation |
| Support contact | P23 rests on the continuous M40 sole at Z4; M40 contacts the core underside and its base lies at bench Z0. M4 arm-shank and recessed M5-head probes show no interference |
| Service access | Ten Ø6 × 58 mm tool-shaft probes clear the adapter and folded arm. Lid/gasket lift 8 mm, then withdraw rearward at 40/80/140 mm sampled offsets without overlap |
| Intentional exclusion | Only the B04 worm / B11 wheel **tooth-envelope** pair is excluded. Whole components or occurrences are not excluded |
| Parameter regeneration | Two trials: radius 150/160 mm, diametral fit 0.20/0.40 mm, seam 0.30/0.60 mm, motor reserve 60/80 mm. Both regenerate without errors; 85 closed bodies; baseline restored |
| Reproducibility | Fresh standalone build matches all 85 saved table/support bodies by name, volume and bounds, with maximum volume difference <0.00001 mm³ and zero measured bounding-box difference |
| Assembly STEP round trip | Reimport yields the same 85 bodies and bounds; maximum body-volume difference <0.00005 mm³ |
| Printable meshes | **33 assembly STLs + coupon**: all edges paired, consistent triangle winding, positive enclosed volume |
| Mesh/CAD agreement | Worst assembly mesh volume difference **0.04042%**; coupon **0.01391%** |
| A1 Mini envelope | Largest supplied print dimension **168 mm**; maximum XY footprint with a 5 mm brim on each side **178 mm**. Coupon 140 × 70 × 8 mm |
| Visual review | Mounted assembly, covers/adapter-hidden and motor-support views reviewed. Final file restored to assembled view with the arm mounted; section and selection overlays cleared |

Parameter trials check regeneration and body closure, not every collision at every alternative parameter combination. The collision and export checks apply to the delivered baseline. Radius is only exercised over 150–160 mm; the design is not proven scalable by arbitrary numeric enlargement.

The STEP and CAD checks concern the modelled bodies. Most fastening hardware, wiring and real bearing/gear internals are not included. Source material labels and CAD default density are not a verified mass model.

## Continuous-clearance reasoning

The sampled collision checks are supplemented by simple sweep bounds:

- Rotating rib envelope is inside R146.2; the stationary main wall starts at R150.
- Stationary seam flanges/backing strips end at Z96; rotating ribs start at Z98: **2 mm vertical gap**.
- Stationary upstand ends at Z114; the deck underside starts at Z116: **2 mm axial gap**.
- Fixed wall OD308 and rotating skirt ID312 give **2 mm radial gap**.
- Metal bearing outer ring ends at Z105; the main output flange starts at Z106. The smaller contact boss touches only the inner bearing ring.
- Steel core tubes are 70 mm long; printed sleeves are 69.5 mm, keeping sustained clamp force on metal.

These are nominal CAD clearances. Print distortion, assembled runout, sealant, fixture hardware and load deflection consume them. Check the complete sweep after assembly and under load.

## Issues found and corrected

An intermediate-angle collision check found the rotating ribs clipping the housing seam braces even though the 0° and 45° poses were clear. Lowering the fixed braces established the 2 mm vertical separation, and all 17 positions passed afterward. The motor foundation was relieved around the metal bench spacer. Motor/coupling clearance, hood gasket compression stops and heat-spreader sealing were also reconciled with their adjacent geometry before export.

Revision 2 replaces the unsupported printed motor tab/platform arrangement with a full metal sole and bench anchors through metal compression sleeves. Two underside countersinks now provide actual M5 head clearance. The arm sits on a metal plate and four bench-supported steel posts above the controller box. The original central lid-screw access conflicted with the folded arm; the final ten-screw pattern moves the front/rear intermediate positions to X±42 and passes the tool-path check. The rear gland clearance was restored through the relocated insert boss, preserving the complete gland aperture and continuous gasket groove.

The final static check was repeated after that gland trim. The trim only removes electronics-box material; it does not change the earlier clear rotary sweep. The fresh scripted build and STEP round trip include the final trimmed shape.

The original arm import retains its existing surface/tolerance warning and one open surface body. This pre-existing reference limitation was preserved, is recorded in [the arm notes](../references/so-arm100/README.md), and is separate from the 85 new closed table/support bodies. No new table warning remains.

## Not run / outstanding before fabrication release

1. **Purchased hardware and manufacturing interfaces:** confirm the exact RU85 bearing variant and hole phase; select motor, coupling, driver, sensor, glands and heat sink. Finish the worm-shaft key/shoulders/retention/preload drawing and wheel attachment machining. Confirm supplier load/torque ratings and all fastener engagement/access. The simplified tooth envelopes do not validate a real mesh.
2. **Printing:** slice with the actual A1 Mini/filament profile, inspect supports and purge clearance, print the fit coupon, measure it, then inspect first articles. No slicing or physical print was performed.
3. **Mechanical performance:** measure actual assembled inertia and friction; select motor current and acceleration accordingly. Test the 5 kg target progressively, measure runout, bidirectional lost motion and loaded stiffness. No FEA, load test or carving test was performed. The 0.10° reversal target is not a measured result.
4. **Ingress and temperature:** verify seam/gasket compression, seal all penetrations and print porosity, then perform unpowered splash/dust tests. Establish heat-sink attachment and driver thermal contact, and measure temperatures with the box closed at operating current. No IP or waterproof rating is claimed.
5. **Control and robot integration:** implement homing, limits, emergency-stop behaviour and coordinated motion. A motor encoder does not measure platter backlash. The optional output encoder has only a reserved volume. The arm is fixed to the bench-supported bridge and its displayed pose is clear. Full reach, moving-arm collision checks, bridge/bench stiffness and loaded carving remain unvalidated.

The supplied model is suitable for design review, dimensional prototyping and preparing the remaining hardware drawings. It does not establish stone-machining capacity or safe loaded operation.

## Repeating the support checks

The headless script below creates temporary fit probes and moves the lid in a disposable in-memory model; it does not save over the working assembly:

```sh
/Applications/SolidCraft.app/Contents/MacOS/solidcraft-cli run cad/support-access-checks.json --in michelaingelo.sc --results --quiet
```

It checks nominal shanks/heads and tool shafts, not threads, wrench-handle ergonomics, manufacturer torque ratings or every real fastener stack. Confirm the owned arm revision and actual screw seating before machining M50. The 228 mm arm plate is metal; every printed part remains within the A1 Mini envelope.
