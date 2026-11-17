#!/usr/bin/env python3
"""Disposable hardware and service probes. Run without --save."""
import json,math
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
parts=[p['name'] for p in json.loads((ROOT/'cad/parts.json').read_text())['parts']]
armdata=json.loads((ROOT/'cad/arm-mount-reference.json').read_text())
arm=armdata['collision_body_names']
rows=json.loads((ROOT/'cad/fasteners.json').read_text())['rows']
HUB='M20 registered output hub';CARRIER='M60 monolithic worm carrier'
sensor=(73*math.cos(math.radians(210)),73*math.sin(math.radians(210)))
C=[];probes=[];exclusions=[];counts=Counter();reasons=[]
def cmd(c,**p):C.append(dict(command=c,params=p))
def cyl(n,d,h,base,axis='Z',op='new'):
 p=dict(diameter=d,height=h,base=base,axis=axis,operation=op)
 p.update(body_name=n) if op=='new' else p.update(targets=[n])
 cmd('solid.cylinder',**p)
def exclude(a,b,reason):exclusions.append([a,b]);reasons.append(dict(a=a,b=b,reason=reason))
def register(n,group=None):
 probes.append(n)
 if group:counts[group]+=1
def screw(n,g,x,y,tip,seat,d,hd,hh,washer=None,ignore=()):
 register(n,g);cyl(n,d,seat-tip,[x,y,tip]);cyl(n,hd,hh,[x,y,seat],op='join')
 if washer:
  od,t=washer;cyl(n,od,t,[x,y,seat-t],op='join')
 for body in ignore:exclude(n,body,'Specified thread engagement; length/depth checked separately')
def collar(n,d,t,x,y,z):cyl(n,d,t,[x,y,z],op='join')
cmd('component.activate',component='root');cmd('component.create',name='Disposable revision 4 hardware',grounded=True)
for i,(x,y) in enumerate([(66,0),(-66,0),(36,-58),(-36,-58)]):screw(f'TEST F01 {i}','F01',x,y,1.6,91.6,6,10,6,(11,1.6),('M01 aluminium base plate',))
for i,(x,y) in enumerate([(x,y) for x in [-64,64] for y in [-64,64]]):screw(f'TEST F02 {i}','F02',x,y,0,13.6,6,10,6,(18,1.6))
for i in range(8):
 a=math.radians(22.5+45*i);x,y=52.5*math.cos(a),52.5*math.sin(a);n=f'TEST F03 {i}'
 screw(n,'F03',x,y,74.6,99.6,5,8.5,5);collar(n,10,1,x,y,81);collar(n,8/math.cos(math.pi/6),4,x,y,77)
for i,(x,y) in enumerate([(-52,18),(52,18),(-70,92),(70,92)]):screw(f'TEST F07 {i}','F07',x,y,5,21,5,8.5,5,(10,1),('M01 aluminium base plate',))
for side in [-1,1]:
 for y in [32.5,78.5]:
  for z in [27,73]:
   n=f'TEST F09 {side} {y} {z}';register(n,'F09');cyl(n,4,12,[-70.85 if side<0 else 58.85,y,z],'X')
   cyl(n,7,4,[-74.85 if side<0 else 70.85,y,z],'X','join');cyl(n,9,.8,[-70.85 if side<0 else 70.05,y,z],'X','join')
   exclude(n,CARRIER,'M4 thread, 7.15 engagement in at least9 full thread')
for i,(x,y) in enumerate([(x,y) for x in [116,138] for y in [32,79]]):screw(f'TEST F10 {i}','F10',x,y,1,21,5,8.5,5,(10,1),('M40 stepped motor support',))
for y in [40,71]:
 for z in [34.5,65.5]:
  n=f'TEST F11 {y} {z}';register(n,'F11');cyl(n,3,10,[123.5,y,z],'X');cyl(n,5.5,3,[120.5,y,z],'X','join');cyl(n,7,.5,[123.5,y,z],'X','join')
  exclude(n,'B06 NEMA17 motor and encoder envelope','Provisional motor screw thread engagement3.5; confirm SKU')
for i,y in enumerate([20,48]):
 n=f'TEST F13 {i}';register(n,'F13');cmd('solid.cone',diameter=10,top_diameter=5,height=2.5,base=[72,y,.2],operation='new',body_name=n)
 cyl(n,5,9.5,[72,y,2.7],op='join');exclude(n,'M01 aluminium base plate','M5 tapped attachment; carrier has tip relief')
