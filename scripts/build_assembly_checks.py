#!/usr/bin/env python3
"""Disposable hardware and service probes. Run without --save."""
import json,math
from collections import Counter
from copy import deepcopy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
part_register=json.loads((ROOT/'cad/parts.json').read_text())
parts=[p['name'] for p in part_register['parts']]
revision=part_register['revision']
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
def nut(n,af,height,x,y,z):
 sketch=n+' hex'
 radius=af/math.sqrt(3)
 vertices=[[f'{radius*math.cos(math.radians(a)):.12f} mm',f'{radius*math.sin(math.radians(a)):.12f} mm'] for a in range(30,360,60)]
 cmd('sketch.create',name=sketch,plane={'origin':[x,y,z],'x_dir':[1,0,0],'y_dir':[0,1,0]})
 cmd('sketch.line',points=vertices,closed=True,connect=False);cmd('sketch.finish')
 cmd('solid.extrude',sketch=sketch,distance=height,operation='join',targets=[n])
cmd('component.activate',component='root');cmd('component.create',name=f'Disposable revision {revision} hardware',grounded=True)
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
foot_points=[(x,y) for x in [-75,75] for y in [-271,-177]]
for i,(x,y) in enumerate(foot_points):
 n=f'TEST F21 {i}';register(n,'F21')
 # Upward bolt. Allow just under 5 mm extra after rounding the minimum length.
 cyl(n,4,44.95,[x,y,0]);collar(n,9,1.55,x,y,32);nut(n,7,5,x,y,33.55)
for i,(x,y) in enumerate([(x,y) for x in [-98,98] for y in [-272,-176]]):
 n=f'TEST F22 {i}';screw(n,'F22',x,y,128.6,153.6,6,10,6);collar(n,18,1.6,x,y,138.4);collar(n,10/math.cos(math.pi/6),6,x,y,132.4)
 screw(f'TEST F23 {i}','F23',x,y,0,5.6,6,10,6,(18,1.6))
for i,p in enumerate(armdata['adapter_holes']):
 x,y=p['plate_hole_center_mm'][:2];n=f'TEST F24 {i}'
 # Longest permitted assembled penetration, with the provisional upper hardware envelope.
 screw(n,'F24',x,y,145,168.8,4,7,4,(9,.8),('M50 SO100 arm mounting plate',))
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
coverage=dict(revision=revision,groups=dict(counts),retired=['F08','F12'],fixed_and_bench_screws=sum(counts.values()),fixture_tip_bounds=4,permanent_retention=['B13 sensor upper jam nut','B13 sensor lower jam nut','M21 wheel drive pin','M62 retainer shim left','M62 retainer shim right'],angles_deg=angles,cartridge_offsets_mm=[3,-3],exclusions=reasons,limits=['Bench bolts in rotation are checked above Z0; below-bench seats are checked separately.','Heat-set insert retention inside its pilot requires first-article testing.','F24 upper seating, actual screw lengths and unselected board, coupling and shaft-retention fasteners remain open interfaces.'])

# Build the same hardware population before testing service. Omit removed screw groups
# per operation, including lid screws when checking the path that reaches their sockets.
C=C[:population_end];cmd('component.activate',component='root');cmd('component.create',name='Disposable service tools',grounded=True)
service_labels=[]
def check(label, moving, removed=(), released=()):
 absent=set(moving)|set(removed)
 against=[n for n in allnames if n not in absent and not n.startswith(released)]
 cmd('inspect.clearance',bodies=moving,against=against,nearest=3)
 service_labels.append(label)

toolnames=[]
for i,(x,y) in enumerate(lidpoints):
 n=f'TEST lid tool {i}';toolnames.append(n);cyl(n,6,70,[x,y,110.2])
check('lid tool approach',toolnames,released=('TEST F18 ',))

lid=['P52 electronics lid','B24 lid gasket']
tray=['P51 removable controller tray','B23 controller packaging envelope']
driver=['B22 driver packaging envelope']
hood=['P46 motor service hood']
released_lid=('TEST F18 ',)
released_tray=released_lid+('TEST F19 ',)

