# Michelaingelo

A robot-carving project starting with foam. RT-01 is a **single-axis rotary worktable**: the workpiece turns on a 320 mm platter about vertical Z, while the SO100 sits on a fixed steel stand above the controller box. The stand and rotary core bolt to the same rigid workbench. The printed box carries no arm load.

## Current design — revision 4

The [independent audit](docs/rotary-table-design-audit-2026-11-17.md) identified twelve assembly, alignment, service and verification issues. They have been checked individually and revised in CAD, hardware records and print exports. Read the [finding-by-finding response](docs/rotary-table-audit-response-2026-11-17.md) for evidence, tradeoffs and remaining physical tests.

The precision core now uses a **machined metal hub, one-piece worm-bearing carrier, metal retainer caps and integral motor foundation**. Purchased crossed-roller and angular-contact bearings support a 40:1 KHK duplex worm drive. Metal pilots, a carrier guide and a drive pin replace the former printed alignment/clamp interfaces. This adds machining beyond the original two-plate concept.

The assembly has **25 A1 Mini printed pieces plus a revised fit coupon**. The covers, platter sections, motor bracket and electronics enclosure remain PETG prototype parts. The arm's geometry and relative pose are preserved; its complete mounting stand is 8 mm taller so the full reserved driver can be removed from the rear.

![RT-01 with mounted arm reference](docs/rotary-table-with-arm.png)

This is **prototype geometry for review, not a fabrication release or tested precision/load/waterproof rating**. The 5 kg payload, 4/8 N·m drive torque and 0.10° reversal error are acceptance targets. Actual bearings, shaft retention/preload, motor/coupling, electronics/cables, fixtures, bench thickness and stand fabrication still need the decisions/tests listed in the specification. Homing does not measure output-angle error. Bracing does not smooth the purchased arm's commands or remove internal backlash.

## Review and build files

- [michelaingelo.sc](michelaingelo.sc) — native SolidCraft assembly; named views **RT01 and arm reference**, **RT01 assembly**, **RT01 top**.
- [Audit response](docs/rotary-table-audit-response-2026-11-17.md) — A01–A12 decisions, evidence and review gates; original revision 3 findings preserved.
- [Mechanical specification](docs/specs/rotary-table.md) — geometry, machining fits, load targets, sensor, sealing and acceptance requirements.
- [Validation report](docs/rotary-table-validation.md) — current checked results and explicit limits.
- [Fastener register](docs/rotary-table-fasteners.md) and [CSV](cad/fastener-shopping-list.csv) — 23 active groups, 101 fixed-length screws and 18 thickness-dependent bench bolts; includes four arm-base bolts, excludes arm internals.
- [Bill of materials](docs/rotary-table-bom.md) — quantities grouped into prints, fabricated metal, bearings/transmission, controls, seals and fasteners; excludes the arm but includes its mounting bolts, washers and nuts. Unselected items and bench-dependent lengths are marked.
- [Printing/assembly guide](docs/rotary-table-printing.md) — coupon map, first articles, print orientation and assembly/service sequence.
- [Print package](exports/rotary-table/rt01-print-package.zip) — 25 oriented STLs, coupon, manifests, guides and metal references.
- [Assembly STEP](exports/rotary-table/rt01-assembly.step), [metal parts](exports/rotary-table/metal/), [seal profiles](exports/rotary-table/seal-profiles.step) — bought devices are labelled simplified envelopes; STEP files are not tolerance drawings.
- [Arm source](references/so-arm100/README.md), [mount coordinates](cad/arm-mount-reference.json), [historical designs](docs/archive/) — preserved reference/context.

![Metal core and drive interfaces](docs/rotary-table-internals.png)

## Working on the model

Units are millimetres. Use the SolidCraft MCP/CLI to preserve named features/components. Update the governing specification, register, checks and exports together. `scripts/rebuild_assembly.py` generates a separate candidate around the existing arm; `cad/rotary-table-build.json` builds the table alone. Regeneration commands are in the printing guide. Do not replace the main assembly with a standalone build or save temporary probe hardware into it.

The dust/splash design uses an overlapping skirt, fixed upstand/gutter, sealed static seams and gasketed electronics box. It needs physical ingress/temperature testing. Scaling requires new loads, fits, drive/bearing sizes and structural calculations; uniform scaling of this model is not supported.

![Braced stand with independent electronics enclosure](docs/rotary-table-arm-stand.png)
