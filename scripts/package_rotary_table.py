#!/usr/bin/env python3
"""Package the current prototype exports, review documents and reproducible source."""
import hashlib,json
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
ROOT=Path(__file__).resolve().parents[1]
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
 archive=out/'rt01-print-package.zip'
 with ZipFile(archive,'w',compression=ZIP_DEFLATED,compresslevel=9) as z:
  for p in sorted(set(files)):z.write(p,p.relative_to(ROOT))
  z.writestr('README-FIRST.txt',f'RT-01 revision {revision} foam prototype\n\nOpen README.md and the revision {revision} response in docs/rotary-table-design-audit-2026-11-18.md.\n25 oriented assembly STLs plus a fit coupon. Use the metal STEP files with the machining specification and supplier drawings.\nThe native assembly, generators, BOM and verification evidence are included. The repository holds the original arm source and historical native files.\nPhysical fit, load, thermal, ingress and stopping acceptance remain pending.\n')
 with ZipFile(archive) as z:
  assert z.testzip() is None
  assert len([n for n in z.namelist() if n.startswith('exports/rotary-table/stl/') and n.endswith('.stl')])==25
  for p in manifest['parts']+[manifest['coupon']]:assert hashlib.sha256(z.read(p['file'])).hexdigest()==p['sha256']
  assert hashlib.sha256(z.read('michelaingelo.sc')).hexdigest()==report['native_sha256']
 print(json.dumps(dict(file=str(archive.relative_to(ROOT)),entries=len(files)+1,bytes=archive.stat().st_size,sha256=sha(archive))))
if __name__=='__main__':main()