for i,y in enumerate([35,77]):screw(f'TEST F14 {i}','F14',220,y,0,13.6,6,10,6) # Existing B41/42 washers.
for q in range(4):
 for x in [-6,6]:
  for z in [25,90]:
   n=f'TEST F15 {q} {x} {z}';register(n,'F15');cyl(n,4,25,[x,136.2,z],'Y');cyl(n,7,4,[x,132.2,z],'Y','join')
   for y in [136.2,153]:cyl(n,9,.8,[x,y,z],'Y','join')
   cyl(n,7/math.cos(math.pi/6),5,[x,153.8,z],'Y','join');cmd('solid.move',bodies=[n],axis=[0,0,1],origin=[0,0,0],angle=f'{90*q} deg')
for q in range(4):
 a=math.radians(90*q);x,y=88*math.cos(a)-108*math.sin(a),88*math.sin(a)+108*math.cos(a)
 screw(f'TEST F16 {q}','F16',x,y,0,3.7,5,8.5,5,(15,1.2))
for i,(x,y) in enumerate([(x,y) for x in [171,225] for y in [21,91]]):screw(f'TEST F17 {i}','F17',x,y,1.3,96.3,4,7,4,(9,.8),('M40 stepped motor support',))
lidpoints=[(x,-224+y) for x,y in [(-78,-50),(78,-50),(-78,50),(78,50),(-42,-51),(42,-51),(-42,51),(42,51),(-79,0),(79,0)]]
for i,(x,y) in enumerate(lidpoints):screw(f'TEST F18 {i}','F18',x,y,98.5,108.5,3,5.7,1.65,(7,.5))
for i,(x,y) in enumerate([(x,y) for x in [-65,65] for y in [-258,-190]]):screw(f'TEST F19 {i}','F19',x,y,72.5,82.5,3,5.7,1.65,(7,.5))
for i,(x,y) in enumerate([(x,y) for x in [-55.5,55.5] for y in [-258.5,-189.5]]):
 n=f'TEST F20 {i}';register(n,'F20');cyl(n,3,14.9,[x,y,19.55]);cmd('solid.cone',diameter=3.4,top_diameter=6,height=1.3,base=[x,y,34.25],operation='join',targets=[n])
 collar(n,7,1.25,x,y,26.75);collar(n,5.5/math.cos(math.pi/6),4,x,y,22.75)
for i,(x,y) in enumerate([(x,y) for x in [-75,75] for y in [-271,-177]]):screw(f'TEST F21 {i}','F21',x,y,0,32.8,4,7,4,(9,.8))
for i,(x,y) in enumerate([(x,y) for x in [-98,98] for y in [-272,-176]]):
 n=f'TEST F22 {i}';screw(n,'F22',x,y,128.6,153.6,6,10,6);collar(n,18,1.6,x,y,138.4);collar(n,10/math.cos(math.pi/6),6,x,y,132.4)
 screw(f'TEST F23 {i}','F23',x,y,0,5.6,6,10,6,(18,1.6))
for i,p in enumerate(armdata['adapter_holes']):
 x,y=p['plate_hole_center_mm'][:2];n=f'TEST F24 {i}';screw(n,'F24',x,y,133.8,168.8,4,7,4,(9,.8));collar(n,9,.8,x,y,143.2);collar(n,7/math.cos(math.pi/6),5,x,y,138.2)
cmd('component.activate',component='RT01 - rotating table')
for i in range(8):
 a=math.radians(45*i);screw(f'TEST F04 {i}','F04',32.5*math.cos(a),32.5*math.sin(a),90,110,5,8.5,5,ignore=('B10 bearing inner ring reference',))
for i,(x,y) in enumerate([(15,0),(0,15),(-15,0),(0,-15)]):screw(f'TEST F05 {i}','F05',x,y,65,110,5,8.5,5,ignore=('B11 duplex wheel envelope',))
for i,(x,y) in enumerate([(x,y) for sx in [-1,1] for sy in [-1,1] for x,y in [(65*sx,22*sy),(22*sx,65*sy)]]):screw(f'TEST F06 {i}','F06',x,y,109,125,5,9.5,2.75,ignore=(HUB,))
n='TEST F25';register(n,'F25');cmd('solid.cone',diameter=6,top_diameter=3.4,height=1.3,base=[*sensor,99.8],operation='new',body_name=n)
cyl(n,3,6.7,[*sensor,101.1],op='join');exclude(n,HUB,'M3 target thread, 5.1 engagement')
for x in [-47,47]:
 for y in [-47,47]:
  n=f'TEST permitted fixture tip {x} {y}';register(n);cyl(n,6,16,[x,y,112]);exclude(n,HUB,'Permitted M6 thread engagement9 from Z121; blind drill bottomZ108.5')
exclude('M21 wheel drive pin',HUB,'Intentional press fit4/3.99; finish to measured pin')
exclude('B04 duplex worm envelope','B11 duplex wheel envelope','Purchased tooth envelopes; no tooth-contact simulation')
for i,a in enumerate(arm):
 for b in arm[i+1:]:exclude(a,b,'Unchanged imported arm self-contacts')
