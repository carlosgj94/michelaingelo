#!/usr/bin/env python3
"""Rebuild RT-01 around the existing arm. Always write a separate review candidate."""
import argparse,json,subprocess,tempfile
from pathlib import Path
from shutil import copyfile
from zipfile import ZipFile
ROOT=Path(__file__).resolve().parents[1]
CLI='/Applications/SolidCraft.app/Contents/MacOS/solidcraft-cli'

BODY_GROUPS = {
    'print': 'To Be Printed',
    'buy': 'To Be Bought',
    'fabricate': 'To Be Fabricated',
    'reservation': 'Space Reservations',
}
ARM_GROUP = 'Existing Arm Reference'

def run(args):
 p=subprocess.run([CLI,*map(str,args)],cwd=ROOT,text=True,capture_output=True)
 if p.returncode:raise RuntimeError(p.stderr or p.stdout)
 return p.stdout

def label_assembly(source, destination, scratch):
    """Group bodies in the browser without changing their names or components."""
    parts = json.loads((ROOT/'cad/parts.json').read_text())['parts']
    labels = {part['name']: BODY_GROUPS[part['sourcing']] for part in parts}

    inspect = scratch/'list-bodies.json'
    inspect.write_text(json.dumps({'commands': [
        {'command': 'component.list', 'params': {'compact': True, 'bodies': True}},
    ]}))
    components = json.loads(run(['run', inspect, '--in', source, '--results', '--quiet']))[0]['components']
    by_id = {component['id']: component for component in components}

    def is_arm(component):
        while component['parent'] is not None:
            if component['name'].startswith('SO100 follower arm - '):
                return True
            component = by_id[component['parent']]
        return False

    groups = {}
    matched = set()
    for component in components:
        arm = is_arm(component)
        for name in component['bodies']:
            if arm:
                label = ARM_GROUP
            else:
                if name not in labels:
                    raise ValueError(f'Body missing from the parts list: {name}')
                label = labels[name]
                matched.add(name)
            groups.setdefault((component['id'], label), []).append(name)
    if matched != labels.keys():
        raise ValueError(f'Parts missing from assembly: {sorted(labels.keys() - matched)}')

    with ZipFile(source) as archive:
        previous_groups = json.loads(archive.read('document.json')).get('browser_groups', [])
    label_names = {*BODY_GROUPS.values(), ARM_GROUP}
    previous_labels = [
        group for group in previous_groups
        if group['folder'] == 'bodies' and group['name'] in label_names
    ]
    previous_members = {(group['component'], group['name']): group['items'] for group in previous_labels}
    if len(previous_labels) == len(groups) and previous_members == groups:
        copyfile(source, destination)
        return
    commands = [
        {'command': 'browser.ungroup', 'params': {'group': group['id']}}
        for group in previous_labels
    ]
    commands.extend(
        {'command': 'browser.group', 'params': {
            'folder': 'bodies', 'component': component_id, 'name': label, 'items': names,
        }}
        for (component_id, label), names in groups.items()
    )
    script = scratch/'label-bodies.json'
    script.write_text(json.dumps({'commands': commands}))
    run(['run', script, '--in', source, '--save', destination, '--quiet'])

    with ZipFile(destination) as archive:
        saved_groups = json.loads(archive.read('document.json'))['browser_groups']
    actual = {
        (group['component'], group['name']): group['items']
        for group in saved_groups if group['folder'] == 'bodies' and group['name'] in label_names
    }
    if actual != groups:
        raise RuntimeError('Saved sourcing groups do not match the parts list.')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--in',dest='source',type=Path,default=ROOT/'michelaingelo.sc');ap.add_argument('--out',type=Path,required=True)
 ap.add_argument('--labels-only', action='store_true', help='Update browser sourcing groups without rebuilding the assembly.')
 args=ap.parse_args()
 source=args.source.resolve();out=args.out.resolve()
 if source==out:raise ValueError('Write a separate candidate, verify it, then replace the reviewed native file.')
 with tempfile.TemporaryDirectory(prefix='rt01-rebuild-') as td:
  td=Path(td);inspect=td/'inspect.json'
  if args.labels_only:
   label_assembly(source,out,td)
   print(out)
   return
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
  revision=json.loads((ROOT/'cad/parts.json').read_text())['revision']
  C.append(dict(command='document.metadata.set',params=dict(key='com.michelaingelo.rt01',value=dict(revision=revision,status='Prototype; see audit response and remaining release gates'))))
  for folder in ['sketches','construction','origin','joints']:
   C.append(dict(command='browser.visibility',params=dict(folder=folder,visible=False)))
  C.extend([dict(command='inspect.section',params=dict(clear=True)),dict(command='inspect.analysis',params=dict(off=True)),dict(command='select.clear',params={}),dict(command='view.apply',params=dict(view='RT01 and arm reference'))])
  script=td/'rebuild.json';script.write_text(json.dumps(dict(commands=C)))
  candidate=td/'rebuilt.sc'
  run(['run',script,'--in',source,'--save',candidate,'--json-out',out.with_suffix('.measure.json'),'--quiet'])
  label_assembly(candidate,out,td)
 print(out)
if __name__=='__main__':main()
