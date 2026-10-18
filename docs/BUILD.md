# Build the reading editions

Requirements: **Python 3.10+**, **Pandoc**, and the packages in [`requirements.txt`](../requirements.txt). DejaVu fonts are loaded from the system, with Matplotlib's bundled fonts as a fallback. The [build-environment record](../records/BUILD_ENVIRONMENT.json) lists the versions used for this beta.

From the repository root, after installing Pandoc:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 build_edition.py
python3 validate_edition.py
```

On Windows, activate the environment with `.venv\Scripts\Activate.ps1` in PowerShell.

Edit [`manuscript/Creatures_of_Context.md`](../manuscript/Creatures_of_Context.md), then rebuild. The builder reads its title, author, date, chapter structure, and notes, and generates the Markdown, PDF, EPUB, and [`EDITION_MANIFEST.json`](../EDITION_MANIFEST.json). Editing a generated reading file directly will not change the next build.

The validator checks chapter/output consistency, note order, EPUB resources and anchors, PDF destinations, and text bounds. The [technical results](../records/TECHNICAL_QA.json) and [visual-review record](../records/VISUAL_QA.md) describe the checks performed. They do not verify scientific claims. A new release also needs visual inspection; e-reader rendering can vary between applications.

An optional replay applies the recorded replacements to the archived input and checks that it produces the archived October 2 chapters:

```bash
python3 replay_style_pass.py ../creatures-style-replay
```

Choose a nonexistent destination directory. The replay does not overwrite the working manuscript. Its inputs and outputs are historical snapshots; it does not reproduce later revisions. The October 18 changes have a separate replacement record. PDF and EPUB metadata can differ between builds; the manifest identifies the delivered files without promising identical binary output across systems.
