#!/usr/bin/env python3
"""Separate provisional fixture for one 50 x 50 x 40 mm foam blank.

Main RT-01 CAD/exports are read-only. Baseline clamping includes PETG and is
for low-force foam commissioning only. The optional hard-seat variant needs
enlarged passages in removed platter quadrants; it is not a drop-in upgrade.
"""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import subprocess
import tempfile
from zipfile import ZipFile
from build_drain_catch import add, prism, run, sha, write

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'exports/rotary-table/foam-fixture'
E = ROOT/'docs/audit-evidence/2026-11-18-rt01/service-follow-up'
CLI = '/Applications/SolidCraft.app/Contents/MacOS/solidcraft-cli'
YELLOW, GREY, BLACK = '#F6C915', '#9B9B9B', '#202020'


def box(c, b, size, origin, op='new'):
    add(c, 'solid.box', length=size[0], width=size[1], height=size[2], corner=origin,
        operation=op, **({'body_name': b} if op == 'new' else {'targets': [b]}))


def cyl(c, b, d, h, origin, axis='Z', op='new'):
    add(c, 'solid.cylinder', diameter=d, height=h, base=origin, axis=axis,
        operation=op, **({'body_name': b} if op == 'new' else {'targets': [b]}))


def hexcut(c, b, af, depth, origin, axis='Z', phase=0):
    dirs = {'Z': ([1,0,0],[0,1,0]), 'X': ([0,1,0],[0,0,1])}
    u,v = dirs[axis]
    name=f'{b} nut pocket {len(c)}'
    points=[[af/math.sqrt(3)*math.cos(math.radians(a+phase)), af/math.sqrt(3)*math.sin(math.radians(a+phase))] for a in range(0,360,60)]
    prism(c,b,name,points,dict(origin=origin,x_dir=u,y_dir=v),depth,'cut')


def hexnut(c,b,af,h,origin,axis='Z',phase=0):
    u,v={'Z':([1,0,0],[0,1,0]),'X':([0,1,0],[0,0,1])}[axis]
    points=[[af/math.sqrt(3)*math.cos(math.radians(a+phase)),af/math.sqrt(3)*math.sin(math.radians(a+phase))] for a in range(0,360,60)]
    prism(c,b,b+' hex profile',points,dict(origin=origin,x_dir=u,y_dir=v),h,'new')


def slot(c, b, x,y,z,length,width,depth):
    box(c,b,[length-width,width,depth],[x-(length-width)/2,y-width/2,z],'cut')
    for s in [-1,1]:cyl(c,b,width,depth,[x+s*(length-width)/2,y,z],op='cut')


def color(c,b,value=YELLOW):
    add(c,'appearance.assign',bodies=[b],color=value)


def base(c,b='P56 foam fixture base'):
    box(c,b,[130,130,3],[-65,-65,128])
    for x in [-47,47]:
        for y in [-47,47]:cyl(c,b,6.6,6,[x,y,127],op='cut')
    # Two independent tie loops pass below the base, inside these grooves.
    for x in [-32,32]:
        box(c,b,[6,82,3],[x-3,-41,127],'cut')
        for y in [-40,40]:box(c,b,[6,2,5],[x-3,y-1,127],'cut')
    box(c,b,[4,60,19],[-31,-31,131],'join')
    box(c,b,[56,4,19],[-27,-31,131],'join')
    for q in [0,1]:
        t=f'{b} temporary guide {q}'
        box(c,t,[18,52,5],[25,-26,131])
        if q:add(c,'solid.move',bodies=[t],axis=[0,0,1],origin=[0,0,0],angle='90 deg')
        add(c,'solid.combine',target=b,tools=[t],operation='join')
        t=f'{b} temporary screw tower {q}'
        box(c,t,[8,18,22],[43,-9,131])
        cyl(c,t,4.6,10,[42,0,143],axis='X',op='cut')
        hexcut(c,t,7.4,5.4,[43,0,143],axis='X',phase=30)
        if q:add(c,'solid.move',bodies=[t],axis=[0,0,1],origin=[0,0,0],angle='90 deg')
        add(c,'solid.combine',target=b,tools=[t],operation='join')
    for q in [0,1]:
        for y in [-17,17]:
            x0,y0=(36,y) if not q else (-y,36)
            cyl(c,b,3.4,10,[x0,y0,130.5],op='cut')
            hexcut(c,b,5.9,2.8,[x0,y0,132],phase=90*q)
            if not q:box(c,b,[9,5.9,2.8],[36,y-2.95,132],'cut')
            else:box(c,b,[5.9,9,2.8],[x0-2.95,36,132],'cut')
    color(c,b)


