#!/usr/bin/env python3
"""Rebuild RT-01 around the existing arm. Always write a separate review candidate."""
import argparse,json,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CLI='/Applications/SolidCraft.app/Contents/MacOS/solidcraft-cli'
def run(args):
 p=subprocess.run([CLI,*map(str,args)],cwd=ROOT,text=True,capture_output=True)
 if p.returncode:raise RuntimeError(p.stderr or p.stdout)
 return p.stdout
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--in',dest='source',type=Path,default=ROOT/'michelaingelo.sc');ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
 source=args.source.resolve();out=args.out.resolve()
 if source==out:raise ValueError('Write a separate candidate, verify it, then replace the reviewed native file.')
 with tempfile.TemporaryDirectory(prefix='rt01-rebuild-') as td:
  td=Path(td);inspect=td/'inspect.json'
  inspect.write_text(json.dumps(dict(commands=[dict(command='component.list',params=dict(compact=True)),dict(command='parameters.list',params=dict(filter='user')),dict(command='joint.list',params={})])))
  state=json.loads(run(['run',inspect,'--in',source,'--results','--quiet']))
  C=[dict(command='component.activate',params=dict(component='root'))]
  names={j['name'] for j in state[2]['joints']}
  for n in ['SO100 fixed bridge mount','RT01 vertical C axis']:
   if n in names:C.append(dict(command='joint.delete',params=dict(joint=n)))
  for c in state[0]['components']:
   if c['name'].startswith('RT01 -'):C.append(dict(command='component.delete',params=dict(component=c['name'])))
  for p in state[1]['parameters']:
   if p['name'].startswith('rt_'):C.append(dict(command='parameters.delete',params=dict(name=p['name'])))
  arm=json.loads((ROOT/'cad/arm-mount-reference.json').read_text())
  C.append(dict(command='occurrence.move',params=dict(occurrence='SO100 follower arm - mounted reference:1',to_matrix=arm['new_root_transform_row_major_3x4'],move_grounded=True)))
  C+=json.loads((ROOT/'cad/rotary-table-build.json').read_text())['commands']
  C.append(dict(command='joint.as_built',params=dict(type='rigid',a='RT01 - arm support bridge:1',b='SO100 follower arm - mounted reference:1',at=dict(occurrence='RT01 - arm support bridge:1',point=[0,-224,152],z=[0,0,1]),name='SO100 fixed bridge mount')))
  C.append(dict(command='document.metadata.set',params=dict(key='com.michelaingelo.rt01',value=dict(revision=4,status='Prototype; see audit response and remaining release gates'))))
  for folder in ['sketches','construction','origin','joints']:
   C.append(dict(command='browser.visibility',params=dict(folder=folder,visible=False)))
  C.extend([dict(command='inspect.section',params=dict(clear=True)),dict(command='inspect.analysis',params=dict(off=True)),dict(command='select.clear',params={}),dict(command='view.apply',params=dict(view='RT01 and arm reference'))])
  script=td/'rebuild.json';script.write_text(json.dumps(dict(commands=C)))
  run(['run',script,'--in',source,'--save',out,'--json-out',out.with_suffix('.measure.json'),'--quiet'])
 print(out)
if __name__=='__main__':main()
