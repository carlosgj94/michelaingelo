"""Generate named SolidCraft commands for RT-01. Dimensions are mm.
Run this generator, then run cad/rotary-table-build.json in SolidCraft.
Purchased parts are deliberately simplified envelopes; see the specification.
"""
import json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REVISION=5
commands=[]; parts=[]; stages=[]; serial=0
CARRIER='M60 monolithic worm carrier'
HUB='M20 registered output hub'
SENSOR_XY=(73*math.cos(math.radians(210)),73*math.sin(math.radians(210)))

def cmd(command,**params):
    commands.append({'command':command,'params':params})

def stage(name):
    stages.append((name,len(commands)))

def group(name,ground=True):
    cmd('component.activate',component='root')
    cmd('component.create',name=name,grounded=ground)

def feature(label):
    global serial
    serial+=1
    return f'{serial:03d} {label}'

def box(body,size,corner,op='new',label=None):
    p=dict(length=size[0],width=size[1],height=size[2],corner=corner,operation=op,name=feature(label or body))
    p.update(body_name=body) if op=='new' else p.update(targets=[body])
    cmd('solid.box',**p)

def cyl(body,d,h,base,axis='Z',op='new',label=None):
    p=dict(diameter=d,height=h,base=base,axis=axis,operation=op,name=feature(label or body))
    p.update(body_name=body) if op=='new' else p.update(targets=[body])
    cmd('solid.cylinder',**p)

def ring(body,od,id_,h,z,xy=(0,0),axis='Z'):
    base=[xy[0],xy[1],z]
    cyl(body,od,h,base,axis)
    cut=base.copy(); k={'X':0,'Y':1,'Z':2}[axis];cut[k]=f'({cut[k]})-1 mm'
    cyl(body,id_,f'({h})+2 mm',cut,axis,'cut',body+' bore')

def hole(body,d,base,h,axis='Z',label='clearance hole'):
    cyl(body,d,h,base,axis,'cut',body+' '+label)

def hexcut(body,af,h,center,axis='Z'):
    # Expression-placed vertices are fixed and remain driven by fit parameters.
    x,y,z=center
    dirs={'Z':([1,0,0],[0,1,0]),'X':([0,1,0],[0,0,1]),'Y':([1,0,0],[0,0,-1])}
    u,v=dirs[axis]
    nm=feature(body+' nut pocket profile')
    cmd('sketch.create',plane={'origin':[x,y,z],'x_dir':u,'y_dir':v},name=nm)
    pts=[[f'({af})/sqrt(3)*{math.cos(math.radians(a)):.12f}',f'({af})/sqrt(3)*{math.sin(math.radians(a)):.12f}'] for a in (30,90,150,210,270,330)]
    cmd('sketch.line',points=pts,closed=True,connect=False)
    cmd('sketch.finish')
    cmd('solid.extrude',sketch=nm,distance=h,operation='cut',targets=[body],name=feature(body+' captive nut'))

def hexbody(body,af,h,center):
    nm=feature(body+' profile')
    cmd('sketch.create',plane={'origin':center,'x_dir':[1,0,0],'y_dir':[0,1,0]},name=nm)
    pts=[[f'{af} mm/sqrt(3)*{math.cos(math.radians(a)):.12f}',f'{af} mm/sqrt(3)*{math.sin(math.radians(a)):.12f}'] for a in (30,90,150,210,270,330)]
    cmd('sketch.line',points=pts,closed=True,connect=False)
    cmd('sketch.constraint.fix',entities=[f'l{i}' for i in range(1,7)],fixed=True)
    cmd('sketch.finish')
    cmd('solid.extrude',sketch=nm,distance=h,operation='new',body_name=body,name=feature(body))

def part(body,kind,material,orientation=(0,0,0),notes='',sourcing=None):
    default_sourcing = {'print': 'print', 'metal': 'fabricate', 'purchased': 'buy', 'space': 'reservation'}
    parts.append(dict(name=body,kind=kind,sourcing=sourcing or default_sourcing[kind],
                      material=material,print_rotation_deg=list(orientation),notes=notes))

def rotate(body,a):cmd('solid.move',bodies=[body],axis=[0,0,1],origin=[0,0,0],angle=f'{a} deg',name=feature(body+' quadrant placement'))

def quarter(body):
    box(body,[501,1000,300],['rt_seam/2-501 mm',-500,-1],'cut','quadrant X seam')
    box(body,[1000,501,300],[-500,'rt_seam/2-501 mm',-1],'cut','quadrant Y seam')

def join(target,tool):cmd('solid.combine',target=target,tools=[tool],operation='join')

def slot_x(body,x,y,z,length,width,depth):
    # Three overlapping cuts; extension beyond the surface avoids coincident caps.
    box(body,[length-width,width,depth],[x-(length-width)/2,y-width/2,z],'cut','adjustment slot web')
    for sx in [-1,1]:hole(body,width,[x+sx*(length-width)/2,y,z],depth,label='adjustment slot end')