# Dimensioned tool envelopes are acceptance limits for a selected physical tool,
# not a claim that a particular commercial driver or a human hand was checked.
def tool_box(n,size,corner,op='new'):
 p=dict(length=size[0],width=size[1],height=size[2],corner=corner,operation=op)
 p.update(body_name=n) if op=='new' else p.update(targets=[n])
 cmd('solid.box',**p)

def lever_tool(n,x,y,tip,shaft_d,shaft_h,handle_h,axis,side=1,travel=0):
 # The enlarged hub bounds the bend or bit holder. The bar includes its grip.
 cyl(n,shaft_d,shaft_h+travel,[x,y,tip])
 cyl(n,8,handle_h+travel,[x,y,tip+shaft_h],op='join')
 corner=[x if side>0 else x-65,y-4,tip+shaft_h] if axis=='X' else [x-4,y-65,tip+shaft_h]
 tool_box(n,[65,8,handle_h+travel] if axis=='X' else [8,65,handle_h+travel],corner,'join')

tool_contracts={
 'F24':dict(shaft_diameter_mm=3.47,shaft_projection_mm=25,hub_diameter_mm=8,
             handle_reach_mm=65,handle_section_mm=[8,5],engaged_tip_z_mm=170.8,
             disengagement_mm=3,approach_axis_x_mm=90,rotation_sample_step_deg=5,
             bounding_rotation_radius_mm=69,
             between_sample_motion_bound_mm=2*69*math.sin(math.radians(5)/4),
             preconditions=['Power isolated; arm supported in the saved folded pose.',
               'Provisional F24 head seat Z168.8 only; revise checks after the matched seats are designed.',
               'All other F24 fasteners remain installed; exclude only the working socket.',
               'Select/measure an actual AF3 tool within the shaft, bend and grip envelope; confirm its rating and hand access for the qualified clamp torque.'],
             limits=['The arm/foot clamps, actual seating pressure, hand volume and tool strength are not qualified by clearance.',
               'Angular paths are sampled every5 degrees; subtract the recorded between-sample bound from the measured minimum before claiming continuous angular clearance.']),
 'F19':dict(shaft_diameter_mm=2.31,shaft_projection_mm=22,hub_diameter_mm=8,
             handle_reach_mm=65,handle_section_mm=[8,8],engaged_tip_z_mm=83,
             rear_entry_y_mm=-306,rear_entry_tip_z_mm=106.5,disengagement_mm=2.5,
             screw_backout_mm=7,thread_contact_lift_min_mm=6,retrieval_lift_to_tip_z_mm=106.5,
             captive_washer=dict(outer_diameter_mm=7,thickness_mm=.5,bore_mm=[2.75,2.80],
                 neck_max_diameter_mm=2.68,thread_stop_min_diameter_mm=2.88,axial_float_max_mm=.25),
             gripper=dict(jaw_and_stem_max_diameter_mm=8,jaw_lower_edge_above_head_seat_mm=.10,
                 bridge_reach_mm=145,bridge_section_mm=[8,4],bridge_bottom_above_head_seat_mm=17.5),
             preconditions=['Isolate power; remove lid/gasket and all F18 screws.',
               'Disconnect and label controller/service leads; park loose leads outside the rear tool and extraction corridor before working.',
               'Keep the controller/tray, driver reservation and all other installed hardware while accessing each F19 socket.',
               'Use an AF2 lever driver within the stated envelope, then a rear-operated mechanical head gripper sized for the captive screw.',
               'Keep removed fasteners outside the tray service sweep.'],
             limits=['F19 includes the enlarged 118 x 70 x 20 controller reserve. Actual head grip, captive retention, insert-mouth position, hand access and fitted cables require the physical trial.',
               'The gripper is a dimensional acceptance envelope. Select or fabricate a tool with jaws that retain and release the screw head from the rear.'])}

