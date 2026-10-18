"""Check edition structure and internal navigation. Does not validate science.

Requires PyMuPDF. Run after build_edition.py. For a release, also inspect renders.
"""
from pathlib import Path
import hashlib, json, re, posixpath, zipfile
import xml.etree.ElementTree as ET
from urllib.parse import urlsplit, unquote
import fitz

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'output'
errors = []
checks = {}
manifest = json.loads((ROOT/'EDITION_MANIFEST.json').read_text())
for name, metadata in manifest['files'].items():
    if hashlib.sha256((OUT/name).read_bytes()).hexdigest() != metadata['sha256']:
        errors.append(f'Manifest hash mismatch: {name}')

source = (ROOT/'manuscript/Creatures_of_Context.md').read_text(encoding='utf-8')
assembled = (OUT/'Creatures_of_Context.md').read_text(encoding='utf-8')
if source != assembled:
    errors.append('Published Markdown differs from canonical manuscript')
body, notes = source.split('\n# Notes\n', 1)
refs = list(dict.fromkeys(re.findall(r'\[\^([^\]]+)\]', body)))
all_notes = re.findall(r'^\[\^([^\]]+)\]:', notes, re.M)
if refs != all_notes:
    errors.append('Note definitions do not match first-reference order')
chapter_numbers = [int(n) for n in re.findall(r'^## Chapter (\d+):',body,re.M)]
if chapter_numbers != list(range(1,manifest['chapters']+1)):
    errors.append('Chapter order or count differs from manifest')
checks['chapters'] = len(chapter_numbers)
checks['unique_notes'] = len(set(all_notes))
if len(all_notes)!=len(set(all_notes)):
    errors.append('Duplicate footnote identifiers')
if hashlib.sha256(source.encode()).hexdigest()!=manifest['source']['sha256']:
    errors.append('Canonical source hash differs from manifest')

doc = fitz.open(OUT/'Creatures_of_Context.pdf')
checks['pdf_pages'] = len(doc)
checks['pdf_outline_entries'] = len(doc.get_toc())
checks['pdf_links'] = sum(len(p.get_links()) for p in doc)
for number,page in enumerate(doc,1):
    if not page.get_text().strip():
        errors.append(f'Blank PDF page: {number}')
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            for span in line['spans']:
                x0,y0,x1,y1=span['bbox']
                if min(x0,y0)<-0.5 or x1>page.rect.width+0.5 or y1>page.rect.height+0.5:
                    errors.append(f'Text outside PDF page: {number}: {span["text"][:35]}')
    for link in page.get_links():
        if link.get('kind')==fitz.LINK_GOTO and not 0<=link.get('page',-1)<len(doc):
            errors.append(f'Invalid internal PDF destination on page {number}')
expected_outline = manifest['chapters'] + 2 + 3 + 1
if len(doc.get_toc()) != expected_outline:
    errors.append(f'Expected {expected_outline} PDF outline entries')
if doc.metadata.get('author') != manifest['author']:
    errors.append('PDF author metadata differs from manifest')
if '[^' in ''.join(p.get_text() for p in doc):
    errors.append('Unrendered Markdown footnote token in PDF')

with zipfile.ZipFile(OUT/'Creatures_of_Context.epub') as z:
    if z.read('mimetype')!=b'application/epub+zip':
        errors.append('Invalid EPUB mimetype')
    names=set(z.namelist())
    parsed={}
    for name in names:
        if name.endswith(('.xhtml','.html','.opf','.ncx','.xml')):
            parsed[name]=ET.fromstring(z.read(name))
    ids={n:{e.attrib['id'] for e in root.iter() if 'id' in e.attrib} for n,root in parsed.items()}
    linkcount=0
    for name,root in parsed.items():
        for el in root.iter():
            for attr in ('href','src'):
                ref=el.attrib.get(attr)
                if not ref: continue
                u=urlsplit(ref)
                if u.scheme or u.netloc: continue
                target=posixpath.normpath(posixpath.join(posixpath.dirname(name),unquote(u.path))) if u.path else name
                if target not in names:
                    errors.append(f'Missing EPUB resource: {name}: {ref}')
                if u.fragment and unquote(u.fragment) not in ids.get(target,set()):
                    errors.append(f'Missing EPUB anchor: {name}: {ref}')
                linkcount+=1
    checks['epub_xml_documents']=len(parsed)
    checks['epub_internal_references']=linkcount

checks['errors']=errors
checks['status']='passed' if not errors else 'failed'
checks['scope']='Source/output consistency, footnotes, XML and internal navigation, PDF page bounds. External URLs, scientific accuracy and visual quality require separate review.'
(ROOT/'records/TECHNICAL_QA.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(checks,indent=2))
raise SystemExit(bool(errors))