stage('01-core')
group('RT01 - stationary core')
for n,v,comment in [
 ('rt_r','160 mm','Platter radius; revision 4 verification is for 160 mm only. Recheck anchors and clearance after changes.'),
 ('rt_column_bore','10.30 mm','Printed sleeve bore, DIAMETRAL; calibrate a full P11 first article.'),
 ('rt_fixture_boss_bore','16.30 mm','Printed pocket over the metal fixture boss; coupon then quadrant first article.'),
 ('rt_seam','0.40 mm','Total printed section seam gap; 0.30–0.60 mm, seal after assembly.'),
 ('rt_m3','3.4 mm','Printed M3 clearance; calibrate coupon.'),
 ('rt_m4','4.5 mm','Printed M4 clearance; calibrate coupon.'),
 ('rt_m5','5.5 mm','Printed M5 clearance; calibrate coupon.'),
 ('rt_m6','6.6 mm','Printed M6 clearance; calibrate coupon.'),
 ('rt_m3_h','3.5 mm','Printed horizontal M3 hole; separate calibration from vertical holes.'),
 ('rt_m4_h','4.6 mm','Printed horizontal M4 hole; separate calibration from vertical holes.'),
 ('rt_anchor_nut_af','7.4 mm','F21 captive M4 nyloc pocket across flats; calibrate actual nut fit and low-torque retention on a first article.'),
 ('rt_m5_h','5.6 mm','Printed horizontal M5 hole; separate calibration from vertical holes.'),
 ('rt_motor_pilot_h','22.6 mm','Horizontal printed NEMA17 pilot; first-article calibration.'),
 ('rt_motor_l','80 mm','Motor plus encoder reserved length; range 60–80 mm.'),
 ('rt_lid_gasket_stock_w','2 mm','Solid EPDM stock ring width, centred in the 3.5 mm groove; review gland fill and compression force before changing.'),
 ('rt_lid_gasket_stock_t','2 mm','Solid EPDM uncompressed thickness; 1.5 mm hard-stop height. Stock volume must fit the gland with tolerance/swell allowance.'),
 ('rt_insert','4.0 mm','RX-M3x5.7 nominal insert pilot; verify printed coupon before installing.')]:
    cmd('parameters.add',name=n,expression=v,comment=comment,favorite=True)
b='M01 aluminium base plate';box(b,[164,184,8],[-82,-82,4]);part(b,'metal','Aluminium, machined datum')
for x in [-64,64]:
 for y in [-64,64]:hole(b,6.6,[x,y,3],10,label='bench fixing')
posts=[(66,0),(-66,0),(36,-58),(-36,-58)]
# A03/A06: round/slot locating-column seats, local threaded bosses and an axial guide.
for x,y in posts:
 cyl(b,14,2.2,[x,y,2],op='join',label='column thread engagement boss')
 hole(b,5,[x,y,1],12,label='M6 tap drill, 9 mm below locating recess')
 if (x,y)==(-66,0):slot_x(b,x,y,11,10.52,10.02,2)
 else:hole(b,10.02 if (x,y)==(66,0) else 10.4,[x,y,11],2,label='column locating recess')
box(b,[60,6,2.2],[-30,52.5,11.8],'join','machined axial guide tongue')
for x,y in [(-52,18),(52,18),(-70,92),(70,92)]:hole(b,4.2,[x,y,3],10,label='M5 cartridge tap drill')
for y in [20,48]:hole(b,4.2,[72,y,3],10,label='M5 motor-pod tap drill')
for i,(x,y) in enumerate([(x,y) for x in [-64,64] for y in [-64,64]],1):
 b=f'M0{2+i} metal bench spacer';ring(b,18,6.6,4,0,(x,y));part(b,'purchased','Metal spacer')
for i,(x,y) in enumerate(posts,1):
 b=f'M1{i} steel locating column';ring(b,10,6.2,72,11,(x,y));part(b,'metal','Turned steel column, matched ground ends',notes='72 mm overall; 1 mm locates in each plate. See machining inspection table.')
 b=f'P1{i} column sleeve';ring(b,22,'rt_column_bore',69.5,12,(x,y));part(b,'print','PETG')
b='M02 aluminium bearing seat';ring(b,156,94,8,82);part(b,'metal','Aluminium, machined datum')
# Interrupted outer-ring register clears the column washers and bearing corner radius.
for q in range(4):
 a=math.radians(45+90*q);t=f'tool bearing register pad {q}'
 cyl(t,6,2.2,[61.5*math.cos(a),61.5*math.sin(a),89.8])
 hole(t,120.02,[0,0,89],4,label='outer bearing locating surface')
 hole(t,121.6,[0,0,89.7],1.1,label='bearing corner relief')
 join(b,t)
for i in range(8):
 a=math.radians(i*45+22.5);hole(b,5.5,[52.5*math.cos(a),52.5*math.sin(a),81],10,label='outer bearing bolt')
for x,y in posts:
 hole(b,6.6,[x,y,81],10,label='column clamp')
 if (x,y)==(-66,0):slot_x(b,x,y,81,10.52,10.02,2)
 else:hole(b,10.02 if (x,y)==(66,0) else 10.4,[x,y,81],2,label='column locating recess')
cyl(b,18,8,[*SENSOR_XY,82],op='join',label='supported sensor nut mounting pad')
hole(b,8.4,[*SENSOR_XY,81],10,label='axial M8 home sensor')
b='B01 bearing outer ring reference';ring(b,120,85.2,15,90);part(b,'purchased','RU85-size bearing envelope',notes='Ring split is illustrative; verify purchased variant.')
for i in range(8):
 a=math.radians(i*45+22.5);x=52.5*math.cos(a);y=52.5*math.sin(a)
 hole(b,5.5,[x,y,89],17);hole(b,9.5,[x,y,99.6],6.4,label='bearing counterbore')

