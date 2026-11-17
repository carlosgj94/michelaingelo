#!/usr/bin/env python3
"""Generate the RT-01 hardware register and purchasing totals from joint records.
Dimensions are nominal mm. The register is a prototype specification, not a release.
"""
from collections import Counter
import csv, json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
rows=[]
CAP='ISO 4762 socket cap'; BUTTON='ISO 7380-1 button'; CSK='DIN 7991 90-degree countersunk'
W3='M3 washer ID3.2 OD7 x 0.5';W4='M4 washer ID4.3 OD9 x 0.8';W5='M5 washer ID5.3 OD10 x 1';W6='M6 washer ID6.6 OD18 x 1.6'
N3='M3 DIN 985 nyloc nut h4';N4='M4 DIN 985 nyloc nut h5';N6='M6 DIN 985 nyloc nut h6'
P4='M4 DIN 934 plain nut AF7 h3.2';P5='M5 DIN 934 plain nut AF8 h4'
I3='ruthex RX-M3x5.7 heat-set insert'
def add(id,joint,qty,d,L,head,hardware,stack,location,status='Defined geometry'):
 rows.append(dict(id=id,joint=joint,quantity=qty,thread=f'M{d}',pitch_mm={3:.5,4:.7,5:.8,6:1}[d],length_mm=L,head=head,hardware_per_joint=hardware,stack_and_assembly=stack,location=location,status=status))
