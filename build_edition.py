"""Build the PDF, EPUB and editable Markdown from the canonical manuscript.

Dependencies: Python 3, reportlab, pandoc, DejaVu Serif fonts.
Run from any directory: python3 build_edition.py
"""
from pathlib import Path
import re, html, json, subprocess, shutil, hashlib
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
    PageBreak, NextPageTemplate, KeepTogether,
)
from reportlab.platypus.tableofcontents import TableOfContents

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'output'
OUT.mkdir(exist_ok=True)
SOURCE = ROOT / 'manuscript' / 'Creatures_of_Context.md'
manuscript = SOURCE.read_text(encoding='utf-8')
front = re.match(r"^---\n(.*?)\n---\n", manuscript, re.S)
assert front, 'Missing edition metadata'
metadata = {}
for line in front[1].splitlines():
    key, value = line.split(':', 1)
    metadata[key] = json.loads(value.strip()) if value.strip().startswith('"') else value.strip()
TITLE, SUBTITLE = metadata['title'], metadata['subtitle']
AUTHOR, DATE = metadata['author'], metadata['date']
EDITION = metadata['edition']
body, note_text = manuscript[front.end():].split('\n# Notes\n', 1)
notes = {}
for match in re.finditer(r'^\[\^([^\]]+)\]:\s*(.*?)(?=^\[\^|\Z)', note_text, re.M | re.S):
    key, note = match.groups()
    assert key not in notes, f'Duplicate note: {key}'
    notes[key] = {'number': len(notes)+1, 'text': ' '.join(note.split())}

chapters, PARTS = [], {}
EDITION_NOTE = None
sections = list(re.finditer(r'^#{1,2} (Introduction:.*|Chapter \d+:.*|Conclusion:.*|Part [IVX]+:.*|About this edition)$', body, re.M))
pending_part = None
for i, section in enumerate(sections):
    heading = section[1]
    content = body[section.end():sections[i+1].start() if i+1<len(sections) else len(body)].strip()
    if heading == 'About this edition':
        EDITION_NOTE = content
        continue
    label, title = heading.split(': ', 1)
    if label.startswith('Part '):
        pending_part = (label.split()[1], title, content)
        continue
    n = int(label.split()[1]) if label.startswith('Chapter ') else None
    if pending_part:
        assert n is not None
        PARTS[n] = pending_part
        pending_part = None
    keys = list(dict.fromkeys(re.findall(r'\[\^([^\]]+)\]', content)))
    for key in keys:
        assert key in notes, f'Missing note: {key}'
    chapters.append({'label':label, 'title':title, 'body':content, 'number':n, 'notes':keys})
assert EDITION_NOTE and not pending_part
numbers = [c['number'] for c in chapters if c['number'] is not None]
assert numbers == list(range(1,len(numbers)+1)), 'Chapter order is not contiguous'
allrefs = [key for c in chapters for key in re.findall(r'\[\^([^\]]+)\]', c['body'])]
assert set(allrefs) == set(notes), 'Missing or unused note definitions'
assert list(dict.fromkeys(allrefs)) == list(notes), 'Notes must follow first-reference order'
(OUT/'Creatures_of_Context.md').write_text(manuscript, encoding='utf-8')

# PDF typography. Font embedding keeps all named researchers legible.
fontdir = Path('/usr/share/fonts/truetype/dejavu')
if not (fontdir/'DejaVuSerif-Italic.ttf').exists():
    import matplotlib
    fontdir = Path(matplotlib.get_data_path())/'fonts'/'ttf'