# F24: side entry with the long arm pointing outward. Every tightening stroke
# is clockwise viewed from +Z. Mirrored sites use different starting clocking.
f24_clocking=[]
for i,point in enumerate(armdata['adapter_holes']):
 x,y=point['plate_hole_center_mm'][:2];side=1 if x>0 else -1
 arc=side*(1 if y>-224 else -1)
 start=60 if arc>0 else 0;end=start-60;outside=0 if side>0 else 180
 f24_clocking.append(dict(site=i,center_mm=[x,y],handle_start_azimuth_deg=outside+start,handle_end_azimuth_deg=outside+end))
 socket=(f'TEST F24 {i}',)
 delta=90-abs(x)
 n=f'TEST F24 outboard entry sweep {i}'
 tool_box(n,[delta+3.47,3.47,25],[x-1.735 if side>0 else -91.735,y-1.735,173.8])
 tool_box(n,[delta+69,8,5],[x-4 if side>0 else -155,y-4,198.8],'join')
 check(f'F24 tool {i} complete outboard entry', [n], released=socket)
 n=f'TEST F24 engagement sweep {i}';lever_tool(n,x,y,170.8,3.47,25,5,'X',side,3)
 check(f'F24 tool {i} complete axial engagement', [n], released=socket)
 n=f'TEST F24 compact lever {i}';lever_tool(n,x,y,173.8,3.47,25,5,'X',side)
 yaw=0
 if start:
  for angle in range(5,start+1,5):
   cmd('solid.move',bodies=[n],axis=[0,0,1],origin=[x,y,170.8],angle=angle-yaw);yaw=angle
   check(f'F24 tool {i} raised entry clocking {angle}',[n],released=socket)
 cmd('solid.move',bodies=[n],translate=[0,0,-3]);check(f'F24 tool {i} first engagement',[n],released=socket)
 for stroke in range(2):
  for angle in range(start-5,end-1,-5):
   cmd('solid.move',bodies=[n],axis=[0,0,1],origin=[x,y,170.8],angle=angle-yaw);yaw=angle
   check(f'F24 tool {i} clockwise stroke {stroke} at {angle}',[n],released=socket)
  cmd('solid.move',bodies=[n],translate=[0,0,3]);check(f'F24 tool {i} disengaged after stroke {stroke}',[n],released=socket)
  for angle in range(end+5,start+1,5):
   cmd('solid.move',bodies=[n],axis=[0,0,1],origin=[x,y,170.8],angle=angle-yaw);yaw=angle
   check(f'F24 tool {i} raised reset {stroke} at {angle}',[n],released=socket)
  if stroke==0:
   cmd('solid.move',bodies=[n],translate=[0,0,-3]);check(f'F24 tool {i} second engagement',[n],released=socket)
 # Return to the straight outboard orientation while disengaged, then leave.
 if yaw:cmd('solid.move',bodies=[n],axis=[0,0,1],origin=[x,y,170.8],angle=-yaw)
 cmd('solid.move',bodies=[n],translate=[side*(90-abs(x)),0,0])
 check(f'F24 tool {i} outboard withdrawal',[n],released=socket)
tool_contracts['F24']['clocking']=f24_clocking

# F19. The general assembly check uses the same maximum exterior stack.
# For service, replace that bounding stack in the collision population with
# two separate solids. The washer can lag the screw by 0.25 mm.
general_service_population = allnames
sites = [(x, y) for x in [-65, 65] for y in [-258, -190]]
screws = [f'F19 captive screw {i}' for i in range(4)]
washers = [f'F19 captive washer {i}' for i in range(4)]
storage_y = -306
seat_z = 82.5
washer_float = .25
storage_lift = 34
thread_contact_lift = 6
contact_screw_z = seat_z + thread_contact_lift
board = 'F19 enlarged controller reservation'
tool_box(board, [118, 70, 20], [-59, -259, 82])
allnames = [name for name in allnames if not name.startswith('TEST F19 ')] + screws + washers + [board]

