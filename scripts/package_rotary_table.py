#!/usr/bin/env python3
"""Package the current prototype exports, review documents and reproducible source."""
import hashlib,json
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=ROOT/'exports/rotary-table';report=json.loads((ROOT/'cad/validation-results.json').read_text());manifest=json.loads((out/'print-manifest.json').read_text())
 assert report['revision']==manifest['revision']==4 and sha(ROOT/'michelaingelo.sc')==report['native_sha256']
 for p in manifest['parts']+[manifest['coupon']]:assert sha(ROOT/p['file'])==p['sha256']
 for name,digest in report['evidence_sha256'].items():assert sha(ROOT/name)==digest,name
 files=[ROOT/'michelaingelo.sc',ROOT/'README.md']
 files+=list((ROOT/'cad').glob('*.json'))+list((ROOT/'cad').glob('*.csv'))+list((ROOT/'scripts').glob('*.py'))
 files+=list((ROOT/'docs').glob('rotary-table-*'))+[ROOT/'docs/specs/rotary-table.md']
 files+=list((ROOT/'docs/audit-evidence/2026-11-17-rt01').rglob('*.json'))
 files+=[ROOT/'docs/archive/rotary-table-spec-rev3.md',ROOT/'docs/archive/rotary-table-validation-rev3.md']
 files+=[p for p in out.rglob('*') if p.is_file() and p.suffix!='.zip']
 archive=out/'rt01-print-package.zip'
 with ZipFile(archive,'w',compression=ZIP_DEFLATED,compresslevel=9) as z:
  for p in sorted(set(files)):z.write(p,p.relative_to(ROOT))
  z.writestr('README-FIRST.txt','RT-01 revision 4 prototype\n\nOpen README.md and docs/rotary-table-audit-response-2026-11-17.md first.\n25 oriented assembly STLs plus a fit coupon. Metal STEP files require the machining specification and supplier/fabricator review.\nNative SolidCraft model, generators, current checks and review evidence are included. Historical native files and the original arm source are in the repository, not duplicated in this package.\nNo slicing, physical printing, load/accuracy or ingress qualification is claimed. See remaining release gates before ordering or operation.\n')
 with ZipFile(archive) as z:
  assert z.testzip() is None
  assert len([n for n in z.namelist() if n.startswith('exports/rotary-table/stl/') and n.endswith('.stl')])==25
  for p in manifest['parts']+[manifest['coupon']]:assert hashlib.sha256(z.read(p['file'])).hexdigest()==p['sha256']
  assert hashlib.sha256(z.read('michelaingelo.sc')).hexdigest()==report['native_sha256']
 print(json.dumps(dict(file=str(archive.relative_to(ROOT)),entries=len(files)+1,bytes=archive.stat().st_size,sha256=sha(archive))))
if __name__=='__main__':main()
