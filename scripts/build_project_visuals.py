#!/usr/bin/env python3
"""Render exact recorded before/after passages as PNG and SVG comparisons."""
from html import escape
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parents[1]
WIDTH = 1440
PAPER, INK, MUTED = '#f7f4eb', '#223531', '#52605a'
TEAL, RULE, PANEL = '#24685c', '#c7cec2', '#e8eee4'


def font(size, serif=False, bold=False):
    prop = font_manager.FontProperties(
        family='DejaVu Serif' if serif else 'DejaVu Sans',
        weight='bold' if bold else 'normal')
    return ImageFont.truetype(font_manager.findfont(prop), size)


def lines_for(text, typeface, width):
    result = []
    for paragraph in text.split('\n\n'):
        if result:
            result.append('')
        line = ''
        for word in paragraph.split():
            proposed = f'{line} {word}'.strip()
            if typeface.getlength(proposed) > width and line:
                result.append(line)
                line = word
            else:
                line = proposed
        result.append(line)
    return result


class Canvas:
    def __init__(self, height, title, description):
        self.image = Image.new('RGB', (WIDTH, height), PAPER)
        self.draw = ImageDraw.Draw(self.image)
        self.svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}" role="img" aria-labelledby="title desc">',
                    f'<title id="title">{escape(title)}</title>',
                    f'<desc id="desc">{escape(description)}</desc>',
                    f'<rect width="{WIDTH}" height="{height}" fill="{PAPER}"/>']

    def rectangle(self, xy, fill):
        x0, y0, x1, y1 = xy
        self.draw.rectangle(xy, fill=fill)
        self.svg.append(f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="{fill}"/>')

    def text(self, x, y, text, size=26, color=INK, serif=False, bold=False):
        face = font(size, serif, bold)
        self.draw.text((x, y), text, fill=color, font=face, anchor='lt')
        # SVG uses a baseline; Pillow's top anchor begins at the ink bounds.
        ascent = face.getbbox(text or 'A')[1]
        family = 'DejaVu Serif' if serif else 'DejaVu Sans'
        weight = 'bold' if bold else 'normal'
        self.svg.append(f'<text x="{x}" y="{y+size-ascent}" fill="{color}" font-family="{family}" font-size="{size}" font-weight="{weight}">{escape(text)}</text>')

    def paragraph(self, x, y, lines, size=28, line_height=40, **kwargs):
        for line in lines:
            if line:
                self.text(x, y, line, size=size, **kwargs)
            y += line_height

    def save(self, name):
        target = ROOT / 'assets' / name
        self.image.save(target.with_suffix('.png'))
        target.with_suffix('.svg').write_text('\n'.join(self.svg + ['</svg>']) + '\n')


EXAMPLES = [
    dict(name='example-decision', chapter='01_regulators.md', needle='The visit has done',
         number='01', title='Stay inside the decision',
         challenge='Three new situations interrupt a decision already worth following.',
         change='The visit supplies information the applicant can act on.',
         note='The revision connects an observation to the next question. It keeps the reader with the applicant long enough to see what changed.'),
    dict(name='example-connection', chapter='09_connection.md', needle='At the reading group',
         number='02', title='Give recognition an event',
         challenge='The paragraph names continuity, then explains it again.',
         change='A remembered book makes the next conversation possible.',
         note='Recognition now has a particular cause and consequence. The reader can follow what is different about returning to the same group.'),
    dict(name='example-delay', chapter='11_delay.md', needle='Suppose the author finally',
         number='03', title='Let the attempt discover something',
         challenge='The draft says a rough paragraph could reveal a problem.',
         change='The paragraph exposes an inference the writer cannot support.',
         note='The example makes the missing evidence specific: attendance alone cannot establish benefit. The imperfect draft changes the next action.'),
]


def main():
    edits = json.loads((ROOT / 'records/STYLE_CHANGES.json').read_text())
    for example in EXAMPLES:
        matches = [e for e in edits if e['chapter'] == example['chapter']
                   and e['after'].startswith(example['needle'])]
        if len(matches) != 1:
            raise ValueError(f"Expected one recorded edit: {example['name']}")
        edit = matches[0]
        # Only publish comparisons whose full passages remain in these editions.
        assert edit['before'] in (ROOT / 'archive/pre_style/chapters' / edit['chapter']).read_text()
        assert edit['after'] in (ROOT / 'archive/october-02/chapters' / edit['chapter']).read_text()
        body_font = font(29, serif=True)
        before = lines_for(edit['before'], body_font, 594)
        after = lines_for(edit['after'], body_font, 594)
        note = lines_for(example['note'], font(27), 1296)
        challenge = lines_for(example['challenge'], font(25), 594)
        change = lines_for(example['change'], font(25), 594)
        body_top = 266 + max(len(challenge), len(change)) * 35
        body_bottom = body_top + max(len(before), len(after)) * 42
        note_top = body_bottom + 54
        height = note_top + len(note) * 38 + 92
        c = Canvas(height, example['title'],
                   'Exact manuscript excerpts, before and after. Both depict a fictional illustration. Text and commentary are available in methods/WORKED_EXAMPLES.md.')
        c.rectangle((0, 0, 12, height), TEAL)
        c.text(60, 40, 'CREATURES OF CONTEXT  /  EDITORIAL EXAMPLE ' + example['number'], 22, color=TEAL, bold=True)
        c.text(60, 91, example['title'], 48, serif=True)
        c.text(62, 156, f"Chapter {int(example['chapter'][:2])} · Exact excerpts · Fictional illustration", 24, color=MUTED)
        c.rectangle((738, 208, 1408, body_bottom+26), PANEL)
        c.text(64, 227, 'BEFORE', 22, color=MUTED, bold=True)
        c.text(768, 227, 'AFTER', 22, color=TEAL, bold=True)
        c.paragraph(64, 272, challenge, 25, 35, color=MUTED)
        c.paragraph(768, 272, change, 25, 35, color=TEAL)
        c.paragraph(64, body_top+20, before, 29, 42, serif=True)
        c.paragraph(768, body_top+20, after, 29, 42, serif=True)
        c.rectangle((64, note_top-16, 1372, note_top-14), RULE)
        c.paragraph(64, note_top+12, note, 27, 38)
        c.text(64, height-40, 'Editorial intention, not a measured reader outcome.  Source: records/STYLE_CHANGES.json', 20, color=MUTED)
        c.save(example['name'])
        print(f"{example['name']}: {WIDTH} × {height}; exact excerpts verified")


if __name__ == '__main__':
    main()