for screw_name, washer, (x, y) in zip(screws, washers, sites):
    cyl(screw_name, 3, 9.25, [x, y, 72.5])
    cyl(screw_name, 2.68, .75, [x, y, seat_z-.75], op='join')
    cyl(screw_name, 5.7, 1.65, [x, y, seat_z], op='join')
    cyl(washer, 7, .5, [x, y, 82])
    cyl(washer, 2.75, 1.5, [x, y, 81.5], op='cut')

lid_parts = lid + [name for name in probes if name.startswith('TEST F18 ')]
parked = []
hardware_lift = [0.] * 4
washer_lift = [0.] * 4


def translate(bodies, dy=0, dz=0):
    if dy or dz:
        cmd('solid.move', bodies=bodies, translate=[0, dy, dz])


def shift_hardware(i, height, lag=True):
    # The washer may remain seated on the tray while slack is taken up.
    lower_washer = max(0, height-washer_float) if lag else height
    translate([screws[i]], dz=height-hardware_lift[i])
    translate([washers[i]], dz=lower_washer-washer_lift[i])
    hardware_lift[i] = height
    washer_lift[i] = lower_washer


def tool_check(i, phase, bodies, contact=()):
    check(f'F19 site {i+1} {phase}', bodies, lid_parts+parked+list(contact))


def torque_access(i, removing):
    x, y = sites[i]
    screw_name, washer = screws[i], washers[i]
    action = 'remove' if removing else 'refit'
    key = f'F19 {action} AF2 key {i}'
    entry = key+' full rear travel'
    tool_box(entry, [2.31, y+308.31, 22], [x-1.155, -307.155, 106.5])
    tool_box(entry, [8, y+375, 8], [x-4, -371, 128.5], 'join')
    tool_check(i, action+' AF2 full rear entry and exit', [entry])
    # This bound covers every axial position, every 60-degree turn,
    # and every 2.5 mm lift to disengage before the return stroke.
    bound = key+' turning bound'
    cyl(bound, 2.31, 31.5, [x, y, 83])
    cyl(bound, 8, 17.5, [x, y, 105], op='join')
    tool_box(bound, [65*math.sin(math.pi/3)+8, 69, 17.5],
             [x-4 if x<0 else x-65*math.sin(math.pi/3)-4, y-69, 105], 'join')
    tool_check(i, action+' AF2 full turning and reset bound', [bound], [screw_name])
    down = key+' entry descent bound'
    lever_tool(down, x, y, 83, 2.31, 22, 8, 'Y', travel=23.5)
    tool_check(i, action+' AF2 full axial entry and exit', [down], [screw_name])

    start, end = (0, 60) if x < 0 else (-60, 0)
    if not removing:
        start, end = end, start
    origin = [x, y, seat_z]
    height = hardware_lift[i]
    lever_tool(key, x, y, 83+height+2.5, 2.31, 22, 8, 'Y')
    if start:
        cmd('solid.move', bodies=[key], axis=[0, 0, 1], origin=origin, angle=start)
    for stroke in range(2):
        translate([key], dz=-2.5)
        tool_check(i, f'{action} AF2 socket engagement {stroke+1}', [key], [screw_name])
        advance = (.5/6) * (1 if removing else -1)
        cmd('solid.move', bodies=[key], axis=[0, 0, 1], origin=origin, angle=end-start)
        translate([key], dz=advance)
        height += advance
        shift_hardware(i, height)
        tool_check(i, f'{action} AF2 driven turn {stroke+1}', [key, screw_name, washer])
        translate([key], dz=2.5)
        tool_check(i, f'{action} AF2 lift after turn {stroke+1}', [key])
        cmd('solid.move', bodies=[key], axis=[0, 0, 1], origin=origin, angle=start-end)
    final_height = 7 if removing else 0
    shift_hardware(i, final_height)
    translate([key], dz=final_height-height)
    tool_check(i, action+' AF2 at end of repeated turns', [key, screw_name, washer])
    if start:
        cmd('solid.move', bodies=[key], axis=[0, 0, 1], origin=origin, angle=-start)
    translate([key], dz=106.5-(85.5+final_height))
    tool_check(i, action+' AF2 rear-clocked and raised', [key])
    translate([key], dy=storage_y-y)
    tool_check(i, action+' AF2 withdrawn', [key])


