#!/usr/bin/env python3
"""Generate the RT-01 hardware register and purchasing totals from joint records.
Dimensions are nominal mm. The register is a prototype specification, not a release.
"""
from collections import Counter
import csv, json, math, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
revision=json.loads((ROOT/'cad/parts.json').read_text())['revision']
rows=[]
def readable(s):
 return re.sub(r'(?<![\w/.-])([a-z]{2,})(?=\d)', lambda m: m.group(1) if m.group(1) in {'rt','so','arm','python','rev'} else m.group(1)+' ', s)
CAP='ISO 4762 socket cap'; BUTTON='ISO 7380-1 button'; CSK='DIN 7991 90-degree countersunk'
W3='M3 washer ID3.2 OD7 x 0.5';W4='M4 washer ID4.3 OD9 x 0.8';W5='M5 washer ID5.3 OD10 x 1';W6='M6 washer ID6.6 OD18 x 1.6'
N3='M3 DIN 985 nyloc nut h4';N4='M4 DIN 985 nyloc nut h5';N6='M6 DIN 985 nyloc nut h6'
P4='M4 DIN 934 plain nut AF7 h3.2';P5='M5 DIN 934 plain nut AF8 h4'
I3='ruthex RX-M3x5.7 heat-set insert'
def add(id,joint,qty,d,L,head,hardware,stack,location,status='Defined geometry'):
 rows.append(dict(id=id,joint=joint,quantity=qty,thread=f'M{d}',pitch_mm={3:.5,4:.7,5:.8,6:1}[d],length_mm=L,head=head,hardware_per_joint=hardware,stack_and_assembly=readable(stack),location=readable(location),status=status))
