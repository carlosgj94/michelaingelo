#!/usr/bin/env python3
"""Check retained CAD and export evidence before writing the validation record."""
import argparse, hashlib, json, math, subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/'docs/audit-evidence/2026-11-18-rt01/revision5'
SERVICE_PROBE=ROOT/'cad/support-access-checks.json'
SERVICE_RESULTS=E.parent/'service-follow-up/service.results.json'
DRAIN_MANIFEST=ROOT/'exports/rotary-table/drain-catch/drain-catch-manifest.json'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def native_geometry_sha256(path):
    """Fingerprint the full native archive with only display appearances excluded."""
    entry_hashes = {}
    with ZipFile(path) as archive:
        document_bytes = archive.read('document.json')
        document = json.loads(document_bytes)
        document.pop('appearances', None)
        structural_document = json.dumps(document, sort_keys=True).encode()
        for name in archive.namelist():
            if name == 'document.json':
                contents = structural_document
            elif name == 'cache/model.json':
                cache = json.loads(archive.read(name))
                assert cache['document'] == hashlib.sha256(document_bytes).hexdigest()
                cache['document'] = hashlib.sha256(structural_document).hexdigest()
                contents = json.dumps(cache, sort_keys=True).encode()
            else:
                contents = archive.read(name)
            entry_hashes[name] = hashlib.sha256(contents).hexdigest()
    return hashlib.sha256(json.dumps(entry_hashes, sort_keys=True).encode()).hexdigest()

def bodies(p):return {b['name']:b for b in read(p)['bodies']}

def replay_service(native, geometry_sha, coverage):
    """Record the current production tool probes without saving their test bodies."""
    with TemporaryDirectory(prefix='rt01-service-') as directory:
        output = Path(directory)/'results.json'
        subprocess.run(['solidcraft-cli', 'run', str(SERVICE_PROBE), '--in', str(native),
                        '--results', '--quiet', '--json-out', str(output)], check=True)
        results = read(output)
    commands = read(SERVICE_PROBE)['commands']
    assert len(commands) == len(results)
    clearance = []
    seating = []
    for command, result in zip(commands, results):
        if command['command'] == 'inspect.clearance':
            clearance.append({key: value for key, value in result.items() if key != 'ms'})
        elif command['command'] == 'inspect.interference':
            seating.append({key: value for key, value in result.items() if key != 'ms'})
    clearance_names = coverage['service_checks']
    seating_names = [row['name'] for row in coverage['seating_checks']]
    assert len(clearance_names) == len(clearance) and len(seating_names) == len(seating)
    return dict(solidcraft=subprocess.check_output(['solidcraft-cli','--version'],text=True).strip(),
                native_sha256=sha(native), native_geometry_sha256=geometry_sha,
                probe_sha256=sha(SERVICE_PROBE),
                clearances=dict(zip(clearance_names, clearance)), seating=dict(zip(seating_names, seating)))