def transfer(i, removing):
    x, y = sites[i]
    screw_name, washer = screws[i], washers[i]
    action = 'remove' if removing else 'refit'
    tool = f'F19 {action} captive fastener gripper {i}'
    low_nose = contact_screw_z+.10
    low_bridge = contact_screw_z+17.5
    reach = 145
    travel = storage_lift-thread_contact_lift
    # Model the outside envelope of open/closed head jaws and their reach.
    # The head is intentionally inside the jaws during capture and release.
    empty_rear = tool+' empty horizontal sweep'
    tool_box(empty_rear, [8, y-storage_y+reach+4, 21.4],
             [x-4, storage_y-reach, low_nose+18])
    tool_check(i, action+' gripper full empty rear sweep', [empty_rear], [screw_name, washer])
    loaded_rear = tool+' loaded horizontal sweep'
    tool_box(loaded_rear, [8, y-storage_y+reach+4, 31.5],
             [x-4, storage_y-reach, 106.5])
    tool_check(i, action+' gripper full loaded rear sweep', [loaded_rear], [screw_name, washer])
    vertical = tool+' full vertical sweep'
    cyl(vertical, 8, 17.4+travel+4, [x, y, low_nose])
    tool_box(vertical, [8, reach, travel+4], [x-4, y-reach, low_bridge], 'join')
    tool_check(i, action+' gripper full vertical sweep', [vertical], [screw_name, washer])
    payload = tool+' complete payload lift bound'
    cyl(payload, 3, 11.65+travel, [x, y, 72.5+thread_contact_lift])
    cyl(payload, 7, .5+washer_float+travel, [x, y, 82+thread_contact_lift-washer_float], op='join')
    tool_check(i, action+' captive stack full axial travel', [payload], [screw_name, washer])

    cyl(tool, 8, 21.4, [x, y, low_nose])
    tool_box(tool, [8, reach, 4], [x-4, y-reach, low_bridge], 'join')
    if removing:
        translate([tool], dy=storage_y-y, dz=18)
        tool_check(i, 'remove gripper enters from rear', [tool])
        translate([tool], dy=y-storage_y)
        translate([tool], dz=-18)
        tool_check(i, 'remove jaws grip head above captive washer', [tool], [screw_name])
        translate([tool], dz=travel)
        shift_hardware(i, storage_lift)
        tool_check(i, 'remove captured stack just above rim', [tool, screw_name, washer])
        translate([tool, screw_name, washer], dy=storage_y-y)
        tool_check(i, 'remove captured stack fully withdrawn', [tool, screw_name, washer])
    else:
        translate([tool], dy=storage_y-y, dz=travel)
        tool_check(i, 'refit loaded tool enters from rear', [tool, screw_name, washer])
        translate([tool, screw_name, washer], dy=y-storage_y)
        tool_check(i, 'refit captive stack positioned over hole', [tool, screw_name, washer])
        translate([tool], dz=-travel)
        shift_hardware(i, thread_contact_lift)
        tool_check(i, 'refit jaws release at insert mouth', [tool], [screw_name])
        tool_check(i, 'refit screw and washer at thread pickup', [screw_name, washer])
        translate([tool], dz=18)
        translate([tool], dy=storage_y-y)
        tool_check(i, 'refit empty gripper withdrawn', [tool])


for i in range(4):
    tool_check(i, 'installed screw and captive washer', [screws[i], washers[i]])
    torque_access(i, removing=True)
    shift_hardware(i, thread_contact_lift)
    tool_check(i, 'free washer against its thread stop and other hardware', [washers[i]])
    # Test the opposite end of washer axial float before gripping the head.
    shift_hardware(i, thread_contact_lift, lag=False)
    tool_check(i, 'free washer at top of permitted float', [washers[i]])
    shift_hardware(i, thread_contact_lift)
    transfer(i, removing=True)
    parked += [screws[i], washers[i]]