add('F01','Core columns: M02 / locating columns / M01',4,6,90,CAP,{'M6 small washer ID6.4 OD11 x 1.6':1},'Head seat91.6; tip1.6. Columns72 locate1 into each plate; visible span70. Local M01 bosses provide9 mm full M6 engagement below the locating recess. Clamp the matched metal columns, not the69.5 mm printed sleeves.','(66,0), (-66,0), (36,-58), (-36,-58)')
add('F02','Core to bench',4,6,None,CAP,{W6:1,'M6 fender washer ID6.6 OD24 x 2':1,N6:1},'L >= T + 23.6; round up to next available 5 mm. Includes core/spacer 12, washers 3.6, nut 6, two pitches 2. Tighten all four anchors BEFORE installing M60: its integral blocks obstruct the two Y+64 key paths even with shaft/bearings removed. Retorque requires removing M60 and the upper core/drivetrain parts that obstruct its removal, then rechecking carrier alignment and backlash after refitting. The Ø25 pockets are cut after the blocks are joined to a Z21 ceiling, leaving1.4 mm nominal clearance above the Z19.6 heads; they are head reliefs, not through-tool openings. Verify actual head/washer thickness and datum tolerances before assembly.','X +/-64, Y +/-64','Bench thickness required')
add('F03','Outer bearing to M02',8,5,25,CAP,{W5:1,P5:1},'Head seat Z99.6; tip74.6; underside washer81-82, nut77-81. 2.4 mm projection. No washer in bearing head counterbore. Fit nuts before enclosing the core.','PCD105, phase22.5 deg','Confirm purchased bearing drawing')
add('F04','M20 to inner bearing',8,5,20,CAP,{},'Head seat110, tip90;15 mm engagement in the bearing reference. M20 has a measured-fit bearing pilot. No head washer. Verify purchased ring tapping and bolt class/torque.','PCD65, phase0 deg','Confirm purchased bearing drawing')
add('F05','M20 metal hub to wheel',4,5,45,CAP,{},'Seat110; solid metal grip36 down to wheel face74; tip65 gives9 mm thread engagement and3 mm blind-bottom clearance. No sleeves or head washers. M21 drive pin supplies positive torque transfer; pilots locate the axes. Final wheel thread capacity and preload require fabricator approval.','PCD30 cardinal points','Confirm wheel machining and preload')
add('F06','Four platter quadrants to M20',8,5,16,BUTTON,{},'Seat125; tip109 gives7 mm engagement below the Z116 hub face. Button head <=2.75 high in3 mm recess. No captive nuts or head washers. Do not substitute the old25 mm screws.','( +/-65, +/-22 ) and ( +/-22, +/-65 )')
add('F07','Monolithic worm carrier to M01',4,5,16,CAP,{W5:1},'Seat21, tip5;7 mm engagement in M01. Four X slots permit +/-3 mm adjustment; the machined tongue/groove controls Y and yaw. No separate bearing-block bolts.','Front X +/-52,Y18; rear X +/-70,Y92')
add('F09','Metal worm bearing retainers to carrier',8,4,12,CAP,{W4:1},'Cap4 + selected shim nominal0.05 + washer0.8 gives7.15 mm thread engagement. Specify9 mm full M4 thread and10 mm drilled depth in the carrier. Select shim from measured pocket/bearing/boss stack; do not set shaft preload with the cap screws. No nuts.','Both X faces; Y32.5/78.5,Z27/73')
add('F10','Printed motor bracket to M40 metal riser',4,5,20,CAP,{W5:1},'Seat21, tip1;11 mm thread engagement in the integral metal riser/sole. No captive nuts. Tightening is limited by the printed bracket and must be validated on a first article.','X116/138,Y32/79')
add('F11','NEMA17 face to bracket',4,3,10,CAP,{W3:1},'Bracket6 + washer0.5; motor thread penetration3.5. Confirm permissible depth with selected motor.','AxisX; Y40/71, Z34.5/65.5','Confirm motor SKU')
add('F13','M40 stepped support to M01',2,5,12,CSK,{},'Overall length includes head. Head recessed ~0.2 from underside Z0; tip~12.2, full 8 mm thread in M01. M60 has 1 mm underside tip-relief slots allowing +/-3 axial adjustment. Head diameter <=10; no washer. Install from underside before bench anchoring.','X72, Y20/48')
add('F14','Integral metal motor support to bench',2,6,None,CAP,{W6:1,'M6 fender washer ID6.6 OD24 x 2':1,N6:1},'L >= T +23.6. Integral metal support is12 mm at these holes. No printed clamp stack or compression sleeves. B41-42 top washers counted here once.','X220,Y35/77','Bench thickness required')
add('F15','Fixed housing seam strips',16,4,25,CAP,{W4:2,N4:1},'Strip8 + housing flange8 =16 grip. Outer washer seats on the new diameter10 flat at local Y153. Washers1.6 + nut5 leave2.4 mm tip projection. Use low clamp force and seal the static seams.','Four seams; X +/-6, Z25/90 in each local seam frame')
add('F16','Fixed housing to bench',4,5,None,CAP,{'M5 DIN 9021 washer ID5.3 OD15 x 1.2':2,'M5 DIN 985 nyloc nut h5':1},'L >= T +11.5. Floor2.5, washers2.4,nut5,two pitches1.6. Entire OD15 top washer sits on the floor, clear of the motor passage and curved wall.','(88,108) rotated0/90/180/270 deg','Bench thickness required')
add('F17','Motor hood to integral metal support',4,4,95,CAP,{W4:1},'Seat96.3; tip1.3;12.2 mm thread engagement below the Z13.5 hard stop. No captive nuts. Cut/deburr100 mm to95 only if required; keep at least16 mm threaded tip.','X171/225,Y21/91')
add('F18','Electronics lid',10,3,10,BUTTON,{W3:1,I3:1},'Seat108.5; tip98.5; insert flush104 down98.3, engagement5.5. 7 mm pilot depth. Fit inserts flush and coupon-check retention.','Ten lid points; matching Ø8 access holes in M50')
add('F19','Controller tray',4,3,10,BUTTON,{W3:1,I3:1},'Seat82.5; tip72.5. Insert79 down73.3, engagement5.7; tip remains1.5 above pilot floor71.','X +/-65, Y-258/-190')
add('F20','Heat spreader to box floor',4,3,16,CSK,{W3:1,N3:1,'EPDM seal washer OD7 ID3.2 x 1 (0.75 compressed)':1,'Metal compression shim OD6.5 ID3.4 x 0.75':1},'Head diameter <=6, recessed ~0.2 below spreader top35.75. Tip~19.55, nut22.75-26.75. Seal washer and metal washer below floor28; shim above floor32. Shim M31-34 counted here. Keep screw flush below driver envelope.','X +/-55.5, Y-258.5/-189.5')
add('F21','Electronics feet and box to bench',4,4,None,CAP,{W4:1,'M4 fender washer ID4.3 OD12 x 1':1,N4:1,'EPDM seal washer OD9 ID3.8 x 1 (0.75 compressed)':1},'REVERSED: head and OD12 fender washer BELOW the bench; M4 nyloc nut captured above the box floor. L >= T +40.95 (feet28 + floor4 + underside washer1 + seal0.75 + top washer0.8 + nut5 + two pitches1.4), rounded to the next suitable length. Floor stays4 thick. Slide the uncompressed seal and OD9 washer inward-to-outward through the2 mm-high loading slot, then drop an AF7 x5 nut into the AF7.4 pocket from inside the open box. Installed seal Z32-32.75, washer32.75-33.55, nut33.55-38.55. Insert bolt upward and tighten/retorque from below; no straight tool approach through the rim is assumed. Validate seal imprint and low clamp torque on PETG; do not use steel-joint torque.','X +/-75, Y-271/-177','Bench thickness required')
add('F22','M50 to steel stand top flanges',4,6,25,CAP,{W6:2,N6:1},'Plate8 + flange4 + washers3.2 + nut6; projection3.8. Head seat153.6, tip128.6. Existing B51-54 top washers counted here once.','X +/-98,Y-272/-176')
add('F23','Steel stand bottom flanges to bench',4,6,None,CAP,{W6:2,N6:1},'L >= T + 18.2 (flange4, washers3.2, backing strip3, nut6, two pitches2). Two shared steel strips40x136x3 under bench, holes96 apart. Each strip has two Ø16 scallops centred23 mm inboard of its hole line and at Y +/-47 relative to the strip centre. Install scalloped edges toward the electronics box; rotate the second identical strip180 deg about Z. Scallops clear all four reversed F21 OD12 underside washers by2 mm while retaining complete F23 OD18 washer seats.','X +/-98, Y-272/-176','Bench thickness required')
add('F24','SO100 base to M50 top-down tapped threads',4,4,23.5,CAP,{W4:1},'CONDITIONAL cut-length example only: nominal head seat168.8 and screw23.5 give tip145.3 and6.7 mm penetration into M50 from Z152. Cut/deburr a25 mm screw only after measuring the owned foot and matched upper seating detail. Let G be measured grip from M50 top to head seat: require L-G=6.5-7.0 mm penetration, at least6.0 mm effective full thread after entry/tip runout, and tip at or above Z145 (at least1 mm recessed from underside144). M50 has four M4x0.7-6H through threads. No lower washer or nut; do not reinstall the old35 mm screws. Upper OD9 washer has no validated seat on the imported foot: each site needs a matched supported seating detail from physical measurement, witness contact and preload-retention tests before release. The nominal head/washer envelope is packaging evidence only, not proof of contact. Keep arm bottomZ152; internal arm screws excluded.','Nonrectangular pattern in arm-mount-reference.json','Measure owned foot seats and screw length')
add('F25','Steel home target to M20',1,3,8,CSK,{},'Upward screw, head recessed0.1 atZ99.8; tip107.8. Target3 mm leaves5.1 mm engagement into hub boss fromZ102.7. Head diameter <=6. Do not use stainless target material without rechecking sensing range.','Radius73, angle210 deg')
non_screw_hardware=[dict(id='H01',item='M8x1 sensor jam nut AF13, thickness <=4 mm',quantity=2,note='Supplied with selected SICK sensor; modeled at4 mm'),dict(id='H02',item='Ground steel drive pin nominal diameter4 x12',quantity=1,note='M21, matched press fit and tangential slot clearance'),dict(id='H03',item='Metal retainer shim M62, nominal0.05 mm, select after measurement',quantity=2,note='Outer-race axial retention; not shaft preload')]
pending=[
 ('Workholding','Four blind M6 metal threads start atZ121 with9 mm full thread. Require8–9 mm engagement: bolt length minus fixture/washer stack aboveZ128 must be15–16 mm. Example M6x20 requires4–5 mm upper stack. Verify every actual clamp; never force a screw against a blind bottom. No M6 captive nuts remain.'),
 ('Worm shaft retention','Key sizes, shaft shoulders, bearing preload locknut(s), spacers and retaining screws require a finished shaft drawing; quantity/length unknown.'),
 ('Coupling','Clamping screws supplied with selected coupling; quantity and torque unknown until SKU is selected.'),
 ('Home sensor','Mechanical reference SICK IME08-02BPSZT0S, M8x1, two AF13 nuts and F25 retained mild-steel target. Select mating cordset, confirm supplied nut thickness <=4 mm, set gap1.2 mm, and test one home transition per revolution. PNP output needs a compatible input interface.'),
 ('Driver / controller','Board mounting screw and standoff patterns unselected. The 14 lid/tray screws do not fasten the boards.'),
 ('Heat sink','B27 represents thermal adhesive pad, not verified structural retention. Select rated adhesive or mechanical retention and any fasteners with final heat sink.'),
 ('Optional encoder / external devices','Encoder mounting, PSU, E-stop and cable clamps depend on selected devices. Not included in fixed quantities.'),
 ('Stand fabrication','Two side channels and front brace are welded, not screwed together. Fabricator must specify weld size/process, finish datums and inspect distortion. No unlisted hidden frame screws.')]
