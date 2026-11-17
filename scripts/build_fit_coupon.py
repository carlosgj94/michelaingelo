"""Generate the RT-01 PETG fit coupon; do not infer printer accuracy from CAD."""
import contextlib, io, json
from pathlib import Path
with contextlib.redirect_stdout(io.StringIO()):
    import build_rotary_table as rt
rt.commands=[];rt.parts=[];rt.stages=[];rt.serial=0
rt.group('RT01 fit coupon')
rt.cmd('parameters.add',name='coupon_zero',expression='0 mm',comment='Keeps nut-pocket coordinates fixed; leave at zero.')
b='RT01 PETG fit coupon'
rt.box(b,[140,70,8],[0,0,0])
# A clipped lower-left corner establishes orientation when the print is turned over.
rt.box(b,[4,4,10],[-1,-1,-1],'cut','orientation notch')
for i,(x,d) in enumerate([(25,35.2),(70,35.3),(115,35.4)],1):
    rt.hole(b,d,[x,25,4],5,label=f'bearing seat plus {d-35:.1f}')
    rt.hole(b,15.4,[x,25,-1],6,label='seat bottom access')
    for j in range(i):rt.hole(b,1.8,[x+(j-(i-1)/2)*3,4,-1],10,label='seat identity dot')
for x,d in [(35,3.4),(60,4.5),(85,5.5),(110,6.6)]:
    rt.hole(b,d,[x,48,-1],10,label=f'Metric clearance {d}')
for x,af in [(15,8.2),(40,8.4),(65,8.6)]:
    rt.hexcut(b,f'{af} mm+coupon_zero',4.5,[x,58,3.6]);rt.hole(b,5.5,[x,58,-1],6)
for x,d in [(90,4.0),(110,4.2),(130,4.4)]:rt.hole(b,d,[x,58,2],7,label=f'insert trial {d}')
rt.cmd('appearance.assign',bodies=[b],color='#DAE4E6')
rt.cmd('view.apply',view='iso')
root=Path(__file__).resolve().parents[1]
(root/'cad/fit-coupon-build.json').write_text(json.dumps({'commands':rt.commands},indent=2)+'\n')
print(f'Generated fit coupon: {len(rt.commands)} commands')
