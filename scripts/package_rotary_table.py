#!/usr/bin/env python3
"""Package the current prototype exports, review documents and reproducible source."""
import hashlib,json
from os.path import relpath
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
ROOT=Path(__file__).resolve().parents[1]
REPOSITORY_DOCUMENTS='https://github.com/carlosgj94/michelaingelo/blob/main'
BOM=Path('docs/rotary-table-bom.md')
ARM_REFERENCE=Path('references/so-arm100/README.md')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=ROOT/'exports/rotary-table';report=json.loads((ROOT/'cad/validation-results.json').read_text());manifest=json.loads((out/'print-manifest.json').read_text())
 revision=json.loads((ROOT/'cad/parts.json').read_text())['revision']
 assert report['revision']==manifest['revision']==revision and sha(ROOT/'michelaingelo.sc')==report['native_sha256']
 for p in manifest['parts']+[manifest['coupon']]:assert sha(ROOT/p['file'])==p['sha256']
 for name,digest in report['evidence_sha256'].items():assert sha(ROOT/name)==digest,name
 files=[ROOT/'michelaingelo.sc',ROOT/'README.md']
 files+=list((ROOT/'cad').glob('*.json'))+list((ROOT/'cad').glob('*.csv'))+list((ROOT/'scripts').glob('*.py'))
 files+=list((ROOT/'docs').glob('rotary-table-*'))+[ROOT/'docs/specs/rotary-table.md']
 files+=[p for p in (ROOT/'docs/audit-evidence').rglob('*') if p.is_file() and p.suffix in ('.json','.py','.png')]
 files+=[ROOT/'docs/archive/rotary-table-spec-rev3.md',ROOT/'docs/archive/rotary-table-validation-rev3.md']
 files+=[p for p in out.rglob('*') if p.is_file() and p.suffix!='.zip']
 linked_documents=[BOM,ARM_REFERENCE]
 files=sorted(set(files)-{ROOT/p for p in linked_documents})
 archive=out/'rt01-print-package.zip'
 with ZipFile(archive,'w',compression=ZIP_DEFLATED,compresslevel=9) as z:
  for p in files:
   member=p.relative_to(ROOT).as_posix()
   if p.suffix=='.md':
    document=p.read_text(encoding='utf-8')
    packaged_document=document
    for linked in linked_documents:
     relative_link=Path(relpath(ROOT/linked,p.parent)).as_posix()
     url=f'{REPOSITORY_DOCUMENTS}/{linked.as_posix()}'
     packaged_document=packaged_document.replace(f']({relative_link})',f']({url})')
    if packaged_document!=document:
     z.writestr(member,packaged_document)
     continue
   z.write(p,member)
  z.writestr('README-FIRST.txt',(
   f'RT-01 revision {revision} foam prototype\n\n'
   f'Open README.md and the revision {revision} response in docs/rotary-table-design-audit-2026-11-18.md.\n'
   '25 oriented assembly STLs, a fit coupon and one drain catch STL to print four times. Use the metal STEP files with the machining specification and supplier drawings.\n'
   'The native assembly, generators and verification evidence are included. The repository holds the original arm source and historical native files.\n'
   'The current bill of materials and SO100 arm reference are in the repository.\n'
   f'{REPOSITORY_DOCUMENTS}/{BOM.as_posix()}\n'
   f'{REPOSITORY_DOCUMENTS}/{ARM_REFERENCE.as_posix()}\n'
   'Physical fit, load, thermal, ingress and stopping acceptance remain pending.\n'
  ))
 with ZipFile(archive) as z:
  assert z.testzip() is None
  assert len([n for n in z.namelist() if n.startswith('exports/rotary-table/stl/') and n.endswith('.stl')])==25
  for p in manifest['parts']+[manifest['coupon']]:assert hashlib.sha256(z.read(p['file'])).hexdigest()==p['sha256']
  assert hashlib.sha256(z.read('michelaingelo.sc')).hexdigest()==report['native_sha256']
 print(json.dumps(dict(file=str(archive.relative_to(ROOT)),entries=len(files)+1,bytes=archive.stat().st_size,sha256=sha(archive))))
if __name__=='__main__':main()