pending=[(a,readable(b)) for a,b in pending]
for item in non_screw_hardware:
 item['item']=readable(item['item']); item['note']=readable(item['note'])
meta=dict(design='RT-01',revision=revision,units='mm',date='2026-11-18',status='Prototype register; not a complete order release',bench_thickness_symbol='T',excludes='All purchased-arm internal screws; includes four arm base attachments',rows=rows,non_screw_hardware=non_screw_hardware,retired_ids=['F08','F12'],pending=[dict(interface=a,remaining=b) for a,b in pending])
(ROOT/'cad/fasteners.json').write_text(json.dumps(meta,indent=2)+'\n')
totals=Counter();conditional=Counter()
for r in rows:
 if r['id']=='F24':
  key='M4 ISO 4762 socket cap, finish to measured length / F24'
  totals[key]+=r['quantity'];conditional[key]+=r['quantity']
 elif r['length_mm'] is not None:
  key=f"{r['thread']}x{r['length_mm']} {r['head']}"
  totals[key]+=r['quantity']
  if r['status']!='Defined geometry':conditional[key]+=r['quantity']
 for key,n in r['hardware_per_joint'].items():totals[key]+=r['quantity']*n
for item in non_screw_hardware:totals[item['item']]+=item['quantity']
with (ROOT/'cad/fastener-shopping-list.csv').open('w',newline='') as f:
 w=csv.writer(f,lineterminator='\n');w.writerow(['item','installed_quantity','conditional_screw_quantity','note'])
 for k,v in sorted(totals.items()):
  note='Measure owned foot and fitted seat before selecting and finishing length' if k.endswith('/ F24') else 'No spares included; provisional interfaces per register'
  w.writerow([k,v,conditional[k],note])
 for r in rows:
  if r['length_mm'] is None:w.writerow([r['thread']+' bench bolt / '+r['id'],r['quantity'],r['quantity'],'Choose length after measuring T; see register'])
 w.writerow(['M55 steel backing strip 40x136x3 with two Ø16 scallops',2,0,'F23; orient scallops inward per fabrication drawing'])