def compare(a,b,names,z=0):
 v=max(abs((a[n].get('volume_mm3') or 0)-(b[n].get('volume_mm3') or 0)) for n in names)
 d=max(abs(a[n]['bbox'][k][i]-b[n]['bbox'][k][i]-(z if i==2 else 0)) for n in names for k in ['min','max'] for i in range(3))
 assert v<.01 and d<1e-6,(v,d)
 return dict(bodies=len(names),max_volume_delta_mm3=v,max_bound_error_mm=d,expected_z_translation_mm=z)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--native',type=Path,default=ROOT/'michelaingelo.sc')
 ap.add_argument('--replay-service',action='store_true',help='Run and record the current installed-service probes before validating the package.')
 args=ap.parse_args()
 part_register=read(ROOT/'cad/parts.json');names=[p['name'] for p in part_register['parts']]
 native=bodies(E/'native.measure.json');fresh=bodies(E/'fresh.measure.json');step=bodies(E/'step.measure.json')
 assert len(names)==81 and set(names)==set(fresh)==set(step)
 assert all(native[n]['closed'] for n in names)
 arm=read(ROOT/'cad/arm-mount-reference.json')['collision_body_names'];baseline=bodies(E/'baseline.measure.json')
 assert set(native)==set(names+arm)
 health,joints,params=read(E/'health.results.json')
 assert not any(f.get('error') for f in health['timeline'])
 assert all(s['dof']==0 for s in health['sketches'])
 assert not any(joints.get(key) for key in ['conflicts','floating','errors'])
 axis=next(j for j in joints['joints'] if j['name']=='RT01 vertical C axis');assert axis['values'][0]['value']==0
 assert any(j['name']=='SO100 fixed bridge mount' for j in joints['joints'])
 motion=[x for x in read(E/'rotation-hardware.results.json') if 'unchecked' in x]
 assert len(motion)==28
 assert all(not x['interferences'] and not x['unchecked'] and not x['budget_exceeded'] and not x['pairs_not_checked'] and not x['truncated'] for x in motion)
 coverage=read(ROOT/'cad/hardware-check-coverage.json')
 geometry_sha=native_geometry_sha256(args.native)
 service=replay_service(args.native,geometry_sha,coverage) if args.replay_service else read(SERVICE_RESULTS)
 assert service['native_geometry_sha256']==geometry_sha and service['probe_sha256']==sha(SERVICE_PROBE)
 clearances=service['clearances']
 assert list(clearances)==coverage['service_checks']
 for label,result in clearances.items():
  issues={key: result[key] for key in ['overlaps','unchecked','truncated','pairs_not_checked','budget_exceeded'] if result.get(key)}
  assert not issues,(label,issues)
 assert list(service['seating'])==[row['name'] for row in coverage['seating_checks']]
 for row in coverage['seating_checks']:
  result=service['seating'][row['name']]
  assert not any(result.get(k) for k in ['unchecked','truncated','budget_exceeded']),row['name']
  assert len(result['interferences'])==len(row['gauges']),row['name']
  for gauge in row['gauges']:
   hits=[pair for pair in result['interferences'] if gauge in [pair['a'],pair['b']]]
   assert len(hits)==1 and abs(hits[0]['volume_mm3']-row['expected_overlap_mm3_per_gauge'])<.001,(gauge,hits)
 def gap(label,body,against):
  return next(x['distance_mm'] for x in clearances[label]['nearest'][body] if x['body']==against)
 driver_path='driver complete withdrawal sweep';driver=f'TEST {driver_path}'
 rim_gap=gap(driver_path,driver,'P50 electronics service box')
 plate_gap=gap(driver_path,driver,'M50 SO100 arm mounting plate')
 assert abs(rim_gap-2.5)<.001 and abs(plate_gap-2.5)<.001
 hood_washer_gap=min(v['distance_mm'] for v in clearances['hood posts clear motor anchor washers at X+49']['nearest']['P46 motor service hood'])
 assert hood_washer_gap>=.899
 fit=read(E/'fit-parameters.results.json');assert len(fit[0]['changed'])==12 and not fit[0]['errors']
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
 catch=read(DRAIN_MANIFEST)
 catch_print=catch['print']
 assert catch['quantity']==4 and catch_print['closed_edges'] and catch_print['consistent_winding']
 assert 0<catch_print['mesh_volume_mm3'] and max(catch_print['print_bbox_mm'])<=168.001
 assert max(catch_print['footprint_with_5mm_brim_mm'])<=180.001
 for item in (catch_print,catch['editable_native']):assert sha(ROOT/item['file'])==item['sha256']
 register=read(ROOT/'cad/fasteners.json')
 assert coverage['groups']=={r['id']:r['quantity'] for r in register['rows']}
 revision=part_register['revision'];assert revision==register['revision']==manifest['revision']==coverage['revision']==5
 provenance=read(E/'input-provenance.json')
 native_sha=sha(args.native)
 checked_native_sha=provenance['candidate_native_sha256']
 if native_sha!=checked_native_sha:
  assert geometry_sha==provenance['candidate_native_geometry_sha256'], 'Native changes exceed display appearances.'
 report=dict(design='RT-01',revision=revision,date='2026-11-18',status='CAD corrections verified for the foam prototype. Fabrication release and physical tests pending.',
  native_sha256=native_sha,geometry_validated_native_sha256=checked_native_sha,baseline_sha256=provenance['baseline_native_sha256'],
  health=dict(new_closed_bodies=len(names),total_world_bodies=len(native),sketches_zero_dof=len(health['sketches']),timeline_entries=len(health['timeline']),failed_features=0,arm_import_warnings=[f['warning'] for f in health['timeline'] if f.get('warning')]),
  source_comparison=compare(native,fresh,names),step_round_trip=compare(native,step,names),arm_preservation=compare(native,baseline,arm),
  hardware=dict(groups=len(coverage['groups']),screws=sum(coverage['groups'].values()),specified_lengths=sum(r['quantity'] for r in register['rows'] if r['length_mm'] and r['id']!='F24'),arm_screws_to_fit=4,bench_bolts=sum(r['quantity'] for r in register['rows'] if not r['length_mm']),fixture_tip_probes=4,rotation_angles_deg=coverage['angles_deg'],cartridge_offsets_mm=[3,-3],unexpected_intersections=0,unchecked_pairs=0,budget_failures=0,exclusions='cad/hardware-check-coverage.json'),
  service=dict(clearance_checks=len(clearances),supported_seats=sum(len(row['gauges']) for row in coverage['seating_checks']),unexpected_intersections=0,unchecked_pairs=0,raised_driver_rim_clearance_mm=rim_gap,raised_driver_plate_clearance_mm=plate_gap,critical_hood_washer_clearance_mm=hood_washer_gap),
  fit_parameter_trial=dict(changes=fit[0]['changed'],features_recomputed=fit[0]['recomputed'],changed_print_bodies=changed,failed_features=0,scope='One simultaneous enlargement trial of twelve printed fits. Physical print fit remains pending.'),
  prints=dict(assembly_stls=25,coupons=1,largest_dimension_mm=max(max(p['print_bbox_mm']) for p in manifest['parts']),largest_brim_footprint_mm=max(max(p['footprint_with_5mm_brim_mm']) for p in manifest['parts']),max_mesh_volume_error_percent=max(p['mesh_volume_error_percent'] for p in manifest['parts']),seam_strips=[dict(name=p['name'],bounds_mm=p['print_bbox_mm'],bed_contact_area_mm2=p['bed_contact_area_mm2']) for p in strips]),
  drain_catch=dict(quantity=catch['quantity'],file=catch_print['file'],print_bbox_mm=catch_print['print_bbox_mm'],capacities_ml=catch['capacities_ml'],manifest=str(DRAIN_MANIFEST.relative_to(ROOT))),
  analytic_nominal_bounds_mm=dict(anchor_washer_to_wall=150-math.hypot(88,108)-7.5,anchor_washer_to_motor_opening=108-7.5-97.5,carrier_end_gap_at_limit=1,blind_fixture_bottom_metal=2.5,target_to_column_heads=2.1,rib_to_wall=3.8,skirt_radial_gap=2,deck_upstand_gap=2),
  not_run=['Owned-foot seat and thread/preload qualification','Slicing, printing, fit, insert, seal and nut-trap retention tests','Loaded reversal, runout, stiffness, fatigue and stopping tests','Home signal, selected connectors/cables and electronics thermal tests','Articulated arm/tool/workpiece study and actual bench/weld qualification'],
  limits=['Geometry verifies the represented envelopes and nominal seats. Hardware supplier tolerances and actual clamp loads require physical acceptance.','The 17 November evidence and the 18 November revision 4 audit are historical. The new service test includes retained hardware and two exact swept boxes for the driver envelope.','Foam prototype scope. Rock work requires its own tooling, extraction and qualification.'])
 if args.replay_service:
  SERVICE_RESULTS.parent.mkdir(parents=True,exist_ok=True)
  SERVICE_RESULTS.write_text(json.dumps(service,indent=2)+'\n')
 files=[ROOT/'cad/rotary-table-build.json',ROOT/'cad/parts.json',ROOT/'cad/fasteners.json',ROOT/'cad/fastener-clearance-checks.json',SERVICE_PROBE,ROOT/'cad/fit-coupon-build.json',ROOT/'cad/hardware-check-coverage.json',ROOT/'cad/stand-backing-strip.json',ROOT/'exports/rotary-table/metal/m55-bench-backing-strip-make-two.step',ROOT/'exports/rotary-table/print-manifest.json',ROOT/'exports/rotary-table/rt01-assembly.step',DRAIN_MANIFEST,ROOT/catch_print['file'],ROOT/catch['editable_native']['file']]
 files+=[ROOT/'scripts/build_drain_catch.py',SERVICE_RESULTS.parent/'drain-catch-placement.png']
 files+=sorted(E.glob('*.json'))+sorted(SERVICE_RESULTS.parent.glob('*.json'))
 files=[p for p in files if p.name!='summary.json']
 report['evidence_sha256']={str(p.relative_to(ROOT)):sha(p) for p in files}
 (ROOT/'cad/validation-results.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:report[k] for k in ['health','source_comparison','step_round_trip','arm_preservation','prints']},indent=2))
if __name__=='__main__':main()