# Set removed fasteners aside, then withdraw and return the tray before refitting.
tray_with_board = tray+[board]
for phase, dy, dz in [
    ('lift for removal', 0, 27), ('slide out', -140, 0),
    ('slide back in', 140, 0), ('lower onto posts', 0, -27),
]:
    translate(tray_with_board, dy=dy, dz=dz)
    check('F19 tray '+phase, tray_with_board, lid_parts+parked)

for i in reversed(range(4)):
    parked = [name for name in parked if name not in (screws[i], washers[i])]
    transfer(i, removing=False)
    torque_access(i, removing=False)
    tool_check(i, 'refitted screw seated and washer supported', [screws[i], washers[i]])

allnames = general_service_population
coverage['service_tool_contracts']=tool_contracts

for label,moving,height,removed,released in [
 ('lid',lid,8,[],released_lid),('tray',tray,27,lid,released_tray),
 ('driver',driver,70.5,lid+tray,released_tray),
]:
 cmd('solid.move',bodies=moving,translate=[0,0,height]);check(f'{label} lift {height}',moving,removed,released)
 previous=0
 for distance in [10,20,30,40,50,60,70,80,100,120,140]:
  cmd('solid.move',bodies=moving,translate=[0,previous-distance,0])
  check(f'{label} rearward {distance}',moving,removed,released);previous=distance

# A rectangular body swept along one axis has a rectangular swept volume.
# Check both full segments, including the retained arm and its recessed F24 tips.
for label,corner,size in [
 ('driver complete lift sweep',[-59,-262,36],[118,76,105.5]),
 ('driver complete withdrawal sweep',[-59,-402,106.5],[118,216,35]),
]:
 length,width,height=size
 cmd('solid.box',body_name=f'TEST {label}',corner=corner,length=length,width=width,height=height,operation='new')
 check(label,[f'TEST {label}'],lid+tray+driver,released_tray)

previous=0
for distance in [2,5,10,20,30,48,49,50,70]:
 cmd('solid.move',bodies=hood,translate=[distance-previous,0,0])
 check(f'hood outward {distance}',hood,lid+tray+driver,('TEST F17 ',));previous=distance
 if distance==49:
  cmd('inspect.clearance',bodies=hood,against=['B41 motor anchor washer','B42 motor anchor washer'],nearest=2)
  service_labels.append('hood posts clear motor anchor washers at X+49')
cmd('solid.move',bodies=hood,translate=[0,0,30])
check('hood outward 70 and up 30',hood,lid+tray+driver,('TEST F17 ',))

# F02 is torqued while the core is still exposed. The two covered heads are
# below solid carrier blocks after assembly, so the carrier is removed for access.
core_base=['M01 aluminium base plate','M40 stepped motor support']
core_base.extend(n for n in parts if 'metal bench spacer' in n)
for i,(x,y) in enumerate([(x,y) for x in [-64,64] for y in [-64,64]]):
 n=f'TEST F02 straight key {i}';cyl(n,6,70,[x,y,16.6])
 cmd('inspect.clearance',bodies=[n],against=core_base,nearest=1)
 service_labels.append(f'F02 key before carrier {i}')