stage('02-drive')
group('RT01 - worm cartridge')
b=CARRIER;box(b,[156,94,8],[-78,6.5,12]);part(b,'metal','6061-T6 aluminium, machined in one setup',notes='A01/A06: no separate block bolts; matched bearing seats and sliding guide.')
box(b,[68,6.02,2.3],[-34,52.49,11.9],'cut','axial guide groove')
for y in [20,48]:slot_x(b,72,y,11,12.6,6.6,2)
for x in [-66,66]:hole(b,30,[x,0,11],10,label='column sleeve adjustment clearance')
for x,y in [(-52,18),(52,18),(-70,92),(70,92)]:slot_x(b,x,y,11,11.5,5.5,10)
for side in [-1,1]:
 suffix='left' if side<0 else 'right'
 lo=-66 if side<0 else 40
 b=CARRIER;box(b,[26,60,60.2],[lo,25.5,19.8],'join','integral bearing support')
 hole(b,15.3,[lo-1,55.5,50],28,'X','shaft clearance')
 pocket=-67 if side<0 else 54.95
 hole(b,35.01,[pocket,55.5,50],12.05,'X','measured-fit bearing seat, depth 11.05')
 for y in [32.5,78.5]:
  for z in [27,73]:hole(b,3.3,[-67 if side<0 else 56,y,z],11,'X','M4 retainer tap drill; 9 mm full thread')
 capx=-70.05 if side<0 else 66.05
 b=f'M61 worm bearing retainer {suffix}';box(b,[4,54,54],[capx,28.5,23]);part(b,'metal','Machined aluminium retainer',notes='0.10 mm outer-race boss; select M62 shim from measured bearing width and pocket depth.')
 cyl(b,34.9,.10,[-66.05 if side<0 else 65.95,55.5,50],'X','join','outer-race retaining boss')
 hole(b,16,[capx-1,55.5,50],6,'X')
 hole(b,28,[-66.6 if side<0 else 65.8,55.5,50],.8,'X','inner-ring noncontact relief')
 for y in [32.5,78.5]:
  for z in [27,73]:hole(b,4.5,[capx-1,y,z],6,'X')
 b=f'M62 retainer shim {suffix}';box(b,[.05,54,54],[-66.05 if side<0 else 66,28.5,23]);part(b,'purchased','Steel shim, selected thickness; CAD 0.05 mm')
 hole(b,35.5,[-67 if side<0 else 65,55.5,50],3,'X')
 for y in [32.5,78.5]:
  for z in [27,73]:hole(b,4.5,[-67 if side<0 else 65,y,z],3,'X')
 b=f'B02 worm support bearing {suffix}';ring(b,35,15,11,50,(-65.95 if side<0 else 54.95,55.5),'X');part(b,'purchased','7202 bearing envelope')
# Apply head relief after the integral blocks are joined. These pockets clear
# installed hardware to Z21; they do not provide a through-tool route.
for x in [-64,64]:hole(CARRIER,25,[x,64,11],10,label='core bench bolt head relief; tighten before carrier installation')
b='B03 worm shaft reference';cyl(b,15,177,[-78,55.5,50],'X');part(b,'purchased','Steel shaft machining reference',notes='Key, shoulders, locknuts and preload stack require fabrication drawing.',sourcing='fabricate')
b='B04 duplex worm envelope';cyl(b,35,36,[-22,55.5,50],'X');cyl(b,25,14,[14,55.5,50],'X','join');hole(b,15,[-23,55.5,50],52,'X');part(b,'purchased','KHK KWGDL2-R1 reference',notes='Finish bore 15 mm proposed. Tooth envelope, not meshing tooth CAD.')
b='B05 clamp coupling reference';ring(b,25,15,25,50,(78,55.5),'X');cyl(b,25,15,[103,55.5,50],'X','join');hole(b,5,[102,55.5,50],17,'X');part(b,'purchased','Metal coupling 15/5 mm envelope')
b='tool motor support riser';box(b,[153.5,82,8],[82.5,15,4])
for y in [35,77]:hole(b,6.6,[220,y,3],10,label='bench anchor')
for x in [116,138]:
 for y in [32,79]:hole(b,4.2,[x,y,3],10,label='M5 motor bracket thread')
for x in [171,225]:
 for y in [21,91]:
  hole(b,3.3,[x,y,3],10,label='M4 hood thread')
b='P24 NEMA17 motor bracket';box(b,[38,62,8],[96,24.5,12]);box(b,[6,62,62],[112,24.5,18],'join');part(b,'print','PETG',(90,0,0),'Print L-shaped side on bed; clean motor pilot after support removal.')
# Shaft pilot and standard NEMA17 screw square.
hole(b,'rt_motor_pilot_h',[111,55.5,50],8,'X','motor pilot')
for y in [40,71]:
 for z in [34.5,65.5]:hole(b,'rt_m3_h',[111,y,z],8,'X','NEMA17 fixing')
for x in [104,126]:
 for y in [32,79]:hole(b,'rt_m5_h',[x,y,11],10)
cmd('solid.move',bodies=['P24 NEMA17 motor bracket'],translate=[12,0,0],name='Motor bracket clearance shift')
b='B06 NEMA17 motor and encoder envelope';box(b,['rt_motor_l',42.3,42.3],[118,34.35,28.85]);cyl(b,22,2,[116,55.5,50],'X','join');cyl(b,5,24,[94,55.5,50],'X','join');part(b,'purchased','Matched closed-loop NEMA17, envelope')
cmd('solid.move',bodies=['B06 NEMA17 motor and encoder envelope'],translate=[12,0,0],name='Motor clearance shift')
# A05: axial sensor keeps the complete package away from the rib sweep.
cmd('component.activate',component='RT01 - stationary core')
b='B08 axial home sensor reference';cyl(b,8,50,[*SENSOR_XY,48.5]);part(b,'purchased','SICK IME08-02BPSZT0S mechanical reference',notes='M8x1; 50 mm envelope; sensing face Z98.5. Electrical integration remains pending.')
for label,z in [('upper',90),('lower',78)]:
 b=f'B13 sensor {label} jam nut';hexbody(b,13,4,[*SENSOR_XY,z]);hole(b,8.2,[*SENSOR_XY,z-1],6);part(b,'purchased','M8x1 sensor nut AF13, conservative 4 mm thickness')