add('F01','Core columns: M02 / metal tubes / M01',4,6,90,CAP,{'M6 small washer ID6.4 OD11 x 1.6':1},'Seat Z91.6; tip Z1.6. Seat 8 + tube 70 + washer 1.6; 8 mm tapped M01 engagement. Bolt tip stays 1.6 above bench. Clamp metal, not P11-14 sleeves.','(66,0), (-66,0), (36,-58), (-36,-58)')
add('F02','Core to bench',4,6,None,CAP,{W6:1,'M6 fender washer ID6.6 OD24 x 2':1,N6:1},'L >= T + 23.6; round up to next available 5 mm. Includes core/spacer 12, washers 3.6, nut 6, two pitches 2. P20 has Ø25 head access openings over Y+64; tighten these before the worm supports are fitted. Nominal head top19.6 is0.4 below blocks.','X +/-64, Y +/-64','Bench thickness required')
add('F03','Outer bearing to M02',8,5,25,CAP,{W5:1,P5:1},'Head seat Z99.6; tip74.6; underside washer81-82, nut77-81. 2.4 mm projection. No washer in bearing head counterbore. Fit nuts before enclosing the core.','PCD105, phase22.5 deg','Confirm purchased bearing drawing')
add('F04','P30 to inner bearing',8,5,20,CAP,{},'Head seat110, tip90: 15 mm thread into bearing envelope. No washer in recessed head. Confirm actual ring tapping and supplier screw class before ordering.','PCD65, phase0 deg','Confirm purchased bearing drawing')
add('F05','P30 metal sleeves to wheel',4,5,45,CAP,{},'Head seat110; sleeve36 down to74; tip65 gives 9 mm engagement and 3 mm to blind-hole bottom62. M5x50 is too long. No head washer.','PCD30 at cardinal points','Confirm wheel machining')
add('F06','Four platter quadrants to P30',8,5,25,BUTTON,{P5:1},'Seat125, head <=2.75 high in 3 mm recess. Nut106.4-110.4; tip100. Install nuts before hub assembly. No head washer.','( +/-65, +/-22 ) and ( +/-22, +/-65 )')
add('F07','Worm sled to M01',4,5,16,CAP,{W5:1},'Seat21, tip5; 7 mm engagement in M01. Washer bridges 5.5 mm slot width. Adjust cartridge before tightening; screws now outside bearing-block/cap tool paths.','Front X +/-52, Y18; rear X +/-70, Y92')
add('F08','Worm blocks to sled',4,5,65,CAP,{W5:1,P5:1},'Washer seats73.5, head74.5-79.5 in new recess; tip9.5. Captive nut12.4-16.4. Base tip relief slots reach7.5 and allow +/-3 axial adjustment. Tighten BEFORE fitting M02; insert nuts before fitting sled.','X +/-53, Y31.5/79.5')
add('F09','Worm bearing retainer caps',8,4,35,CAP,{W4:1,P4:1},'Cap4 + block26; nut in 4.4 mm recess on inside face. Bolt extends4.2 past inner block face. Nut pockets take plain nuts, not nylocs.','Both X faces; Y32.5/78.5, Z27/73')
add('F10','Motor bracket to P23',4,5,20,CAP,{W5:1,P5:1},'Seat21, tip1. Nut4.4-8.4. M40 through-reliefs clear the tips, which remain1 above bench. Fit captive nuts before sole.','X116/138, Y32/79')
add('F11','NEMA17 face to bracket',4,3,10,CAP,{W3:1},'Bracket6 + washer0.5; motor thread penetration3.5. Confirm permissible depth with selected motor.','AxisX; Y40/71, Z34.5/65.5','Confirm motor SKU')
add('F12','Home bracket to M02',2,3,12,BUTTON,{W3:1},'Foot6 + washer0.5, thread engagement5.5. Head top98.15 below rotating platter screw tips100. Mount now rotated -45 deg away from column bolt.','(-70,+/-6) rotated -45 deg about table centre')
add('F13','M40 sole to M01',2,5,12,CSK,{},'Overall length includes head. Head recessed ~0.2 from underside Z0; tip~12.2, full 8 mm thread in M01. P20 has 1 mm underside tip-relief slots allowing +/-3 axial adjustment. Head diameter <=10; no washer. Install from underside before bench anchoring.','X72, Y20/48')
add('F14','Motor pod to bench',2,6,None,CAP,{W6:1,'M6 fender washer ID6.6 OD24 x 2':1,N6:1},'L >= T + 23.6. Sole4 + metal sleeve8; same remaining stack as F02. Existing B41-42 washers are included, not additional.','X220, Y35/77','Bench thickness required')
add('F15','Fixed housing seam strips',16,4,25,CAP,{W4:2,N4:1},'Two printed flanges total16; washers1.6 + nut5; tip projection2.4. Use low clamp force. These are M4, not the old BOM M3.','Four seams; two holes at each of Z25 and90')
add('F16','Fixed housing to bench',4,5,None,CAP,{'M5 DIN 9021 washer ID5.3 OD15 x 1.2':2,'M5 DIN 985 nyloc nut h5':1},'L >= T + 11.5 (floor2.5, washers2.4, nut5, two pitches1.6). Nonstructural cover clamping only.','(105,105) rotated0/90/180/270 deg','Bench thickness required')
add('F17','Motor hood to foundation',4,4,95,CAP,{W4:1,P4:1},'Seat96.3; tip1.3. Nut4.4-7.6. Sole holes clear tips. Length95 is non-preferred: cut/deburr a100 mm screw to95 if unavailable; retain >=12 mm threaded tip.','X171/225, Y21/91')
add('F18','Electronics lid',10,3,10,BUTTON,{W3:1,I3:1},'Seat108.5; tip98.5; insert flush104 down98.3, engagement5.5. 7 mm pilot depth. Fit inserts flush and coupon-check retention.','Ten lid points; matching Ø8 access holes in M50')
add('F19','Controller tray',4,3,10,BUTTON,{W3:1,I3:1},'Seat82.5; tip72.5. Insert79 down73.3, engagement5.7; tip remains1.5 above pilot floor71.','X +/-65, Y-258/-190')
add('F20','Heat spreader to box floor',4,3,16,CSK,{W3:1,N3:1,'EPDM seal washer OD7 ID3.2 x 1 (0.75 compressed)':1,'Metal compression shim OD6.5 ID3.4 x 0.75':1},'Head diameter <=6, recessed ~0.2 below spreader top35.75. Tip~19.55, nut22.75-26.75. Seal washer and metal washer below floor28; shim above floor32. Shim M31-34 counted here. Keep screw flush below driver envelope.','X +/-55.5, Y-258.5/-189.5')
add('F21','Electronics feet and box to bench',4,4,None,CAP,{W4:1,'M4 fender washer ID4.3 OD12 x 1':1,N4:1},'L >= T + 40.2 (feet28 + floor4 + washers1.8 + nut5 + two pitches1.4). Install before electronics; avoid compressing PETG.','X +/-75, Y-271/-177','Bench thickness required')
add('F22','M50 to steel stand top flanges',4,6,25,CAP,{W6:2,N6:1},'Plate8 + flange4 + washers3.2 + nut6; projection3.8. Head seat145.6, tip120.6. Existing B51-54 top washers are included.','X +/-98, Y-272/-176')
add('F23','Steel stand bottom flanges to bench',4,6,None,CAP,{W6:2,N6:1},'L >= T + 18.2 (flange4, washers3.2, backing strip3, nut6, two pitches2). Two shared steel strips40x136x3 under bench, holes96 apart.','X +/-98, Y-272/-176','Bench thickness required')
add('F24','SO100 base to M50',4,4,35,CAP,{W4:2,N4:1},'Nominal imported foot16 + plate8 + washers1.6 + nut5; projection4.4. Head seat160.8, tip125.8. Verify owned arm revision and flat washer seating; arm internal screws excluded.','Measured nonrectangular four-hole pattern in arm-mount-reference.json','Verify physical arm foot')
pending=[
 ('Workholding','Four M6 DIN 934 captive nuts AF10 h5 are specified in P30; fixture screw lengths, washers and clamps depend on the fixture. Do not bottom against fixed core.'),
 ('Worm shaft retention','Key sizes, shaft shoulders, bearing preload locknut(s), spacers and retaining screws require a finished shaft drawing; quantity/length unknown.'),
 ('Coupling','Clamping screws supplied with selected coupling; quantity and torque unknown until SKU is selected.'),
 ('Home sensor and target','Two sensor jam nuts normally supplied with sensor; confirm thread (often M8x1). Steel target retention/adhesive and sensor tip clearance remain to select.'),
 ('Driver / controller','Board mounting screw and standoff patterns unselected. The 14 lid/tray screws do not fasten the boards.'),
 ('Heat sink','B27 represents thermal adhesive pad, not verified structural retention. Select rated adhesive or mechanical retention and any fasteners with final heat sink.'),
 ('Optional encoder / external devices','Encoder mounting, PSU, E-stop and cable clamps depend on selected devices. Not included in fixed quantities.'),
 ('Stand fabrication','Two side channels and front brace are welded, not screwed together. Fabricator must specify weld size/process, finish datums and inspect distortion. No unlisted hidden frame screws.')]