# Short leg engages from the side with the housing open and retaining the hub,
# bearing and wheel. B07 is optional and has no baseline installed hardware.
# This is a measured-tool candidate, not a claim about every AF4 hex key.
# Sample two clockwise tightening strokes viewed from +Z, disengaging before
# each return swing. Finish both keys withdrawn in the rearward orientation.
coverage['f07_tool_cycle']=dict(
 tool='AF4 compact hex-key candidate; verify the actual bend, section and torque capability',
 shaft_envelope_diameter_mm=5,handle_section_mm=[5,5],handle_reach_mm=65,
 engaged_tip_z_mm=23,tip_to_handle_top_mm=12,disengagement_mm=5,
 assumed_socket_engagement_mm=3,
 tightening_strokes=2,tightening_direction='Clockwise viewed from +Z for both right-hand screws',
 engaged_yaw_samples_deg={'left':[60,45,30,12,0],'right':[0,-12,-30,-45,-60]},
 disengagement_samples_mm=[1,2,3,4,5],
 reset_yaw_samples_deg={'left':[12,30,45,60],'right':[-45,-30,-12,0]},
 reengagement_samples_mm=[4,3,2,1,0],
 rear_infeed_offsets_mm=[-80,-60,-40,-20,0],rear_retreat_offsets_mm=[-20,-40,-60,-80],
 prerequisites='All fixed housing quadrants, seam strips and motor hood removed with F15/F16/F17 cover hardware; retain hub, bearing, wheel, columns, sleeves and other registered hardware; optional B07 encoder absent',
 carrier_x_offset_mm=0,
 coverage='Sampled tool poses for rear infeed/retreat, swing, disengagement, reset and re-engagement at the centered carrier; not a continuous swept-volume proof')
for i,(x,tightening,reset) in enumerate([
 (-52,[60,45,30,12,0],[12,30,45,60]),
 (52,[0,-12,-30,-45,-60],[-45,-30,-12,0]),
]):
 n=f'TEST F07 side key {i}';cyl(n,5,12,[x,-62,28])
 cmd('solid.box',length=5,width=65,height=5,corner=[x-2.5,-127,35],operation='join',targets=[n])
 against=[b for b in allnames if b!=f'TEST F07 {i}' and not b.startswith(('P4','B25 ','B07 ','TEST F15 ','TEST F16 ','TEST F17 '))]
 yaw=0;lift=5;rear=-80
 for offset in [-80,-60,-40,-20,0]:
  if offset!=rear:cmd('solid.move',bodies=[n],translate=[0,offset-rear,0])
  rear=offset
  cmd('inspect.clearance',bodies=[n],against=against,nearest=2)
  service_labels.append(f'F07 side key {i} rear infeed {rear} mm lifted {lift} mm at 0 degrees')
 if tightening[0]:
  for angle in reset:
   cmd('solid.move',bodies=[n],axis=[0,0,1],origin=[x,18,23],angle=angle-yaw);yaw=angle
   cmd('inspect.clearance',bodies=[n],against=against,nearest=2)
   service_labels.append(f'F07 side key {i} initial airborne reset at {yaw} degrees lifted {lift} mm')
 for height in [4,3,2,1,0]:
  cmd('solid.move',bodies=[n],translate=[0,0,height-lift]);lift=height
  cmd('inspect.clearance',bodies=[n],against=against,nearest=2)
  service_labels.append(f'F07 side key {i} initial engagement lifted {lift} mm at {yaw} degrees')
 for stroke in range(1,3):
  for angle in tightening:
   if angle!=yaw:cmd('solid.move',bodies=[n],axis=[0,0,1],origin=[x,18,23],angle=angle-yaw)
   yaw=angle
   cmd('inspect.clearance',bodies=[n],against=against,nearest=2)
   service_labels.append(f'F07 side key {i} stroke {stroke} engaged at {yaw} degrees')
  for height in [1,2,3,4,5]:
   cmd('solid.move',bodies=[n],translate=[0,0,height-lift]);lift=height
   cmd('inspect.clearance',bodies=[n],against=against,nearest=2)
   service_labels.append(f'F07 side key {i} stroke {stroke} disengagement {lift} mm at {yaw} degrees')
  for angle in reset:
   cmd('solid.move',bodies=[n],axis=[0,0,1],origin=[x,18,23],angle=angle-yaw);yaw=angle
   cmd('inspect.clearance',bodies=[n],against=against,nearest=2)
   service_labels.append(f'F07 side key {i} stroke {stroke} reset at {yaw} degrees lifted {lift} mm')
  if stroke==1:
   for height in [4,3,2,1,0]:
    cmd('solid.move',bodies=[n],translate=[0,0,height-lift]);lift=height
    cmd('inspect.clearance',bodies=[n],against=against,nearest=2)
    service_labels.append(f'F07 side key {i} re-engagement before stroke 2 lifted {lift} mm')
 if yaw:
  for angle in [45,30,12,0]:
   cmd('solid.move',bodies=[n],axis=[0,0,1],origin=[x,18,23],angle=angle-yaw);yaw=angle
   cmd('inspect.clearance',bodies=[n],against=against,nearest=2)
   service_labels.append(f'F07 side key {i} final withdrawal at {yaw} degrees lifted {lift} mm')
 for offset in [-20,-40,-60,-80]:
  cmd('solid.move',bodies=[n],translate=[0,offset-rear,0]);rear=offset
  cmd('inspect.clearance',bodies=[n],against=against,nearest=2)
  service_labels.append(f'F07 side key {i} rear retreat {rear} mm lifted {lift} mm at 0 degrees')