def jaw(c,b='P57 sliding jaw',q=0):
    box(c,b,[15,50,2.5],[27,-25,136])
    box(c,b,[4,50,14],[27,-25,136],'join')
    for y in [-17,17]:slot(c,b,36,y,135.5,9,3.4,4)
    cyl(c,b,4.6,3,[29.2,0,143],axis='X',op='cut')
    if q:add(c,'solid.move',bodies=[b],axis=[0,0,1],origin=[0,0,0],angle='90 deg')
    color(c,b)


def keeper(c,b='P58 open centre keeper'):
    box(c,b,[60,60,3],[-30,-30,174])
    box(c,b,[42,42,5],[-21,-21,173],'cut')
    for x in [-25,25]:box(c,b,[5.4,62,2],[x-2.7,-31,176.4],'cut')
    color(c,b)


def strap_leg(c,b,start,end):
    d=[end[i]-start[i] for i in range(3)];length=math.sqrt(sum(v*v for v in d));d=[v/length for v in d]
    u=[1-d[0]*d[0],-d[0]*d[1],-d[0]*d[2]];norm=math.sqrt(sum(v*v for v in u));u=[v/norm for v in u]
    v=[d[1]*u[2]-d[2]*u[1],d[2]*u[0]-d[0]*u[2],d[0]*u[1]-d[1]*u[0]]
    prism(c,b,b+' section',[[-2.4,-.6],[2.4,-.6],[2.4,.6],[-2.4,.6]],dict(origin=start,x_dir=u,y_dir=v),length,'new')
    color(c,b,BLACK)


