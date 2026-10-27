# Creatures of Context

*Understanding Behavior in a World We Share*

This book grew out of a question I wanted to understand better: **what becomes possible when we understand someone's behavior more accurately, and where does that understanding reach its limits?** It became an attempt to make the book I hadn't been able to find.

## Read the book

**[Read online](output/Creatures_of_Context.md) · [PDF](output/Creatures_of_Context.pdf) · [EPUB](output/Creatures_of_Context.epub)**

**Reader beta · 18 October 2026 · 13 chapters · 64 source notes**

The book follows behavior through bodies, learned expectations, everyday routines, relationships, and shared rules. Its examples sometimes end with a workable change, sometimes with a clearer disagreement.

It opens with a manager's message: *Can we talk tomorrow?*

> You might keep eating dinner. You might put down your fork.

The words on the phone are the same. Understanding the response takes us into the relationship, the recent past, and what the conversation could cost.

## Making the book

AI did a substantial amount of the research, drafting, and rewriting here. I chose the direction, questioned the results, and asked for changes. There are reasonable questions about whose voice you're hearing and whether the information deserves your trust. The repository keeps the process, editing examples, and source-check records available to inspect.

Voice was one of the hardest parts. The prose could be clear sentence by sentence and still become predictable across a chapter: a scene, a study, a qualification, a careful conclusion. I wanted science that was engaging to read without losing the limits that matter.

One edit shows the kind of decision that involved:

**Before**

> These were observational records: illness could reduce movement, and other differences between more and less active people could contribute to the association.

**After**

> They also captured lives already in progress. Illness could reduce movement, and other differences between more and less active people could contribute to the association.

The revision is longer. It brings the people behind the records back into view while keeping the reason for caution. Brevity wasn't the only aim.

Other cuts removed useful warmth or changed a claim. Saved editing instructions and fresh model reviews helped us notice problems, but they could also miss them. Next time I'd involve human readers sooner, test a couple of chapters before drafting the whole book, and keep the source checks separate from the reading-for-enjoyment pass.

| Explore the process | What's there |
| --- | --- |
| [How we worked](methods/WORKFLOW.md) | What helped, what failed, and the workflow I'd try next. |
| [Seven editing comparisons](methods/WORKED_EXAMPLES.md) | Before-and-after passages, their sources, and what each change gained or gave up. |
| [Source-check record](records/EVIDENCE_CHANGES.md) | The specific checks and corrections recorded so far, rather than a claim of a complete audit. |

## Build the reading editions

Nothing needs installing to read the book. To rebuild it, use Git, Python 3.12 (used for the recorded beta build), and Pandoc. The [build guide](docs/BUILD.md) covers setup details and Windows activation.

1. **Clone the repository and open its folder.**

   ```bash
   git clone https://github.com/whatifqu3stion/creatures-of-context.git
   cd creatures-of-context
   ```

2. **Create and activate a Python environment.** These activation commands are for macOS/Linux shells.

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install the Python dependencies.** Install Pandoc separately before running the build.

   ```bash
   python3 -m pip install -r requirements.txt
   ```

4. **Build and check the editions.**

   ```bash
   python3 build_edition.py
   python3 validate_edition.py
   ```

The builder reads one [source manuscript](manuscript/Creatures_of_Context.md) and writes the Markdown, PDF, and EPUB editions to `output/`, along with a root-level edition manifest. Edit the manuscript rather than the generated copies.

[GitHub checks](.github/workflows/verify-edition.yml) validate the committed files without rebuilding first, so an out-of-date reading copy isn't silently replaced before it can be caught. They check consistency, note order, and internal navigation. Scientific accuracy, page appearance, and the reading experience need separate review.

## Status and feedback

This reader beta has received AI-assisted editorial review and selective source checks. It has not received independent specialist review or an organized general-reader test.

Useful feedback is specific: where did you become interested, start skimming, get confused, or find a claim its source doesn't support? That's more useful to the next revision than another open-ended request to improve everything.

[Current status](docs/STATUS.md) · [Next steps](docs/ROADMAP.md) · [Editing skill and its limits](docs/USING_THE_SKILL.md)

---

The manuscript and other project materials do not currently have a general reuse license. The archived editing skill retains its [MIT license](skills/edit-human-science-prose/LICENSE) and attribution to Peter Yang's `no-ai-slop` project.