b='B09 sensor connector and cable reservation';cyl(b,12,25,[*SENSOR_XY,23.5]);box(b,[12,55,12],[SENSOR_XY[0]-6,SENSOR_XY[1]-55,23.5],'join');part(b,'space','Connector and initial cable bend reservation',notes='Select matching M8 cordset and verify actual bend radius; no routing claim beyond this reservation.')
b='B07 output encoder reserved volume';cyl(b,40,16,[0,0,22]);part(b,'space','Output encoder keep-out',notes='Optional encoder; mounting/shaft interface not yet selected.')

stage('03-rotor')
group('RT01 - rotating table',False)
b='B10 bearing inner ring reference';ring(b,84.8,55,15,90);part(b,'purchased','RU85-size bearing envelope')
for i in range(8):
 a=math.radians(i*45);hole(b,4.2,[32.5*math.cos(a),32.5*math.sin(a),89],17,label='M5 thread envelope')
b='B11 duplex wheel envelope';cyl(b,86,18,[0,0,41]);cyl(b,45,15,[0,0,59],op='join');hole(b,15,[0,0,40],35);part(b,'purchased','KHK AGDL2-40R1 reference',notes='Four M5 hub holes require secondary machining; tooth blank only.')
for x,y in [(15,0),(0,15),(-15,0),(0,-15)]:hole(b,4.2,[x,y,62],13,label='M5 hub attachment tap drill')
b=HUB;cyl(b,150,10,[0,0,106])
cyl(b,76,2,[0,0,105],op='join');cyl(b,44,32,[0,0,74],op='join')
cyl(b,54.98,14,[0,0,90],op='join',label='bearing concentric pilot')
cyl(b,53.5,1.2,[0,0,103.9],op='join',label='bearing shoulder relief')
cyl(b,14.98,7,[0,0,67],op='join',label='wheel concentric pilot')
# Relieve the shoulder without removing the neck/core.
t='tool wheel shoulder relief';ring(t,16,14.5,.5,73.5);cmd('solid.combine',target=b,tools=[t],operation='cut')
part(b,'metal','6061-T6 aluminium, machined registered hub',notes='No printed torque/clamp interface. Finish pilots to measured purchased bores; see machining table.')
for x,y in [(15,0),(0,15),(-15,0),(0,-15)]:
 hole(b,5.5,[x,y,73],38,label='M5 wheel through bolt');hole(b,10.5,[x,y,110],7,label='M5x45 recessed head')
for i in range(8):
 a=math.radians(i*45);x=32.5*math.cos(a);y=32.5*math.sin(a)
 hole(b,5.5,[x,y,104],13,label='inner bearing attachment');hole(b,10.5,[x,y,110],7,label='M5x20 recessed head')
for sx in [-1,1]:
 for sy in [-1,1]:
  for x,y in [(65*sx,22*sy),(22*sx,65*sy)]:hole(b,4.2,[x,y,101],16,label='M5 platter tapped through hole')
  x=47*sx;y=47*sy
  cyl(b,16,5.2,[x,y,115.8],op='join',label='raised metal fixture boss')
  hole(b,5,[x,y,110],12,label='blind M6 fixture tap drill; 9 mm full thread from Z121')
  cmd('solid.cone',diameter=0.01,top_diameter=5,height=1.5,base=[x,y,108.5],operation='cut',targets=[b],name=feature('blind fixture drill point'))
# A04: one pin plus a radial slot transmits torque without a second radial locator.
px=py=15/math.sqrt(2)
hole(HUB,3.99,[px,py,73.9],6.9,label='drive pin press bore; finish to measured pin')
t='tool wheel radial drive slot';box(t,[2,4.01,6.3],[14,-2.005,67.8]);
for x in [14,16]:cyl(t,4.01,6.3,[x,0,67.8],op='join')
rotate(t,45);cmd('solid.combine',target='B11 duplex wheel envelope',tools=[t],operation='cut')
b='M21 wheel drive pin';cyl(b,4,12,[px,py,68.5]);part(b,'purchased','Ground hardened-steel pin, nominal Ø4 x 12',notes='6.5 mm hub engagement; matched slot total tangential clearance 0.005–0.010 mm.')
# Steel target is screwed into the metal hub; no unsupported glued flag.
cyl(HUB,14,4.3,[*SENSOR_XY,102.7],op='join',label='retained target mounting boss')
hole(HUB,2.5,[*SENSOR_XY,102],7.2,label='M3 target retention tap drill')
b='B12 retained steel home target';cyl(b,12,3,[*SENSOR_XY,99.7]);hole(b,3.4,[*SENSOR_XY,99],5)
cmd('solid.cone',diameter=6.2,top_diameter=3.4,height=1.4,base=[*SENSOR_XY,99.7],operation='cut',targets=[b],name=feature('recessed target screw'))
part(b,'metal','Mild-steel target Ø12 x 3 mm, M3 countersunk',notes='Sensing face Z99.7; nominal gap 1.2 mm. F25 M3x8 installs upward.')
for q in range(4):
 b=f'P3{q+1} platter quadrant';cyl(b,'2*rt_r',12,[0,0,116])
 # Downward skirt, as an annulus made separately then united with the deck.
 t=f'tool skirt {q}';ring(t,'2*rt_r','2*rt_r-8 mm',14,103);join(b,t)
 quarter(b)
 box(b,['rt_r*0.375',12,19],['rt_r*0.5','rt_r*0.1875',98],'join','radial rib A')
 box(b,[12,'rt_r*0.375',19],['rt_r*0.1875','rt_r*0.5',98],'join','radial rib B')
 for x,y in [(65,22),(22,65)]:hole(b,'rt_m5',[x,y,115],14);hole(b,10.5,[x,y,125],4,label='flush M5 button head')
 hole(b,'rt_m6',[47,47,115],14,label='M6 fixture point')
 hole(b,'rt_fixture_boss_bore',[47,47,115],6.2,label='raised metal fixture boss clearance')
 rotate(b,90*q);part(b,'print','PETG',(180,0,0),'Work face on bed; seal quadrant seams after assembly.')