def assembly(c):
    names=[]
    b='P56 foam fixture base'
    base(c,b);names.append(b)
    for q in [0,1]:
        b=f'P57 sliding jaw {q+1}';jaw(c,b,q);names.append(b)
    keeper(c);names.append('P58 open centre keeper')
    for b,size,origin in [
        ('REF lower EVA pad',[50,50,2],[-25,-25,131]),
        ('REF fixed X EVA pad',[2,50,14],[-27,-25,136]),
        ('REF fixed Y EVA pad',[50,2,14],[-25,-27,136]),
        ('REF moving X EVA pad',[2,50,14],[25,-25,136]),
        ('REF moving Y EVA pad',[50,2,14],[-25,25,136]),
        ('REF small foam blank',[50,50,40],[-25,-25,133]),
    ]:
        box(c,b,size,origin);color(c,b,'#C8DBCE' if 'blank' in b else BLACK);names.append(b)
    b='REF keeper EVA ring';box(c,b,[50,50,1],[-25,-25,173]);box(c,b,[42,42,3],[-21,-21,172],'cut');color(c,b,BLACK);names.append(b)
    for s in [-1,1]:
        for label,size,origin in [
            ('underbase',[4.8,80,1.2],[32*s-2.4,-40,128.8]),
            ('keeper rail',[4.8,63,1.2],[25*s-2.4,-31.5,176.4]),
            ('head envelope',[12,8,6],[32*s-6,42,136]),
        ]:
            b=f'REF tie {s} {label}';box(c,b,size,origin);color(c,b,BLACK);names.append(b)
        for sy in [-1,1]:
            b=f'REF tie {s} leg {sy}';strap_leg(c,b,[32*s,40*sy,129.4],[25*s,31.5*sy,177]);names.append(b)
    for x in [-47,47]:
        for y in [-47,47]:
            b=f'REF M6 mount screw {x} {y}';cyl(c,b,6,20,[x,y,112.6]);cyl(c,b,10,6,[x,y,132.6],op='join');color(c,b,BLACK);names.append(b)
            b=f'REF M6 mount washer {x} {y}';cyl(c,b,12,1.6,[x,y,131]);cyl(c,b,6.4,3,[x,y,130.5],op='cut');color(c,b,BLACK);names.append(b)
    for q in [0,1]:
        for y in [-17,17]:
            x0,y0=(36,y) if not q else (-y,36)
            b=f'REF jaw retainer {q} {y}';cyl(c,b,3,8,[x0,y0,131]);cyl(c,b,5.7,1.65,[x0,y0,139],op='join');color(c,b,BLACK);names.append(b)
            b=f'REF jaw washer {q} {y}';cyl(c,b,7,.5,[x0,y0,138.5]);cyl(c,b,3.2,2,[x0,y0,138],op='cut');color(c,b,BLACK);names.append(b)
            b=f'REF jaw nut {q} {y}';hexnut(c,b,5.5,2.4,[x0,y0,132.4],phase=90*q);cyl(c,b,3.2,4,[x0,y0,132],op='cut');color(c,b,BLACK);names.append(b)
        b=f'REF M4 adjuster {q}';cyl(c,b,4,25,[29.2,0,143],axis='X');cyl(c,b,7,4,[54.2,0,143],axis='X',op='join')
        if q:add(c,'solid.move',bodies=[b],axis=[0,0,1],origin=[0,0,0],angle='90 deg')
        color(c,b,BLACK);names.append(b)
        b=f'REF M4 locking nut {q}';hexnut(c,b,7,5,[43.4,0,143],axis='X',phase=30);cyl(c,b,4.4,6,[43,0,143],axis='X',op='cut')
        if q:add(c,'solid.move',bodies=[b],axis=[0,0,1],origin=[0,0,0],angle='90 deg')
        color(c,b,BLACK);names.append(b)
    return names


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--model',type=Path,default=ROOT/'michelaingelo.sc');ap.add_argument('--checks-only',action='store_true',help='Keep verified part meshes/native files and refresh only assembly/proofs.');args=ap.parse_args();model=args.model.resolve();before=sha(model)
    OUT.mkdir(parents=True,exist_ok=True);E.mkdir(parents=True,exist_ok=True)
    spec=importlib.util.spec_from_file_location('rt_export',ROOT/'scripts/export_rotary_table.py');exporter=importlib.util.module_from_spec(spec);spec.loader.exec_module(exporter)
    prints=json.loads((OUT/'foam-fixture-manifest.json').read_text())['prints'] if args.checks_only else []
    if args.checks_only:
        assert all(sha(ROOT/p['file'])==p['sha256'] for p in prints)
    sources=[('p56-foam-fixture-base',base,'P56 foam fixture base',1),('p57-sliding-jaw',jaw,'P57 sliding jaw',2),('p58-top-keeper',keeper,'P58 open centre keeper',1)]
    for stem,build,body,qty in ([] if args.checks_only else sources):
        c=[];build(c);path=E/(stem+'-build.json');write(path,dict(commands=c));native=OUT/(stem+'.sc');measure=E/(stem+'-build.measure.json');run(path,save=native,output=measure);Path(str(native)+'.bak').unlink(missing_ok=True)
        with tempfile.TemporaryDirectory(prefix='rt01-fixture-') as td:
            raw=Path(td)/'raw.stl';p=Path(td)/'export.json';write(p,dict(commands=[dict(command='file.export',params=dict(path=str(raw),format='stl',bodies=[body],quality='fine'))]));run(p,model=native)
            mesh=exporter.orient_and_check(raw,OUT/(stem+'.stl'),[0,0,0])
        rec=json.loads(measure.read_text())['bodies'][0];assert rec['closed'];mesh.update(quantity=qty,editable_native_file=str(native.relative_to(ROOT)),editable_native_sha256=sha(native),cad_volume_mm3=rec['volume_mm3']);prints.append(mesh)
        print('PRINT_READY '+mesh['file'],flush=True)
    c=[];moving=assembly(c);add(c,'view.save',name='Provisional foam fixture',camera=dict(target=[0,0,145],yaw=-.7,pitch=.65,distance=260));p=E/'foam-fixture-assembly-build.json';write(p,dict(commands=c));run(p,save=OUT/'foam-fixture-prototype.sc',output=E/'foam-fixture-assembly.measure.json');Path(str(OUT/'foam-fixture-prototype.sc')+'.bak').unlink(missing_ok=True)
    # Segments of each reference tie represent one flexible physical band.
    # Their joined bend envelopes may overlap each other, but no fixture part.
    tie_pairs=[]
    for s in [-1,1]:
        members=[n for n in moving if n.startswith(f'REF tie {s} ')]
        tie_pairs += [[a,b] for i,a in enumerate(members) for b in members[i+1:]]
    own=E/'foam-fixture-internal.probe.json';own_result=E/'foam-fixture-internal.results.json'
    write(own,dict(commands=[dict(command='inspect.interference',params=dict(bodies=moving,exclude_pairs=tie_pairs,budget_s=60))]))
    run(own,model=OUT/'foam-fixture-prototype.sc',results=True,output=own_result)
    internal=json.loads(own_result.read_text())[0]
    assert not any(internal.get(k) for k in ['interferences','unchecked','budget_exceeded','truncated','pairs_not_checked']), internal
    parts=[p['name'] for p in json.loads((ROOT/'cad/parts.json').read_text())['parts']];arm=json.loads((ROOT/'cad/arm-mount-reference.json').read_text())['collision_body_names'];world=parts+arm
    labels={};probe=list(c)
    def check(label,bodies,against):
        labels[str(len(probe))]=label;add(probe,'inspect.clearance',bodies=bodies,against=against,nearest=3)
    # Mount-shank threads intentionally enter the metal hub; remaining bodies are checked separately.
    bolts=[n for n in moving if n.startswith('REF M6 mount screw')]
    check('Installed fixture except thread contact',[n for n in moving if n not in bolts],world)
    check('Mount screws except designated hub thread',bolts,[n for n in world if n!='M20 registered output hub'])
    # Complete radial sweep bounds cover every angle, not just sampled poses.
    low='REVIEW complete lower fixture sweep';cyl(probe,low,184,11,[0,0,128]);check('Complete lower sweep',[low],world)
    high='REVIEW complete upper fixture sweep';cyl(probe,high,128,48,[0,0,131]);check('Complete upper sweep',[high],world)
    previous=0
    for angle in [0,30,60,90,120,150,180,210,240,270,300,330,360]:
        if angle:add(probe,'solid.move',bodies=moving,axis=[0,0,1],origin=[0,0,0],angle=f'{angle-previous} deg')
        add(probe,'joint.drive',joint='RT01 vertical C axis',value=angle,quiet=True)
        check(f'Fixture at C{angle}',[n for n in moving if n not in bolts],world)
        check(f'Mount threads at C{angle}',bolts,[n for n in world if n!='M20 registered output hub']);previous=angle
    add(probe,'document.inspect',measure=False,sketch_counts=True)
    path=E/'foam-fixture-install-rotation.probe.json';write(path,dict(commands=probe));result=E/'foam-fixture-install-rotation.results.json';run(path,model=model,results=True,output=result)
    r=json.loads(result.read_text());checks={label:r[int(i)] for i,label in labels.items()};write(E/'foam-fixture-clearance-summary.json',checks)
    assert all(not x['overlaps'] and not x['unchecked'] and not x.get('truncated') for x in checks.values()), {k:v['overlaps'] for k,v in checks.items() if v['overlaps']}
    assert sha(model)==before
    manifest=dict(design='Provisional small foam fixture',prints=prints,source_native_sha256=before,
                  foam=dict(material='Rigid craft foam, provisional low-force commissioning only',dimensions_mm=[50,50,40],bottom_z_mm=133,top_z_mm=173,maximum_blank_mass_kg=.10,provisional_working_window_mm=[30,30,20],working_zone_z_mm=[153,173]),
                  mount=dict(pattern_xy_mm=[[x,y] for x in [-47,47] for y in [-47,47]],screw='4 x M6x20 ISO4762',washers='4 x ID6.4 OD12 x1.6mm',base_thickness_mm=3,nominal_engagement_mm=8.4,screw_tip_z_mm=112.6,required_actual_engagement_mm=[8,9],load_path='Baseline clamps through the3mm PETG base and7mm deck; no metal bypass or rated clamp torque is claimed.'),
                  jaws=dict(retainers='4 x M3x8 ISO7380 button screws,4 x OD7 ID3.2 x0.5 washers,4 x M3 AF5.5x2.4 plain nuts',adjusters='2 x M4x25 ISO4762 cap screws and2 x M4 DIN985 AF7x5 nyloc nuts',pads='4 x50x14x2mm EVA, attach to fixture only'),
                  restraint=dict(ties='2 x4.8x300mm nylon cable ties, thickness<=1.2mm, head envelope<=12x8x6mm; trim tails and replace ties for blank removal',base_slots_xy_mm=[[x,y] for x in [-32,32] for y in [-40,40]],route='Each same-side pair links underbase through a2mm-deep groove, up both sides, and over its keeper rail atX+/-25. Keep the42mm centre opening free.',bottom_pad='50x50x2mm EVA',keeper_pad='50mm outside /42mm inside square ring x1mm EVA'),
                  limits=['Foam blank is an invented sample envelope, not a selected workpiece. No stone/wood/metal workholding is claimed.','Actual clamp torque, pad compression, dimensional fit, foam crushing/marking and restraint strength require coupon/bench tests before cutting.','Current folded arm pose only; no articulated spindle/tool path or cutting capability is certified.','Geometry-only installed/sweep proof; print and physical holding tests remain pending.'],clearance_checks=checks,internal_check=dict(unexpected_intersections=0,unchecked=0,excluded_pairs=tie_pairs))
    manifest['editable_assembly']=dict(file=str((OUT/'foam-fixture-prototype.sc').relative_to(ROOT)),sha256=sha(OUT/'foam-fixture-prototype.sc'))
    manifest['instructions']=['Baseline is a provisional50x50x40mm low-force foam blank only. Keep lower17mm and sacrificial outer border unmachined.', 'Fit all captured nuts and route two 4.8 mm ties through the base slots and underside grooves before mounting. Seat the base on the clean dry platter. Verify M6 washer thickness,3mm base and8-9mm actual blind engagement. No screw may bottom.', 'Bond EVA pads to the fixture only. Fit bottom pad and blank into the padded fixed corner, advance both jaws gently, then lock the M3 retainers without crushing foam.', 'Fit the keeper pad and open keeper. Wrap the two prerouted ties around the outside edges and over the keeper rails. Tighten and trim the tails. The ties provide independent upward restraint.', 'For unloading, cut the ties and lift the keeper 25 mm. Loosen the jaw retainers, back off both adjusters by 2 mm and lift the foam 25 mm. Lift the base to route fresh ties for the next blank.', 'Clamp force, torque, thread stack, pad compression, restraint strength, foam marking and actual tool/harness clearance require physical acceptance.']
    write(OUT/'foam-fixture-manifest.json',manifest);print(json.dumps(dict(prints=[p['file'] for p in prints],checks=len(checks),main_native_unchanged=True),indent=2))


if __name__=='__main__':main()