meta=dict(design='RT-01',revision=3,units='mm',date='2026-11-17',status='Prototype register; not a complete order release',bench_thickness_symbol='T',excludes='All purchased-arm internal screws; includes four arm base attachments',rows=rows,pending=[dict(interface=a,remaining=b) for a,b in pending])
(ROOT/'cad/fasteners.json').write_text(json.dumps(meta,indent=2)+'\n')
totals=Counter();conditional=Counter()
for r in rows:
 if r['length_mm'] is not None:
  key=f"{r['thread']}x{r['length_mm']} {r['head']}"
  totals[key]+=r['quantity']
  if r['status']!='Defined geometry':conditional[key]+=r['quantity']
 for key,n in r['hardware_per_joint'].items():totals[key]+=r['quantity']*n
# Fixture nuts are defined even though the matching bolts are not.
totals['M6 DIN 934 plain nut AF10 h5']+=4
with (ROOT/'cad/fastener-shopping-list.csv').open('w',newline='') as f:
 w=csv.writer(f,lineterminator='\n');w.writerow(['item','installed_quantity','conditional_screw_quantity','note'])
 for k,v in sorted(totals.items()):w.writerow([k,v,conditional[k],'No spares included; provisional interfaces per register'])
 for r in rows:
  if r['length_mm'] is None:w.writerow([r['thread']+' bench bolt / '+r['id'],r['quantity'],r['quantity'],'Choose length after measuring T; see register'])
 w.writerow(['Steel backing strip 40x136x3, 2x Ø6.6 holes96 apart',2,0,'F23; fabrication drawing, not placed at an invented bench thickness'])