stage('04-covers')
group('RT01 - removable shrouds')
for q in range(4):
 b=f'P4{q+1} fixed housing quadrant';cyl(b,'2*rt_r-12 mm',114,[0,0,0])
 cyl(b,'2*rt_r+8 mm',2.5,[0,0,0],op='join',label='floor perimeter')
 cyl(b,'2*rt_r+8 mm',3,[0,0,97],op='join',label='outer drainage gutter')
 t=f'tool gutter lip {q}';ring(t,'2*rt_r+8 mm','2*rt_r+4 mm',2,100);join(b,t)
 hole(b,'2*rt_r-20 mm',[0,0,2.5],116,label='drive cavity')
 box(b,[152,152,5],[-76,-76,-1],'cut','metal core opening')
 quarter(b)
 # Broad backed seam tabs at the two radial boundaries.
 box(b,[12,8,84],['rt_seam/2','rt_r-15 mm',12],'join','seam flange Y')
 box(b,[8,12,84],['rt_r-15 mm','rt_seam/2',12],'join','seam flange X')
 for z in [25,90]:
  hole(b,'rt_m4_h',[6,'rt_r-16 mm',z],12,'Y','horizontal seam screw')
  hole(b,'rt_m4_h',['rt_r-16 mm',6,z],12,'X','horizontal seam screw')
  hole(b,10,[6,'rt_r-7 mm',z],4,'Y','flat outer washer seat')
  hole(b,10,['rt_r-7 mm',6,z],4,'X','flat outer washer seat')
 hole(b,5,['(rt_r+1 mm)*cos(45 deg)','(rt_r+1 mm)*sin(45 deg)',96],8,label='external gutter drain')
 # R4-10: leave the drain's drop path open through the lower flange to its rim.
 # This avoids a second catch surface; collection below the table is still required.
 t=f'tool drain floor relief {q}'
 box(t,[12,8,5],['rt_r-4 mm',-4,-1]);rotate(t,45)
 cmd('solid.combine',target=b,tools=[t],operation='cut')
 hole(b,'rt_m5',[88,108,-1],5,label='housing bench fixing with supported washer land')
 rotate(b,90*q)
 if q==0:
  box(b,[130,82.8,96.9],[110,14.6,-1],'cut','motor enclosure passage')
  box(b,[156.5,83,5],[63.5,14.5,-1],'cut','motor foundation passage')
 part(b,'print','PETG',notes='Support external gutter underside; keep supports away from gasket faces.')
for q in range(4):
 b=f'P45 seam backing strip {q+1}';box(b,[24,8,84],[-12,'rt_r-23 mm',12]);
 for x in [-6,6]:
  for z in [25,90]:hole(b,'rt_m4',[x,'rt_r-24 mm',z],10,'Y')
 rotate(b,90*q);part(b,'print','PETG',(90,90*q,0),'Assembly rotation is cancelled; all four strips print broad face down.')
b='P46 motor service hood';box(b,[126,82,82],[110,15,12]);box(b,[118,74,80],[114,19,11],'cut','motor cavity');hole(b,'2*rt_r-11.2 mm',[0,0,-1],100,label='curved housing mating edge');part(b,'print','PETG',(180,0,0),'R4-05: release curved RTV joint and disconnect gland cables; withdraw +X 70 mm before lifting 30 mm. Replace disturbed gasket/RTV after service.')
for x in [171,225]:
 for y in [21,91]:
  # R4-05: overlap the roof by 1 mm, closing the former 3 mm inner-side gap.
  # The lower 1 mm is OD8 so withdrawal clears the OD18 anchor washers.
  cyl(b,10,79,[x,y,13],op='join',label='continuous roof-to-stop hood screw column')
  cyl(b,8,2,[x,y,12],op='join',label='hood post foot clears anchor washer sweep');hole(b,'rt_m4',[x,y,11],84)
# Core perimeter gasket reference, compressed 1.5 mm under the plate overlap.
b='B20 core static gasket';box(b,[164,164,1.5],[-82,-82,2.5]);box(b,[152,152,3],[-76,-76,2],'cut','gasket opening');part(b,'purchased','EPDM 2 mm, compressed 25%')


# Hard stops establish motor-hood gasket compression; the curved edge gets RTV.
cmd('component.activate',component='RT01 - worm cartridge')
for x in [171,225]:
 for y in [21,91]:
  cyl('tool motor support riser',10,1.5,[x,y,12],op='join',label='motor hood gasket hard stop')
  hole('tool motor support riser',3.3,[x,y,11],4,label='M4 hard stop thread')
