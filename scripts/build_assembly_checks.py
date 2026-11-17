#!/usr/bin/env python3
"""Disposable CAD probes. Run without --save; no test fasteners enter production CAD."""
import json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
parts=[p['name'] for p in json.loads((ROOT/'cad/parts.json').read_text())['parts']]
old=json.loads((ROOT/'cad/support-access-checks.json').read_text())['commands']
arm=[]
for c in old:
 for n in c['params'].get('against',[]):
  if n not in parts and not n.startswith(('TEST','M5')) and n not in arm:arm.append(n)
C=[]; probes=[]; exclusions=[]
def cmd(c,**p):C.append(dict(command=c,params=p))
def cyl(n,d,z,h,x,y,op='new'):
 p=dict(diameter=d,height=h,base=[x,y,z],operation=op)
 p.update(body_name=n) if op=='new' else p.update(targets=[n])
 cmd('solid.cylinder',**p)
def screw(n,x,y,tip,seat,d,hd,hh,washer=None,ignore=()):
 probes.append(n);cyl(n,d,tip,seat-tip,x,y);cyl(n,hd,seat,hh,x,y,'join')
 if washer:
  od,t=washer;cyl(n,od,seat-t,t,x,y,'join')
 for body in ignore:exclusions.append([n,body])
def cylinder(n,x,y,z,d,h):probes.append(n);cyl(n,d,z,h,x,y)
cmd('component.activate',component='root');cmd('component.create',name='Disposable fastener envelopes',grounded=True)
armholes=[(27.776497308103686,-189.2250092524069),(31.75,-259),(-27.77649730810371,-189.2250092524069),(-31.75,-259)]
for i,(x,y) in enumerate(armholes):
 n=f'TEST F24 arm bolt {i}';screw(n,x,y,125.8,160.8,4,7,4,(9,.8));cyl(n,9,135.2,.8,x,y,'join');cyl(n,8.083,130.2,5,x,y,'join')
for i,(x,y) in enumerate([(x,y) for x in [-98,98] for y in [-272,-176]]):
 n=f'TEST F22 frame top bolt {i}';screw(n,x,y,120.6,145.6,6,10,6,ignore=(f'B5{i+1} bridge anchor washer',));cyl(n,18,130.4,1.6,x,y,'join');cyl(n,11.547,124.4,6,x,y,'join')
 screw(f'TEST F23 stand bench head {i}',x,y,0,5.6,6,10,6,(18,1.6))
for i,(x,y) in enumerate([(66,0),(-66,0),(36,-58),(-36,-58)]):screw(f'TEST F01 column bolt {i}',x,y,1.6,91.6,6,10,6,(11,1.6),('M01 aluminium base plate',))
for i,(x,y) in enumerate([(x,y) for x in [-64,64] for y in [-64,64]]):screw(f'TEST F02 core bench head {i}',x,y,0,13.6,6,10,6,(18,1.6))
for i,(x,y) in enumerate([(-52,18),(52,18),(-70,92),(70,92)]):screw(f'TEST F07 cartridge bolt {i}',x,y,5,21,5,8.5,5,(10,1),('M01 aluminium base plate',))
for i,(x,y) in enumerate([(x,y) for x in [-53,53] for y in [31.5,79.5]]):screw(f'TEST F08 worm block bolt {i}',x,y,9.5,74.5,5,8.5,5,(10,1))
for i,(x,y) in enumerate([(x,y) for x in [116,138] for y in [32,79]]):screw(f'TEST F10 motor foot bolt {i}',x,y,1,21,5,8.5,5,(10,1))
for i,(x,y) in enumerate([(x,y) for x in [171,225] for y in [21,91]]):screw(f'TEST F17 hood bolt {i}',x,y,1.3,96.3,4,7,4,(9,.8))
for i,y in enumerate([-6,6]):
 x,y=(-70+y)/math.sqrt(2),(70+y)/math.sqrt(2)
 screw(f'TEST F12 home bolt {i}',x,y,84.5,96.5,3,5.7,1.65,(7,.5),('M02 aluminium bearing seat',))