lines=[f'# RT-01 assembly fastener register — revision {revision}','',
'Updated 2026-11-18. Includes the four arm mounting screws. The arm’s internal screws are outside the RT-01 order. Final selections and fit measurements are listed below.','',
'All dimensions are mm. Coarse threads: M3×0.5, M4×0.7, M5×0.8, M6×1. Length is under-head except countersunk screws, where it includes the head. Use exact head styles: a cap head cannot replace a recessed platter button head. Countersinks are for DIN7991 heads (M3 <=Ø6; M5 <=Ø10); do not substitute larger ISO10642 heads without revising the recess. Nominal fits are checked in CAD; printed tolerances require the coupon.','',
'Prototype hardware uses corrosion-protected class 8.8 steel bolts and compatible nuts for metal frame and datum joints, with A2-70 stainless for covers and electronics. Bearing screws follow the selected supplier’s class and torque. Determine clamp load for PETG, heat-set inserts, the F21 nut traps and the arm foot by testing their actual assemblies. Verify the locking method is compatible with nearby PETG and seals.','',
'## Installed quantities by joint','',
'| ID | Joint | Qty | Screw | Mating hardware per screw | Status |','| --- | --- | ---: | --- | --- | --- |']
for r in rows:
 length='L(G)' if r['id']=='F24' else str(r['length_mm']) if r['length_mm'] else 'L(T)'
 hw='; '.join(f'{v} × {k}' for k,v in r['hardware_per_joint'].items()) or 'Tapped metal; no washer'
 lines.append(f"| {r['id']} | {r['joint']} | {r['quantity']} | {r['thread']} × {length}, {r['head']} | {hw} | {r['status']} |")