cmd('component.activate',component='RT01 - removable shrouds')
cmd('solid.move',bodies=['P46 motor service hood'],translate=[0,0,1.5],name='Motor hood gasket stand-off')
for z in [36,70]:hole('P46 motor service hood',16.5,[231,55.5,z],6,'X','motor cable gland provision')
b='B25 motor hood gasket';box(b,[126,82,1.5],[110,15,12]);box(b,[118,74,3],[114,19,11.5],'cut','motor seal centre');hole(b,'2*rt_r-11.2 mm',[0,0,11],4,label='curved seal edge');part(b,'purchased','EPDM 2 mm compressed to 1.5 mm; RTV at curved transition')
for x in [171,225]:
 for y in [21,91]:hole(b,5.5,[x,y,11],4,label='sealed hood screw clearance')
cmd('component.activate',component='RT01 - worm cartridge')
cmd('solid.combine',target='tool motor support riser',tools=['B25 motor hood gasket'],operation='cut',keep_tools=True)

stage('05-electronics')
group('RT01 - electronics base')
cy=-224
b='P50 electronics service box';box(b,[168,112,76],[-84,cy-56,4]);box(b,[140,84,10],[-70,cy-42,74],'cut','service opening');box(b,[160,104,66],[-80,cy-52,8],'cut','electronics chamber');part(b,'print','PETG',notes='Support underside of inward top rim; keep top gasket land clean.')
# Lid bosses provide full insert engagement below the top sealing land.
for x,y in [(-78,-50),(78,-50),(-78,50),(78,50),(-42,-51),(42,-51),(-42,51),(42,51),(-79,0),(79,0)]:
 cyl(b,10,12,[x,cy+y,68],op='join',label='lid insert boss')
# R4-11: widen inward only, preserving insert separation and a 2 mm inner land.
# With the lid at Z80 the closed groove is 3.5 mm wide x 1.5 mm high.
for x in [-75.5,72]:box(b,[3.5,95,2],[x,cy-47.5,78.5],'cut','lid gasket long groove')
for y in [cy-47.5,cy+44]:box(b,[144,3.5,2],[-72,y,78.5],'cut','lid gasket end groove')
lidpoints=[(x,cy+y) for x,y in [(-78,-50),(78,-50),(-78,50),(78,50),(-42,-51),(42,-51),(-42,51),(42,51),(-79,0),(79,0)]]
for x,y in lidpoints:hole(b,'rt_insert',[x,y,73],8,label='M3 insert pilot')
# Driver heat spreader is exposed through the floor and sealed around its perimeter.
box(b,[100,56,6],[-50,cy-28,3],'cut','heat spreader opening')
for x in [-55.5,55.5]:
 for y in [cy-34.5,cy+34.5]:hole(b,'rt_m3',[x,y,3],6,label='heat spreader clamp')
# Tray posts fit through the top opening. The rear cable glands are stationary.
for x in [-65,65]:
 for y in [cy-34,cy+34]:
  cyl(b,10,47,[x,y,8],op='join',label='tray post');hole(b,'rt_insert',[x,y,47],9,label='tray insert pilot')
for x in [-48,0,48]:hole(b,16.5,[x,cy-57,65],6,'Y','M16 gland provision')
# Dry box mounting holes sit in the corner bosses.
for x in [-75,75]:
 for y in [cy-47,cy+47]:
  hole(b,'rt_m4',[x,y,3],7,label='bench fixing from below')
  # The rim blocks a straight key from above. Capture a DIN985 M4 nut
  # above the unchanged floor; tighten the reversed bolt from below the bench.
  # Insert the seal/washer through the inward side opening before the nut.
  cyl(b,14,8,[x,y,8],op='join',label='bench anchor captive nut boss')
  hole(b,9.4,[x,y,8],2,label='bench anchor seal and washer recess')
  box(b,[9,9.4,2],[x if x<0 else x-9,y-4.7,8],'cut','inward seal and washer loading slot')
  hexcut(b,'rt_anchor_nut_af',6.5,[x,y,10])
b='M30 driver heat spreader';box(b,[118,76,3],[-59,cy-38,8.75]);part(b,'metal','Aluminium heat spreader, exposed underside')
for x in [-55.5,55.5]:
 for y in [cy-34.5,cy+34.5]:
  hole(b,3.4,[x,y,8],5)
  cmd('solid.cone',diameter=3.4,top_diameter=6.4,height=1.5,base=[x,y,10.25],axis='Z',operation='cut',targets=[b],name=feature('flush M3 heat spreader clamp'))
# Slots for the future driver mounting pattern, with space for washers.
# Leave the exposed heat barrier solid. Final driver fasteners must be sealed.
b='B21 heat spreader gasket';box(b,[108,64,0.75],[-54,cy-32,8]);box(b,[102,58,2],[-51,cy-29,7.5],'cut','seal centre');part(b,'purchased','Closed-cell gasket 1 mm compressed to 0.75 mm')
for x in [-55.5,55.5]:
 for y in [cy-34.5,cy+34.5]:hole(b,7,[x,y,7.5],2,label='compression shim corner relief')

for i,(x,y) in enumerate([(x,y) for x in [-55.5,55.5] for y in [cy-34.5,cy+34.5]],1):
 b=f'M3{i} heat-spreader compression stop';ring(b,6.5,3.4,0.75,8,(x,y));part(b,'purchased','Metal shim washer 0.75 mm')
