# RT-01 validation — Revision 3, 2026-11-17

**Prototype geometry and exports checked; not fabrication released.** The arm has not been tried on this assembly. This revision addresses anticipated reaction loads from its abrupt motion; it does not document a measured stand failure or a proven stiffness improvement.

Evidence and file hashes: [validation-results.json](../cad/validation-results.json). Hardware: [fastener register](rotary-table-fasteners.md). Mesh dimensions and hashes: [print manifest](../exports/rotary-table/print-manifest.json).

## Passed

| Check | Result and scope |
| --- | --- |
| Body health | 84/84 table/support bodies closed; no new failed features or warnings |
| Sketch health | 37/37 sketches fully constrained, zero remaining DOF |
| Arm preservation | All 19 arm body volumes and bounds exactly match the mounted pre-revision assembly; no pose or scale change |
| Rotation with hardware | 13 sampled positions, 0–360° in 30° steps, with 64 temporary critical fastener envelopes: zero unintended overlaps and zero unchecked pairs |
| Cartridge adjustment | Both +3 and −3 mm axial positions checked with moving support/shaft/bolt envelopes: zero unintended overlaps and zero unchecked pairs |
| Service access | Ten Ø6 tool shafts clear the arm adapter and frame. Lid/gasket lift 8 mm and withdraw 40/80/140 mm without overlap; arm plate remains 28 mm above the closed lid |
| Fresh source comparison | All 84 table bodies match by name. Maximum volume delta 0.002678 mm³; maximum bound-coordinate delta <0.000001 mm |
| STEP round trip | All 84 bodies return. Maximum volume delta 0.002678 mm³; maximum bound-coordinate delta <0.000001 mm |
| Printed exports | 33 assembly STLs plus coupon: paired edges, consistent winding and positive volume |
| A1 Mini envelope | Largest print dimension 168 mm; largest footprint including 5 mm brim each side 178 mm |
| Mesh/CAD agreement | Worst assembly volume difference 0.040419% |
| Hardware register | 24 joints; 106 defined-length screws and 18 bench bolts with thickness formulas. Internal arm screws excluded; four arm-base bolts included |
| Delivered state | Saved native file reopened in SolidCraft, C axis at 0°, arm rigid mount intact, sketches/selection/section overlays hidden |

The volume-comparison limit is 0.01 mm³ per table body and the bound-coordinate limit is 0.000001 mm. Tiny differences from Boolean history/STEP reconstruction are below those limits. The print exporter separately requires mesh volume error below 0.25%.

Collision exclusions are explicit in the check script: simplified worm/wheel tooth volumes, the imported arm's internal self-pairs, screw threads inside designated tapped parts, and F22 shanks against the already-modelled top washers. The test does not certify real tooth contact, preload or torque capacity. Only selected critical screws are represented by full/partial envelopes; the other register rows are based on nominal hole and stack calculations. No test fasteners are saved into the delivered assembly.

The four brace-window sketches are fixed fabrication profiles. The pre-existing `Sketch1` remains at its original world plane with its four lines preserved; its obsolete projected-face link was converted to fixed review geometry when the table was rebuilt. The original arm's surface/tolerance warnings and one open surface body remain unchanged. The earlier assembly is archived in `docs/archive/rt01-before-braced-stand.sc`.

## Changes covered by these checks

- Two welded 4 mm steel side channels with 28 mm flanges and a front X brace replace the four 136 mm posts. Four M6×25 bolts attach M50; separate bench bolts use two steel backing strips. The electronics box carries no arm load. Rear service access remains open.
- M01 is now 164×184×8 mm. P20 is 156×94×8 mm. Cartridge anchors moved to X±52/Y18 and X±70/Y92. Ø25 openings clear the core bench-bolt heads; Ø30 notches clear the column sleeves throughout adjustment. Tip-relief slots preserve the ±3 mm cartridge travel.
- Wheel screws changed from M5×50 to M5×45. Worm-block heads are recessed. Motor-foot holes moved clear of the upright bracket; M40 clears protruding motor/hood screw tips. The core uses small OD11 washers beside the bearing.
- Home bracket/target moved 45° away from the column screw. Heat-spreader screws are flush DIN7991 heads, with seals below the floor and gasket reliefs around the compression shims. M3 insert pilots use a nominal 4.0 mm starting size for RX-M3x5.7, subject to the coupon.

Existing continuous-clearance bounds still apply: rotating ribs inside R146.2 versus fixed wall starting R150; ribs start Z98 above seam structures ending Z96; skirt ID 312 versus wall OD 308; deck underside Z116 versus fixed upstand Z114. The core steel tubes are 70 mm and printed sleeves 69.5 mm, retaining a metal clamp path. These are nominal clearances, consumed by print distortion, runout, sealant and load deflection.

## Not run / remaining work

1. **Stand and bench:** choose the actual rigid bench, measure its top thickness, finish anchor lengths, and review weld sizing/fabrication against real arm/tool reactions. Test loaded motion and stopping. No FEA, stiffness measurement or dynamic load test was performed; a loose wood block is not the mounting basis.
2. **Purchased components:** confirm bearing variant, motor/coupling, sensor, glands and electronics; finish shaft keys/shoulders/retention/preload and wheel machining. Complete the pending interfaces explicitly listed in the fastener register. The known joint schedule is not an all-components purchasing release.
3. **Printing:** slice, inspect supports, print the coupon and measure actual fits. The A1 Mini check concerns mesh envelopes and topology, not a physical print or strength qualification.
4. **Motion and machining:** measure backlash, runout, loaded accuracy and temperature. Validate the arm's complete moving workspace and implement appropriate motion/control behaviour. Stand bracing does not remove servo backlash or smooth abrupt commands.
5. **Dust, water and heat:** test seals, print porosity, drainage, heat-sink retention and closed-box temperatures. No IP or waterproof rating is claimed.

Revision 2 parameter-range trials are historical; they were not repeated as a Revision 3 scalability qualification. Current collision/export evidence applies to the delivered 320 mm baseline.

## Repeating the checks

Run these in disposable headless models; omit `--save` so probe hardware and test poses cannot overwrite the working assembly:

```sh
/Applications/SolidCraft.app/Contents/MacOS/solidcraft-cli run cad/fastener-clearance-checks.json --in michelaingelo.sc --results --quiet
/Applications/SolidCraft.app/Contents/MacOS/solidcraft-cli run cad/support-access-checks.json --in michelaingelo.sc --results --quiet
```

The scripts test nominal geometric fit, not wrench-handle ergonomics, bolt preload, thread strength, weld quality or physical stiffness. The 228 mm wide arm plate and steel stand are fabricated metal parts, supplied separately from the A1 Mini STLs.