lines+=['','F08 (separate block bolts) and F12 (printed sensor bracket bolts) are deleted in revision4; IDs are not reused.','', '## Other retained hardware','']
for item in non_screw_hardware:lines.append(f"- **{item['id']}**: {item['quantity']} × {item['item']}. {item['note']}.")
lines+=['','## Stack, location and assembly access','']
for r in rows:lines += [f"**{r['id']} — {r['joint']}.** {r['stack_and_assembly']} Location: {r['location']}.",'']
lines+=['## Bench anchors','',
'T is the measured solid bench-top thickness at each hole. Round each minimum up to the next available length, then verify full nut engagement and underside clearance. A 30 mm top is only an example, not a chosen workbench. Use a rigid, braced table shared by the arm stand and rotary core. Through-bolts and backing hardware do not make a flexible or loose tabletop rigid. Avoid chipboard/loose timber blocks as the assumed precision datum.','',
'| Joint | Quantity | Minimum under-head length | Example only: T=30 |','| --- | ---: | --- | --- |',
'| Core F02 | 4 M6 | T+23.6 | 55 |','| Motor pod F14 | 2 M6 | T+23.6 | 55 |','| Housing F16 | 4 M5 | T+11.5 | 45 |','| Box F21 | 4 M4 | T+40.95 | 75 |','| Arm stand F23 | 4 M6 | T+18.2 | 50 |','',
'Install two 40 × 136 × 3 M55 backing strips below the stand flanges. Each has two Ø6.6 holes 96 apart and two Ø16 clearance scallops on its inward edge. Use the F21 and F23 coordinates to lay out the actual bench and inspect the bearing seats. Add any extra bench backing thickness to the applicable bolt formula.','',
'## Still to finish before ordering all hardware','']
for a,b in pending:lines.append(f'- **{a}:** {b}')
lines+=['','## Totals and sources','',
'[Machine-readable joint records](../cad/fasteners.json) and [consolidated purchasing CSV](../cad/fastener-shopping-list.csv) are generated by `scripts/build_fastener_register.py`. Quantities are installed counts, with no spares. Existing model washers B41–42/B51–54 and compression shims M31–34 are counted once. The CSV retains conditional screw quantities and separates thickness-dependent bench bolts.','',
'- [ruthex RX-M3x5.7](https://www.ruthex.de/products/ruthex-gewindeeinsatz-m3-100-stuck-rx-m3x5-7-messing-gewindebuchsen): selected insert size; nominal Ø4 pilot, coupon verification required.','- [Accu DIN7991 M3 dimensions](https://www.accu.co.uk/api/product-datasheet?id=625698) and [BelMetric DIN7991 M5 drawing](https://belmetric.com/content/A-PDF_Drawings/SF5X10.pdf): head-size limits used in the countersink checks.','- [TR Fastenings cap-screw dimensional catalog](https://www.trfastenings.com/Products/Catalogue/Screws-and-Bolts/news/Hexagon-Socket-Screws/Cap-Head/Cart/TR00005910-299): ISO4762/DIN912, 95 mm is non-preferred.','- [Universal Robots stand guidance](https://www.universal-robots.com/manuals/EN/HTML/SW5_24/Content/prod-usr-man/complianceUR8Long/H_g5_sections/mechanical_interface_g5/dimension_stand.htm): moving/stopping torques act on the stand. This supports the braced/anchored load path; UR load ratings are not applied to the SO100.','']
(ROOT/'docs/rotary-table-fasteners.md').write_text('\n'.join(readable(line) for line in lines))
print(json.dumps(dict(joint_rows=len(rows),fixed_length_screws=sum(r['quantity'] for r in rows if r['length_mm'] and r['id']!='F24'),arm_screws_to_fit=4,bench_bolts=sum(r['quantity'] for r in rows if not r['length_mm']),purchasing_lines=len(totals))))