b='B22 driver packaging envelope';box(b,[118,76,35],[-59,cy-38,12]);part(b,'space','Motor driver keep-out',notes='Not selected electronics; includes component height, excludes wiring.')
group('RT01 - controller tray')
b='P51 removable controller tray';box(b,[138,80,3],[-69,cy-40,55]);part(b,'print','PETG')
for x in [-65,65]:
 for y in [cy-34,cy+34]:hole(b,'rt_m3',[x,y,54],5)
for y in [cy-23,cy+23]:slot_x(b,0,y,54,100,3.4,5)
for x in [-53,53]:box(b,[10,28,5],[x-5,cy-14,54],'cut','cable passage')
b='B23 controller packaging envelope';box(b,[80,55,20],[-40,cy-27.5,58]);part(b,'space','Motion controller keep-out')
group('RT01 - electronics lid')
b='P52 electronics lid';box(b,[168,112,4],[-84,cy-56,80]);part(b,'print','PETG')
for x,y in lidpoints:hole(b,'rt_m3',[x,y,79],6)
# R4-11: stock ring is 149.5 x 93.5 outside / 145.5 x 89.5 inside.
# Preserve its volume when showing compression to the 1.5 mm hard stop:
# 2 mm stock width x 2 mm stock thickness -> 8/3 mm installed width.
# The 3.5 x 1.5 mm gland is 2509.5 mm3; stock/installed ring is 1912 mm3 (76.19%).
gw='rt_lid_gasket_stock_w*rt_lid_gasket_stock_t/1.5 mm'
b='B24 lid gasket';box(b,[f'147.5 mm+({gw})',f'91.5 mm+({gw})',1.5],[f'-73.75 mm-({gw})/2',f'{cy-45.75} mm-({gw})/2',78.5]);box(b,[f'147.5 mm-({gw})',f'91.5 mm-({gw})',3],[f'-73.75 mm+({gw})/2',f'{cy-45.75} mm+({gw})/2',78],'cut','gasket centre');part(b,'purchased','Solid EPDM stock 2 x 2 mm section, compressed to 1.5 mm',notes='Stock cut ring baseline OD 149.5 x 93.5 / ID 145.5 x 89.5 mm; STEP shows volume-conserving compressed profile, not the cutting outline. Nominal gland fill 76.19%; compound, tolerance, swell and compression force require validation.')


# Raise the sealed service box for a separately purchased external heat sink.
cmd('component.activate',component='RT01 - electronics base')
b='B26 external heatsink reference';box(b,[98,54,3],[-49,cy-27,5.25])
for offset in range(-24,25,6):box(b,[98,1.5,16],[-49,cy+offset-0.75,-9.75],'join','external heatsink fin')
part(b,'purchased','Aluminium finned heatsink envelope',notes='98 x 54 x 18 envelope; final part and sealed mounting need selection.')
b='B27 thermal interface pad';box(b,[98,54,0.5],[-49,cy-27,8.25]);part(b,'purchased','Thermally conductive adhesive pad reference')
group('RT01 - electronics feet')
for i,(x,y) in enumerate([(x,cy+y) for x in [-75,75] for y in [-47,47]],1):
 b=f'P53 electronics foot {i}';ring(b,20,'rt_m4',28,0,(x,y));part(b,'print','PETG')
for component in ['RT01 - electronics base:1','RT01 - electronics lid:1','RT01 - controller tray:1']:
 cmd('occurrence.move',occurrence=component,translate=[0,0,24],move_grounded=True)


stage('06-support-revision')
group('RT01 - motor sole support')
b='M40 stepped motor support';box(b,[172,82,4],[64,15,0]);join(b,'tool motor support riser');part(b,'metal','Machined aluminium sole and integral riser',notes='A04: all-metal anchor stack, no nominally equal printed compression stack.')
box(b,[6,67,2],[76,15,2.5],'cut','sole core gasket clearance X')
box(b,[18,6,2],[64,76,2.5],'cut','sole core gasket clearance Y')
hole(b,18.6,[64,64,-1],6,label='sole bench spacer relief')
for y in [20,48]:
 hole(b,5.5,[72,y,-1],6,label='M5 core coupling clearance')
 cmd('solid.cone',diameter=10.4,top_diameter=5.5,height=2.45,base=[72,y,0],axis='Z',operation='cut',targets=[b],name=feature('underside M5 flush countersink'))
for y in [35,77]:hole(b,6.6,[220,y,-1],6,label='M6 bench anchor')
for x in [116,138]:
 for y in [32,79]:hole(b,4.2,[x,y,-1],6,label='M5 motor bracket through thread')
for x in [171,225]:
 for y in [21,91]:hole(b,3.3,[x,y,-1],6,label='M4 hood through thread')
for i,y in enumerate([35,77],1):
 b=f'B4{i} motor anchor washer';ring(b,18,6.6,1.6,12,(220,y));part(b,'purchased','M6 metal washer OD18 ID6.6 x 1.6 mm')

group('RT01 - arm support bridge')
b='M50 SO100 arm mounting plate';box(b,[228,116,8],[-114,-282,144]);part(b,'metal','Aluminium 8 mm, arm adapter with lid-tool access',notes='F24: four M4x0.7-6H through threads from above; no arm nuts or washers below Z144. Match upper seats to the measured owned foot. Require >=6 mm effective full screw engagement and screw tips >=Z145; conditional screw length follows the measured grip.')
arm_holes=[(27.776497308103686,-189.2250092524069),(31.75,-259.0),(-27.77649730810371,-189.2250092524069),(-31.75,-259.0)]
for x,y in arm_holes:hole(b,3.3,[x,y,143],10,label='SO100 top-down M4x0.7 tap drill; finish through thread')
for x in [-98,98]:
 for y in [-272,-176]:hole(b,6.6,[x,y,143],10,label='M6 bridge flange attachment')
