"""Replay recorded editorial decisions into a NEW directory; never edits sources."""
from pathlib import Path
import json, sys

root = Path(__file__).resolve().parent
if len(sys.argv)!=2:
    raise SystemExit('Usage: python3 replay_style_pass.py NEW_OUTPUT_DIRECTORY')
target=Path(sys.argv[1]).resolve()
if target.exists():
    raise SystemExit('Choose a nonexistent directory; existing files will not be overwritten.')
source=root/'archive'/'pre_style'/'chapters'
texts={p.name:p.read_text() for p in source.glob('*.md')}
if len(texts)!=16:
    raise SystemExit('Expected the 16 archived pre-pass chapter files.')
for change in json.loads((root/'records'/'STYLE_CHANGES.json').read_text()):
    name=change['chapter']
    if name not in texts or texts[name].count(change['before'])!=1:
        raise SystemExit(f'Input mismatch for {name}; replay stopped without writing.')
    texts[name]=texts[name].replace(change['before'],change['after'])
for name,text in texts.items():
    if text!=(root/'archive'/'october-02'/'chapters'/name).read_text():
        raise SystemExit(f'Replayed chapter differs from archived October 2 output: {name}')
target.mkdir(parents=True)
for name,text in texts.items():
    (target/name).write_text(text)
print(f'Replayed {len(texts)} chapters; all match the archived October 2 chapter outputs.')
