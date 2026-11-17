#!/usr/bin/env python3
"""Check retained revision-4 evidence and write the compact report; does not run CAD.
Run only after refreshing the evidence inputs named in docs/rotary-table-validation.md.
"""
import argparse, hashlib, json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/'docs/audit-evidence/2026-11-17-rt01/revision4'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bodies(p):return {b['name']:b for b in read(p)['bodies']}
def compare(a,b,names,z=0):
 v=max(abs((a[n].get('volume_mm3') or 0)-(b[n].get('volume_mm3') or 0)) for n in names)
 d=max(abs(a[n]['bbox'][k][i]-b[n]['bbox'][k][i]-(z if i==2 else 0)) for n in names for k in ['min','max'] for i in range(3))
 assert v<.01 and d<1e-6,(v,d)
 return dict(bodies=len(names),max_volume_delta_mm3=v,max_bound_error_mm=d,expected_z_translation_mm=z)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--native',type=Path,default=ROOT/'michelaingelo.sc');args=ap.parse_args()
 parts=read(ROOT/'cad/parts.json')['parts'];names=[p['name'] for p in parts]
 native=bodies(E/'native.measure.json');fresh=bodies(E/'fresh.measure.json');step=bodies(E/'step.measure.json')
 assert len(names)==81 and set(names)==set(fresh)==set(step)
 assert all(native[n]['closed'] for n in names)
 arm=read(ROOT/'cad/arm-mount-reference.json')['collision_body_names'];baseline=bodies(E/'arm-baseline.measure.json')
 assert set(native)==set(names+arm)
 health,joints,params=read(E/'health.results.json')
 assert not any(f.get('error') for f in health['timeline'])
 assert all(s['dof']==0 for s in health['sketches'])
 assert not joints.get('conflicts') and not joints.get('floating')
 axis=next(j for j in joints['joints'] if j['name']=='RT01 vertical C axis');assert axis['values'][0]['value']==0
 assert any(j['name']=='SO100 fixed bridge mount' for j in joints['joints'])
 motion=[x for x in read(E/'rotation-hardware.results.json') if 'unchecked' in x]
 assert len(motion)==28
 assert all(not x['interferences'] and not x['unchecked'] and not x['budget_exceeded'] and not x['pairs_not_checked'] and not x['truncated'] for x in motion)
 service=[x for x in read(E/'service.results.json') if 'unchecked' in x]
 assert len(service)==13 and all(not x['overlaps'] and not x['unchecked'] for x in service)
 interfaces=read(E/'interfaces.results.json');gaps=[]
 for x in interfaces:
  assert not x['overlaps'] and not x['unchecked']
  for a,near in x['nearest'].items():
   for b in near:gaps.append(dict(a=a,b=b['body'],gap_mm=b['distance_mm']))
 fit=read(E/'fit-parameters.results.json');assert len(fit[0]['changed'])==11 and not fit[0]['errors']
 assert not any(f.get('error') for f in fit[1]['timeline'])
 fitb={b['name']:b for b in fit[1]['bodies']}
 changed=[n for n in names if abs(native[n]['volume_mm3']-fitb[n]['volume_mm3'])>1e-6]
 assert all(n in changed for n in ['P11 column sleeve','P24 NEMA17 motor bracket','P31 platter quadrant','P41 fixed housing quadrant','P45 seam backing strip 1','P50 electronics service box','P51 removable controller tray','P52 electronics lid'])
 manifest=read(ROOT/'exports/rotary-table/print-manifest.json');assert len(manifest['parts'])==25
 for p in manifest['parts']+[manifest['coupon']]:
  assert p['closed_edges'] and p['consistent_winding'] and p['mesh_volume_mm3']>0
  assert sha(ROOT/p['file'])==p['sha256']
  assert max(p['print_bbox_mm'])<=168.001 and max(p['footprint_with_5mm_brim_mm'])<=180.001
 strips=[p for p in manifest['parts'] if p['name'].startswith('P45')];assert len(strips)==4
 assert all(p['print_bbox_mm']==[24.,84.,8.] and p['bed_contact_area_mm2']>1950 for p in strips)
 register=read(ROOT/'cad/fasteners.json');coverage=read(ROOT/'cad/hardware-check-coverage.json')
 assert coverage['groups']=={r['id']:r['quantity'] for r in register['rows']}
 report=dict(design='RT-01',revision=4,date='2026-11-17',status='CAD corrections verified; prototype, not fabrication released',
  native_sha256=sha(args.native),baseline_sha256='fc5b4c1079a4e5d9955af6266879d54597708b663fdfc605825a25b65dd6eb23',
  health=dict(new_closed_bodies=len(names),total_world_bodies=len(native),sketches_zero_dof=len(health['sketches']),failed_features=0,unchanged_arm_warnings=[f['warning'] for f in health['timeline'] if f.get('warning')]),
  source_comparison=compare(native,fresh,names),step_round_trip=compare(native,step,names),arm_preservation=compare(native,baseline,arm,8),
  hardware=dict(groups=len(coverage['groups']),screws=sum(coverage['groups'].values()),fixed_screws=sum(r['quantity'] for r in register['rows'] if r['length_mm']),bench_bolts=sum(r['quantity'] for r in register['rows'] if not r['length_mm']),fixture_tip_probes=4,rotation_angles_deg=coverage['angles_deg'],cartridge_offsets_mm=[3,-3],unexpected_intersections=0,unchecked_pairs=0,budget_failures=0,exclusions='cad/hardware-check-coverage.json'),
  service=dict(poses=len(service),unexpected_intersections=0,unchecked_pairs=0,driver_rim_clearance_mm=2,driver_plate_clearance_mm=3),
  measured_interfaces=gaps,fit_parameter_trial=dict(changes=fit[0]['changed'],features_recomputed=fit[0]['recomputed'],changed_print_bodies=changed,failed_features=0,scope='One simultaneous enlargement trial, not a range/scaling or physical-fit qualification'),
  prints=dict(assembly_stls=25,coupons=1,largest_dimension_mm=max(max(p['print_bbox_mm']) for p in manifest['parts']),largest_brim_footprint_mm=max(max(p['footprint_with_5mm_brim_mm']) for p in manifest['parts']),max_mesh_volume_error_percent=max(p['mesh_volume_error_percent'] for p in manifest['parts']),seam_strips=[dict(name=p['name'],bounds_mm=p['print_bbox_mm'],bed_contact_area_mm2=p['bed_contact_area_mm2']) for p in strips]),
  analytic_nominal_bounds_mm=dict(anchor_washer_to_wall=150-math.hypot(88,108)-7.5,anchor_washer_to_motor_opening=108-7.5-97.5,carrier_end_gap_at_limit=1,blind_fixture_bottom_metal=2.5,target_to_column_heads=2.1,rib_to_wall=3.8,skirt_radial_gap=2,deck_upstand_gap=2),
  not_run=['Slicing, physical printing, fit/insert/seal tests','Loaded motion, reversal, runout, stiffness, fatigue, FEA or payload qualification','Actual home signal, complete cordset/cable routing and electronics thermal tests','Full articulated arm/tool/workpiece study','Final purchased-bearing/shaft/coupling/board/fixture/bench and weld qualification'],
  limits=['Nominal geometry; material density defaults are not a mass or structural model.','All currently registered screw groups are checked. Heat-set insert retention/press fits, unknown below-bench geometry and unselected component hardware require separate validation.','No certified IP rating or stone-carving capability.'])
 files=[ROOT/'cad/rotary-table-build.json',ROOT/'cad/parts.json',ROOT/'cad/fasteners.json',ROOT/'cad/fastener-clearance-checks.json',ROOT/'cad/support-access-checks.json',ROOT/'cad/fit-coupon-build.json',ROOT/'cad/hardware-check-coverage.json',ROOT/'exports/rotary-table/print-manifest.json',ROOT/'exports/rotary-table/rt01-assembly.step']+sorted(E.glob('*.json'))
 files=[p for p in files if p.name!='summary.json']
 report['evidence_sha256']={str(p.relative_to(ROOT)):sha(p) for p in files}
 (ROOT/'cad/validation-results.json').write_text(json.dumps(report,indent=2)+'\n')
 (E/'summary.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:report[k] for k in ['health','source_comparison','step_round_trip','arm_preservation','prints']},indent=2))
if __name__=='__main__':main()
