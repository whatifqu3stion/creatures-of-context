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

## Automatic checks on GitHub

[Verify reading editions](../.github/workflows/verify-edition.yml) runs on pull requests and pushes to `main`, and can also be started manually from the repository's Actions tab. It installs only the validation dependency and checks the committed manuscript, manifest, and reading files. It deliberately does not rebuild first: doing so could replace a stale output and conceal that it was missing from the submitted update. This workflow validates delivered files; building and visually reviewing a new edition remain separate release tasks.

To run the same check locally without installing the build tools:

```bash
python3 -m pip install -r requirements-checks.txt
python3 validate_edition.py
```

The validator writes diagnostics to the terminal and `records/TECHNICAL_QA.json`, and exits unsuccessfully when checks fail. If an edition is out of date, rebuild from the canonical manuscript, inspect the result, and commit the manuscript, generated reading files, manifest, and updated technical record together. Do not change the manifest just to silence a mismatch.

Passing checks establish file consistency and the navigation checks listed above. They do not verify external URLs, scientific accuracy, visual quality, or readability. See [who checks what](../methods/WORKFLOW.md#who-checks-what) for the remaining reviews.

## Replay the historical edit

An optional replay applies the recorded replacements to the archived input and checks that it produces the archived October 2 chapters:

```bash
python3 replay_style_pass.py ../creatures-style-replay
```

Choose a nonexistent destination directory. The replay does not overwrite the working manuscript. Its inputs and outputs are historical snapshots; it does not reproduce later revisions. The October 18 changes have a separate replacement record. PDF and EPUB metadata can differ between builds; the manifest identifies the delivered files without promising identical binary output across systems.
