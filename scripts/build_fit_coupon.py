"""Coupon for production printed fits. No import side effects."""
import json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
C=[];B='RT01 PETG fit coupon'
def cmd(c,**p):C.append(dict(command=c,params=p))
def box(size,corner,op='join'):
 p=dict(length=size[0],width=size[1],height=size[2],corner=corner,operation=op)
 p.update(body_name=B) if op=='new' else p.update(targets=[B]);cmd('solid.box',**p)
def cyl(d,h,base,axis='Z',op='cut'):
 cmd('solid.cylinder',diameter=d,height=h,base=base,axis=axis,operation=op,targets=[B])
cmd('component.create',name='RT01 revision 5 fit coupon',grounded=True)
box([150,100,4],[0,0,0],'new');box([4,4,6],[-1,-1,-1],'cut')
for x,d in [(15,3.4),(35,4.5),(55,5.5),(75,6.6)]:cyl(d,6,[x,15,-1])
for x,d in [(100,4.0),(120,4.2),(140,4.4)]:
 box([16,16,4.2],[x-8,7,3.8]);cyl(d,8,[x,15,1])
for x,d in [(15,10.2),(35,10.3),(55,10.4)]:
 cyl(16,4.2,[x,42,3.8],op='join');cyl(d,10,[x,42,-1])
for x,d in [(85,16.1),(110,16.3),(135,16.5)]:
 box([20,20,4.2],[x-10,32,3.8]);cyl(d,6.2,[x,42,2.8])
# Reproduce the upward F21 nut trap and inward seal/washer loading slot.
x,y=30,62
cyl(14,8.2,[x,y,3.8],op='join');cyl(4.5,8,[x,y,-1]);cyl(9.4,2,[x,y,4])
box([9,9.4,2],[x-9,y-4.7,4],'cut')
radius=7.4/math.sqrt(3)
vertices=[[round(radius*math.cos(math.radians(a)),12),round(radius*math.sin(math.radians(a)),12)] for a in range(30,360,60)]
cmd('sketch.create',name='F21 M4 nut pocket',plane={'origin':[x,y,6],'x_dir':[1,0,0],'y_dir':[0,1,0]})
cmd('sketch.line',points=vertices,closed=True,connect=False)
cmd('sketch.constraint.fix',entities=[f'l{i}' for i in range(1,7)],fixed=True)
cmd('sketch.finish');cmd('solid.extrude',sketch='F21 M4 nut pocket',distance=6.5,operation='cut',targets=[B])
box([150,20,24],[0,75,0])
horizontal=[3.4,3.5,3.6,4.5,4.6,4.7,5.5,5.6,5.7]
for i,d in enumerate(horizontal):cyl(d,24,[15+15*i,73,15],'Y')
cmd('appearance.assign',bodies=[B],color='#DAE4E6');cmd('view.apply',view='iso')
(ROOT/'cad/fit-coupon-build.json').write_text(json.dumps(dict(commands=C),indent=2)+'\n')
(ROOT/'cad/fit-coupon-features.json').write_text(json.dumps(dict(revision=5,notch='lower-left, X0/Y0',vertical_holes=dict(y=15,xd=[[15,3.4],[35,4.5],[55,5.5],[75,6.6]]),insert_trials=dict(y=15,xd=[[100,4],[120,4.2],[140,4.4]],depth=7),column_trials=dict(y=42,xd=[[15,10.2],[35,10.3],[55,10.4]],depth=8),fixture_boss_trials=dict(y=42,xd=[[85,16.1],[110,16.3],[135,16.5]],depth=5.2),horizontal_holes=dict(y_range=[75,95],z=15,xd=[[15+15*i,d] for i,d in enumerate(horizontal)]),f21_nut_trap=dict(center_xy=[30,62],nut_across_flats=7.4,washer_slot_height=2,slot_opens_toward='-X'),required_first_articles=['One complete P11 column sleeve for the69.5 mm bore','P24 motor bracket for horizontal pilot/holes and clamp retention','P50/P52 enclosure land, insert and gasket compression','F21 nut-trap assembly and sealed clamp','One platter quadrant on M20 raised fixture boss'],removed_interfaces='Printed bearing seats, wheel pilot and hub sleeve fit were removed in revision 4. Metal fits use machining inspection.'),indent=2)+'\n')
print(f'Generated revision 5 coupon: {len(C)} commands')