expected={r['id']:r['quantity'] for r in rows};assert dict(counts)==expected,(counts,expected)
allnames=parts+arm+probes;population_end=len(C)
angles=[360*i/17 for i in range(17)];critical={360.,315.,225.,135.,45.}
for x,y in [(66,0),(-66,0),(36,-58),(-36,-58)]:critical.add((math.degrees(math.atan2(y,x))-210)%360)
angles+=sorted(a for a in critical if not any(abs(a-b)<1e-8 for b in angles))
for angle in angles:
 cmd('joint.drive',joint='RT01 vertical C axis',value=angle,quiet=True);cmd('inspect.interference',bodies=allnames,exclude_pairs=exclusions,budget_s=60)
cmd('joint.drive',joint='RT01 vertical C axis',value=0,quiet=True)
moving=[CARRIER]+[f'M61 worm bearing retainer {s}' for s in ['left','right']]+[f'M62 retainer shim {s}' for s in ['left','right']]+[f'B02 worm support bearing {s}' for s in ['left','right']]+['B03 worm shaft reference','B04 duplex worm envelope']+[n for n in probes if n.startswith('TEST F09')]
cmd('component.activate',component='root')
for delta in [3,-6]:
 cmd('solid.move',bodies=moving,translate=[delta,0,0]);cmd('inspect.interference',bodies=allnames,exclude_pairs=exclusions,budget_s=60)
(ROOT/'cad/fastener-clearance-checks.json').write_text(json.dumps(dict(commands=C),indent=2)+'\n')
(ROOT/'cad/hardware-assembly-check.json').write_text(json.dumps(dict(commands=C[:population_end]+[dict(command='inspect.interference',params=dict(bodies=allnames,exclude_pairs=exclusions,budget_s=60))]),indent=2)+'\n')
(ROOT/'cad/hardware-check-coverage.json').write_text(json.dumps(dict(revision=4,groups=dict(counts),retired=['F08','F12'],fixed_and_bench_screws=sum(counts.values()),fixture_tip_bounds=4,permanent_retention=['B13 sensor upper jam nut','B13 sensor lower jam nut','M21 wheel drive pin','M62 retainer shim left','M62 retainer shim right'],angles_deg=angles,cartridge_offsets_mm=[3,-3],exclusions=reasons,limits=['Bench bolts are checked above Z0; unknown bench/backing geometry below Z0 remains a release gate.','Heat-set insert retention inside its pilot requires first-article testing; boss geometry and complete screw stacks are checked.','Unselected board, coupling and shaft-retention fasteners remain explicit open interfaces.']),indent=2)+'\n')
# A08: ordered service poses with lid and tray screws removed.
C=[];cmd('component.activate',component='root');cmd('component.create',name='Disposable service tools',grounded=True)
toolnames=[]
for i,(x,y) in enumerate(lidpoints):
 n=f'TEST lid tool {i}';toolnames.append(n);cyl(n,6,70,[x,y,110.2])
cmd('inspect.clearance',bodies=toolnames,against=['M50 SO100 arm mounting plate','M51 steel side channel left','M51 steel side channel right','M52 steel front X brace']+arm,nearest=1)
def check(moving,removed=()):cmd('inspect.clearance',bodies=moving,against=[n for n in parts+arm if n not in moving and n not in removed],nearest=2)
lid=['P52 electronics lid','B24 lid gasket'];cmd('solid.move',bodies=lid,translate=[0,0,8]);check(lid)
for dy in [-40,-40,-60]:cmd('solid.move',bodies=lid,translate=[0,dy,0]);check(lid)
cmd('solid.move',bodies=lid,translate=[300,0,0])
tray=['P51 removable controller tray','B23 controller packaging envelope'];cmd('solid.move',bodies=tray,translate=[0,0,27]);check(tray,lid)
for dy in [-40,-40,-60]:cmd('solid.move',bodies=tray,translate=[0,dy,0]);check(tray,lid)
cmd('solid.move',bodies=tray,translate=[300,0,0])
driver=['B22 driver packaging envelope'];cmd('solid.move',bodies=driver,translate=[0,0,70]);check(driver,lid+tray)
for dy in [-40,-40,-60]:cmd('solid.move',bodies=driver,translate=[0,dy,0]);check(driver,lid+tray)
(ROOT/'cad/support-access-checks.json').write_text(json.dumps(dict(commands=C),indent=2)+'\n')
print(json.dumps(dict(registered_screws=sum(counts.values()),groups=len(counts),rotation_checks=len(angles),cartridge_checks=2,service_checks=sum(c['command']=='inspect.clearance' for c in C))))