for x,y in lidpoints:hole(b,8,[x,y,143],10,label='lid screw tool access')
# Welded plate fabrication, not an idealised zero-radius folded sheet.
for side,label in [(-1,'left'),(1,'right')]:
 b=f'M51 steel side channel {label}'
 x=-114 if side<0 else 110
 fx=-114 if side<0 else 86
 box(b,[4,116,144],[x,-282,0])
 box(b,[28,116,4],[fx,-282,0],'join','stand bottom flange')
 box(b,[28,116,4],[fx,-282,140],'join','stand top flange')
 for y in [-272,-176]:
  hole(b,6.6,[side*98,y,-1],6,label='bench through bolt')
  hole(b,6.6,[side*98,y,139],6,label='top plate bolt')
 part(b,'metal','4 mm welded steel plate, web and two 28 mm flanges',notes='Weld before finish-machining top datum and drilling matched flanges. Rear stays open.')
b='M52 steel front X brace';box(b,[228,4,136],[-114,-166,4])
for points in [[[-82,16],[82,16],[0,58]],[[-82,120],[0,78],[82,120]],[[-98,26],[-16,68],[-98,110]],[[98,26],[98,110],[16,68]]]:
 nm=feature('stand brace lightening window')
 cmd('sketch.create',plane={'origin':[0,-167,0],'x_dir':[1,0,0],'y_dir':[0,0,1]},name=nm)
 cmd('sketch.line',points=[[f'{v} mm' for v in pt] for pt in points],closed=True,connect=False)
 cmd('sketch.constraint.fix',entities=['l1','l2','l3'],fixed=True)
 cmd('sketch.finish')
 cmd('solid.extrude',sketch=nm,distance=-6,operation='cut',targets=[b],name=feature('brace window cut'))
part(b,'metal','4 mm steel, weld vertical edges to both side channels',notes='Front shear bracing; fabrication shop to specify welds from actual loads.')
for i,(x,y) in enumerate([(x,y) for x in [-98,98] for y in [-272,-176]],1):
 b=f'B5{i} bridge anchor washer';ring(b,18,6.6,1.6,152,(x,y));part(b,'purchased','M6 metal washer OD18 ID6.6 x 1.6 mm')

stage('07-presentation')
cmd('component.activate',component='root')
cmd('joint.as_built',type='revolute',a='RT01 - stationary core:1',b='RT01 - rotating table:1',at={'occurrence':'RT01 - stationary core:1','point':[0,0,97.5],'z':[0,0,1]},name='RT01 vertical C axis')
cmd('motion.study',name='RT01 one revolution',steps=16,keys=[{'joint':'RT01 vertical C axis','points':[[0,0],[16,360]]}])
# Label colour distinguishes printable parts, metal, bought parts and space reservations.
for kind,color in [('print','#536D7B'),('metal','#BFC8CD'),('purchased','#A9B0B8'),('space','#48B8CC')]:
 names=[p['name'] for p in parts if p['kind']==kind]
 cmd('appearance.assign',bodies=names,color=color)
cmd('appearance.assign',bodies=[HUB]+[f'P3{q+1} platter quadrant' for q in range(4)],color='#DBE2E3')
cmd('appearance.assign',bodies=['B04 duplex worm envelope','B11 duplex wheel envelope'],color='#BE9553')
cmd('appearance.assign',bodies=['B20 core static gasket','B21 heat spreader gasket','B24 lid gasket','B25 motor hood gasket'],color='#253035')
cmd('appearance.assign',bodies=['P52 electronics lid','P46 motor service hood'],color='#397F87')
cmd('browser.visibility',visible=False,items=['B07 output encoder reserved volume'])
cmd('view.save',name='RT01 assembly',camera={'target':[0,-52,65],'yaw':-0.85,'pitch':0.62,'distance':720})
cmd('view.save',name='RT01 and arm reference',camera={'target':[20,-90,130],'yaw':-0.85,'pitch':0.5,'distance':950})
cmd('view.save',name='RT01 top',camera={'target':[0,-55,70],'yaw':0,'pitch':1.5707,'distance':680})
cmd('explode.create',name='RT01 service access',moves=[{'occurrence':'RT01 - rotating table:1','translate':[0,0,150]},{'occurrence':'RT01 - removable shrouds:1','translate':[0,0,75]},{'occurrence':'RT01 - electronics lid:1','translate':[0,0,120]},{'occurrence':'RT01 - controller tray:1','translate':[0,0,60]}])
cmd('view.apply',view='RT01 and arm reference')

# Stage scripts are suitable for incremental live MCP batches; full script for replay.
(ROOT/'cad').mkdir(exist_ok=True)
(ROOT/'cad/rotary-table-build.json').write_text(json.dumps({'commands':commands},indent=2)+'\n')
for i,(name,start) in enumerate(stages):
 end=stages[i+1][1] if i+1<len(stages) else len(commands)
 (ROOT/f'cad/{name}.json').write_text(json.dumps({'commands':commands[start:end]},indent=2)+'\n')
(ROOT/'cad/parts.json').write_text(json.dumps({'design':'RT-01','revision':REVISION,'units':'mm','parts':parts},indent=2)+'\n')
print(json.dumps({'commands':len(commands),'parts':len(parts),'printed_parts':sum(p['kind']=='print' for p in parts),'stages':[(n,(stages[i+1][1] if i+1<len(stages) else len(commands))-s) for i,(n,s) in enumerate(stages)]},indent=2))