for name, file in [('Book','DejaVuSerif.ttf'),('BookItalic','DejaVuSerif-Italic.ttf'),('BookBold','DejaVuSerif-Bold.ttf'),('BookBoldItalic','DejaVuSerif-BoldItalic.ttf'),('Sans','DejaVuSans.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(fontdir/file)))
pdfmetrics.registerFontFamily('Book', normal='Book', bold='BookBold', italic='BookItalic', boldItalic='BookBoldItalic')
W, H = 468, 684
LEFT, RIGHT, TOP, BOTTOM = 53, 49, 58, 51
INK = HexColor('#202622')
ACCENT = HexColor('#36574F')
GRAY = HexColor('#626761')
styles = {
    'body': ParagraphStyle('body', fontName='Book', fontSize=10.5, leading=15, textColor=INK, alignment=TA_LEFT, spaceAfter=8, allowWidows=0, allowOrphans=0, splitLongWords=1),
    'section': ParagraphStyle('section', fontName='BookBold', fontSize=12.1, leading=16.5, textColor=INK, spaceBefore=17, spaceAfter=9, keepWithNext=True),
    'label': ParagraphStyle('label', fontName='Sans', fontSize=9, leading=13, textColor=ACCENT, spaceAfter=9, keepWithNext=True),
    'chapter': ParagraphStyle('chapter', fontName='Book', fontSize=26, leading=31, textColor=INK, spaceAfter=25, keepWithNext=True),
    'cover': ParagraphStyle('cover', fontName='Book', fontSize=38, leading=45, textColor=INK, spaceAfter=22),
    'subtitle': ParagraphStyle('subtitle', fontName='Book', fontSize=16, leading=23, textColor=INK),
    'small': ParagraphStyle('small', fontName='Book', fontSize=9, leading=13.5, textColor=GRAY, spaceAfter=10),
    'note': ParagraphStyle('note', fontName='Book', fontSize=8.7, leading=12, textColor=INK, spaceAfter=9, allowWidows=0, allowOrphans=0, splitLongWords=1),
}

def clean(s):
    return s.replace('\u2011','-').replace('\u2013','-').replace('\u2014',' - ')

def inline(text, refs=False, note=False):
    text = clean(text)
    text = html.escape(text, quote=False)
    # URLs are linked and kept legible in notes. ReportLab wraps long words.
    text = re.sub(r'https?://[^\s<>]+', lambda m: '<link href="'+m[0].rstrip('.,;')+'" color="#36574F">'+m[0].rstrip('.,;')+'</link>'+m[0][len(m[0].rstrip('.,;')):], text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*([^*]+)\*', r'<i>\1</i>', text)
    def reference(m):
        key = m[1]; num = notes[key]['number']
        anchor = '' if key in anchors else f'<a name="ref-{num}"/>'
        anchors.add(key)
        return anchor + f'<super><link href="#note-{num}" color="#36574F">{num}</link></super>'
    return re.sub(r'\[\^([^\]]+)\]', reference, text) if refs else text

def page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(GRAY)
    canvas.setFont('Sans', 6.9)
    canvas.drawString(LEFT, H-29, 'CREATURES OF CONTEXT')
    canvas.setFont('Book', 8)
    canvas.drawCentredString(W/2, 25, str(doc.page))
    canvas.restoreState()

class BookDoc(BaseDocTemplate):
    def __init__(self, filename):
        super().__init__(filename, pagesize=(W,H), leftMargin=LEFT,rightMargin=RIGHT,topMargin=TOP,bottomMargin=BOTTOM,title=TITLE,author=AUTHOR,subject=SUBTITLE, pageCompression=1)
        frame = Frame(LEFT,BOTTOM,W-LEFT-RIGHT,H-TOP-BOTTOM,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
        self.addPageTemplates([PageTemplate(id='cover',frames=frame),PageTemplate(id='body',frames=frame,onPage=page)])
    def afterFlowable(self, flowable):
        if getattr(flowable, 'nav_key', None):
            key, title, level = flowable.nav_key, flowable.nav_title, flowable.nav_level
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(title,key,level=level,closed=False)
            self.notify('TOCEntry',(level,html.escape(title),self.page,key))

def navparagraph(text, style, key, title, level=0):
    p = Paragraph(inline(text),styles[style])
    p.nav_key, p.nav_title, p.nav_level = key,title,level
    return p

anchors=set()
story = [Spacer(1,87),Paragraph('CREATURES<br/>OF CONTEXT',styles['cover']),Paragraph(SUBTITLE,styles['subtitle']),Spacer(1,139),Paragraph(inline(AUTHOR),styles['small']),Paragraph(inline(EDITION),styles['small']),NextPageTemplate('body'),PageBreak()]
story += [Paragraph('About this edition',styles['chapter'])]
for block in EDITION_NOTE.split('\n\n'):
    story += [Paragraph(inline(block),styles['small'])]
story += [PageBreak(),Paragraph('Contents',styles['chapter'])]
toc=TableOfContents()
toc.levelStyles=[ParagraphStyle('TOC0',fontName='BookBold',fontSize=10.1,leading=14,spaceBefore=6,leftIndent=0,firstLineIndent=0,textColor=INK),ParagraphStyle('TOC1',fontName='Book',fontSize=9.5,leading=13,spaceBefore=0,leftIndent=12,firstLineIndent=0,textColor=INK)]
toc.dotsMinLevel = 1
story += [toc,PageBreak()]
for i,c in enumerate(chapters):
    n=c['number']
    if n in PARTS:
        roman,parttitle,description=PARTS[n]
        story += [Spacer(1,112),Paragraph('PART '+roman,styles['label']),navparagraph(parttitle,'chapter',f'part-{roman}',f'Part {roman}: {parttitle}'),Paragraph(inline(description),styles['body']),PageBreak()]
    story += [Paragraph(c['label'].upper(),styles['label']),navparagraph(c['title'],'chapter',f'chapter-{i}',c['label']+': '+c['title'],1 if n else 0)]
    # Small spacing adjustments keep short chapter endings with their preceding page.
    chapter_body_style = styles['body']
    if n in (3, 7, 8):
        chapter_body_style = ParagraphStyle('body-compact-'+str(n), parent=styles['body'], leading=14.6, spaceAfter=7)
    for block in c['body'].split('\n\n'):
        block=' '.join(block.split())
        if not block:continue
        if block.startswith('#'):
            story.append(Paragraph(inline(block.lstrip('#').strip()),styles['section']))
        else:
            story.append(Paragraph(inline(block,refs=True),chapter_body_style))
    story.append(PageBreak())
story.append(navparagraph('Notes','chapter','notes','Notes'))
story.append(Paragraph('Numbers link back to their first occurrence in the text. Source links open the cited material.',styles['small']))
for c in chapters:
    if not c['notes']:continue
    story.append(Paragraph(inline(c['label']+': '+c['title']),styles['section']))
    for key in c['notes']:
        n = notes[key]['number']
        markup=f'<a name="note-{n}"/><b>{n}.</b> '+inline(notes[key]['text'])+f' <font size="7"><link href="#ref-{n}" color="#36574F">Return</link></font>'
        story.append(Paragraph(markup,styles['note']))
doc=BookDoc(str(OUT/'Creatures_of_Context.pdf'))
doc.multiBuild(story)

css='''body {font-family: Georgia, serif; line-height: 1.5; margin: 5%;}
p {margin-top: 0; margin-bottom: .8em;}
h1,h2,h3 {font-weight: normal; line-height: 1.2; text-align: left; break-after: avoid;}
h1 {font-size: 1.9em; margin: 2em 0 1em;}
h2 {font-size: 1.55em; margin: 2em 0 1em;}
h3 {font-size: 1.12em; font-weight: bold; margin-top: 1.7em;}
a {color: inherit; text-decoration: underline; overflow-wrap: anywhere;}
.footnote-ref {font-size: .85em;}
.footnotes {font-size: .9em;}
.title {font-size: 2.4em; margin-top: 2em;}
.subtitle {font-size: 1.2em;}
nav ol {list-style-type: none; padding-left: 1em;}
'''
(ROOT/'reader.css').write_text(css)
pandoc=shutil.which('pandoc')
helptext=subprocess.check_output([pandoc,'--help'],text=True)
split='--split-level=2' if '--split-level' in helptext else '--epub-chapter-level=2'
subprocess.run([pandoc,str(OUT/'Creatures_of_Context.md'),'-f','markdown+footnotes','-t','epub3','--standalone','--toc','--toc-depth=2',split,'--css='+str(ROOT/'reader.css'),'-o',str(OUT/'Creatures_of_Context.epub')],check=True)

manifest={'title':TITLE,'subtitle':SUBTITLE,'author':AUTHOR,'edition':DATE,'status':'reader beta',
          'chapters':len(numbers),'front_and_back_chapters':2,'unique_source_notes':len(notes),
          'main_text_words':sum(len(re.findall(r"\b[\w’'-]+\b",c['body'])) for c in chapters),
          'word_count_including_notes':sum(len(re.findall(r"\b[\w’'-]+\b",c['body'])) for c in chapters)+sum(len(re.findall(r"\b[\w’'-]+\b",n['text'])) for n in notes.values()),
          'source':{'path':str(SOURCE.relative_to(ROOT)),'sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest()},
          'files':{p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in OUT.iterdir() if p.suffix in ['.pdf','.epub','.md']}}
(ROOT/'EDITION_MANIFEST.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps(manifest,indent=2))