# Relative washer-to-strip distances are independent of the common bench thickness.
# Reuse the actual production drawing at both locations. No bench material is modeled.
T=30
strip_commands=json.loads((ROOT/'cad/stand-backing-strip.json').read_text())['commands']
strip_names=[]
for side in [-1,1]:
 strip=f'TEST M55 backing strip {side}';strip_names.append(strip)
 for row in strip_commands:
  if row['command'] not in ('solid.box','solid.cylinder'):continue
  params=deepcopy(row['params'])
  if 'body_name' in params:params['body_name']=strip
  if 'targets' in params:params['targets']=[strip]
  cmd(row['command'],**params)
 if side<0:cmd('solid.move',bodies=[strip],origin=[0,0,0],axis=[0,0,1],angle=180)
 cmd('solid.move',bodies=[strip],translate=[side*98,-224,-T-3])
underbox=[]
for i,(x,y) in enumerate(foot_points):
 n=f'TEST F21 underside {i}';underbox.append(n)
 cyl(n,7,4,[x,y,-T-5]);collar(n,12,1,x,y,-T-1)
understand=[]
for i,(x,y) in enumerate([(x,y) for x in [-98,98] for y in [-272,-176]]):
 n=f'TEST F23 underside {i}';understand.append(n)
 cyl(n,6,17,[x,y,-T-17]);collar(n,18,1.6,x,y,-T-4.6);nut(n,10,6,x,y,-T-10.6)
cmd('inspect.clearance',bodies=underbox,against=strip_names+understand,nearest=3)
service_labels.append('below-bench electronics and stand hardware')
cmd('inspect.clearance',bodies=understand,against=strip_names,nearest=2)
service_labels.append('below-bench stand washer contact')

# A 0.10 mm annulus crossing each seat is an intentional positive intersection.
# Half its volume must be supported at each nominal seat plane.
seating_checks=[]
for label,positions,plane,od,inner,against in [
 ('F23 washer seats',[(x,y) for x in [-98,98] for y in [-272,-176]],-T-3,18,6.6,strip_names),
 ('F21 seal lands',foot_points,32,9,4.5,['P50 electronics service box']),
]:
 gauges=[]
 for i,(x,y) in enumerate(positions):
  n=f'TEST {label} annulus {i}';gauges.append(n)
  cyl(n,od,.1,[x,y,plane-.05]);cyl(n,inner,.3,[x,y,plane-.15],op='cut')
 cmd('inspect.interference',bodies=gauges+against,budget_s=30)
 seating_checks.append(dict(name=label,gauges=gauges,expected_overlap_mm3_per_gauge=.05*math.pi*(od**2-inner**2)/4))

coverage['service_checks']=service_labels
coverage['seating_checks']=seating_checks
(ROOT/'cad/hardware-check-coverage.json').write_text(json.dumps(coverage,indent=2)+'\n')
(ROOT/'cad/support-access-checks.json').write_text(json.dumps(dict(commands=C),indent=2)+'\n')
print(json.dumps(dict(registered_screws=sum(counts.values()),groups=len(counts),rotation_checks=len(angles),cartridge_checks=2,service_checks=sum(c['command']=='inspect.clearance' for c in C))))