lines=['# RT-01 assembly fastener register — revision 3','',
'Updated 2026-11-17. **This replaces the earlier incomplete fastener notes.** It covers every currently designed assembly joint, including the arm-to-stand bolts, and excludes the arm’s internal screws. Unfinished component interfaces are listed at the end: the whole machine is not yet an order-ready screw kit.','',
'All dimensions are mm. Coarse threads: M3×0.5, M4×0.7, M5×0.8, M6×1. Length is under-head except countersunk screws, where it includes the head. Use exact head styles: a cap head cannot replace a recessed platter button head. Countersinks are for DIN7991 heads (M3 <=Ø6; M5 <=Ø10); do not substitute larger ISO10642 heads without revising the recess. Nominal fits are checked in CAD; printed tolerances require the coupon.','',
'Prototype baseline: corrosion-protected class 8.8 steel bolts / compatible nuts for metal frame and datum joints; A2-70 stainless for cover/electronics fasteners. Bearing screws must follow the selected bearing supplier’s class and torque. Keep coatings out of bearing seats; select corrosion protection compatible with aluminium and the wet environment. Do not use metal-joint torque tables on PETG, heat-set inserts or the printed arm. Final preload/torque requires supplier data and coupon/assembly checks. Plain captive nuts need a validated anti-loosening method compatible with PETG; do not substitute taller nylocs in their shallow pockets.','',
'## Installed quantities by joint','',
'| ID | Joint | Qty | Screw | Mating hardware per screw | Status |','| --- | --- | ---: | --- | --- | --- |']
for r in rows:
 length=str(r['length_mm']) if r['length_mm'] else 'L(T)'
 hw='; '.join(f'{v} × {k}' for k,v in r['hardware_per_joint'].items()) or 'Tapped metal; no washer'
 lines.append(f"| {r['id']} | {r['joint']} | {r['quantity']} | {r['thread']} × {length}, {r['head']} | {hw} | {r['status']} |")
lines+=['','## Stack, location and assembly access','']
for r in rows:lines += [f"**{r['id']} — {r['joint']}.** {r['stack_and_assembly']} Location: {r['location']}.",'']
lines+=['## Bench anchors','',
'T is the measured solid bench-top thickness at each hole. Round each minimum up to the next available length, then verify full nut engagement and underside clearance. A 30 mm top is only an example, not a chosen workbench. Use a rigid, braced table shared by the arm stand and rotary core. Through-bolts and backing hardware do not make a flexible or loose tabletop rigid. Avoid chipboard/loose timber blocks as the assumed precision datum.','',
'| Joint | Quantity | Minimum under-head length | Example only: T=30 |','| --- | ---: | --- | --- |',
'| Core F02 | 4 M6 | T+23.6 | 55 |','| Motor pod F14 | 2 M6 | T+23.6 | 55 |','| Housing F16 | 4 M5 | T+11.5 | 45 |','| Box F21 | 4 M4 | T+40.2 | 75 |','| Arm stand F23 | 4 M6 | T+18.2 | 50 |','',
'Two 40 × 136 × 3 steel backing strips go below the stand flanges. Each has two Ø6.6 holes on its centreline, 96 apart and 20 from the ends. The separate STEP is at a manufacturing origin, not positioned under an assumed bench. Add suitable backing under other anchors if the chosen top needs it and add that thickness to their formula.','',
'## Still to finish before ordering all hardware','']
for a,b in pending:lines.append(f'- **{a}:** {b}')
lines+=['','## Totals and sources','',
'[Machine-readable joint records](../cad/fasteners.json) and [consolidated purchasing CSV](../cad/fastener-shopping-list.csv) are generated by `scripts/build_fastener_register.py`. Quantities are installed counts, with no spares. Existing model washers B41–42/B51–54 and compression shims M31–34 are counted once. The CSV retains conditional screw quantities and separates thickness-dependent bench bolts.','',
'- [ruthex RX-M3x5.7](https://www.ruthex.de/products/ruthex-gewindeeinsatz-m3-100-stuck-rx-m3x5-7-messing-gewindebuchsen): selected insert size; nominal Ø4 pilot, coupon verification required.','- [Accu DIN7991 M3 dimensions](https://www.accu.co.uk/api/product-datasheet?id=625698) and [BelMetric DIN7991 M5 drawing](https://belmetric.com/content/A-PDF_Drawings/SF5X10.pdf): head-size limits used in the countersink checks.','- [TR Fastenings cap-screw dimensional catalog](https://www.trfastenings.com/Products/Catalogue/Screws-and-Bolts/news/Hexagon-Socket-Screws/Cap-Head/Cart/TR00005910-299): ISO4762/DIN912, 95 mm is non-preferred.','- [Universal Robots stand guidance](https://www.universal-robots.com/manuals/EN/HTML/SW5_24/Content/prod-usr-man/complianceUR8Long/H_g5_sections/mechanical_interface_g5/dimension_stand.htm): moving/stopping torques act on the stand. This supports the braced/anchored load path; UR load ratings are not applied to the SO100.','']
(ROOT/'docs/rotary-table-fasteners.md').write_text('\n'.join(lines))
print(json.dumps(dict(joint_rows=len(rows),fixed_length_screws=sum(r['quantity'] for r in rows if r['length_mm']),bench_bolts=sum(r['quantity'] for r in rows if not r['length_mm']),purchasing_lines=len(totals))))