for i,(x,y) in enumerate([(x,y) for x in [-55.5,55.5] for y in [-258.5,-189.5]]):
 n=f'TEST F20 spreader screw {i}';probes.append(n)
 cyl(n,3,19.55,14.9,x,y)
 cmd('solid.cone',diameter=3.4,top_diameter=6,height=1.3,base=[x,y,34.25],operation='join',targets=[n])
 cyl(n,7,26.75,1.25,x,y,'join');cyl(n,6.351,22.75,4,x,y,'join')
for i,y in enumerate([20,48]):
 n=f'TEST F13 sole screw {i}';probes.append(n)
 cmd('solid.cone',diameter=10,top_diameter=5,height=2.5,base=[72,y,.2],operation='new',body_name=n)
 cyl(n,5,2.7,9.5,72,y,'join');exclusions.append([n,'M01 aluminium base plate'])
# Recessed screw heads and projecting rotating ends live in the rotor occurrence.
cmd('component.activate',component='RT01 - rotating table')
for i,(x,y) in enumerate([(x,y) for sx in [-1,1] for sy in [-1,1] for x,y in [(65*sx,22*sy),(22*sx,65*sy)]]):
 screw(f'TEST F06 platter bolt {i}',x,y,100,125,5,9.5,2.75)
for i,(x,y) in enumerate([(15,0),(0,15),(-15,0),(0,-15)]):screw(f'TEST F05 wheel bolt {i}',x,y,65,110,5,8.5,5,ignore=('B11 duplex wheel envelope',))
for i in range(8):
 a=math.radians(i*45);screw(f'TEST F04 inner ring bolt {i}',32.5*math.cos(a),32.5*math.sin(a),90,110,5,8.5,5,ignore=('B10 bearing inner ring reference',))
# All newly designed bodies checked; imported arm self-contacts intentionally excluded.
allnames=parts+arm+probes
for i in range(len(arm)):
 for b in arm[i+1:]:exclusions.append([arm[i],b])
exclusions.append(['B04 duplex worm envelope','B11 duplex wheel envelope'])
for angle in range(0,361,30):
 cmd('joint.drive',joint='RT01 vertical C axis',value=angle,quiet=True)
 cmd('inspect.interference',bodies=allnames,exclude_pairs=exclusions,budget_s=45)
cmd('joint.drive',joint='RT01 vertical C axis',value=0,quiet=True)
moving=['P20 worm cartridge sled','P21 worm bearing block left','P21 worm bearing block right','P22 worm bearing retainer left','P22 worm bearing retainer right','B02 worm support bearing left','B02 worm support bearing right','B03 worm shaft reference','B04 duplex worm envelope']+[f'TEST F08 worm block bolt {i}' for i in range(4)]
cmd('component.activate',component='root')
for delta in [3,-6]:
 cmd('solid.move',bodies=moving,translate=[delta,0,0])
 cmd('inspect.interference',bodies=allnames,exclude_pairs=exclusions,budget_s=45)
(ROOT/'cad/fastener-clearance-checks.json').write_text(json.dumps(dict(commands=C),indent=2)+'\n')
# Existing tool and lid checks updated to the new frame. No screw probes during lid removal.
for c in old:
 p=c['params']
 if c['command']=='solid.cylinder' and p.get('body_name','').startswith('TEST lid tool'):p['base'][2]=110.2;p['height']=58
 if c['command']=='inspect.clearance':
  if p['bodies'][0].startswith('TEST lid tool'):p['against']=['M50 SO100 arm mounting plate','M51 steel side channel left','M51 steel side channel right','M52 steel front X brace']+arm
  else:p['against']=[n for n in parts if n not in p['bodies']]+arm
(ROOT/'cad/support-access-checks.json').write_text(json.dumps(dict(commands=old),indent=2)+'\n')
print('Fastener envelopes',len(probes),'arm bodies',len(arm),'commands',len(C))
