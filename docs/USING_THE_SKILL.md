# Use the Human Science Prose Editor

A skill is a set of saved instructions and reference material for an AI assistant. This one asks the assistant to improve writing while preserving what the passage says and what its evidence allows.

The [skill folder](../skills/edit-human-science-prose/) contains the original instructions and supporting guides. Keep them together. You can read them as a checklist or use them with an assistant that can load those files. Downloading the folder alone does not install it.

The skill is preserved from an earlier stage of this project. Later reviews and the October 18 integration edit did not apply it. See [what we learned](../methods/WORKFLOW.md) before treating these instructions as a model for the whole process.

## Choose a job

| Job | What to ask for |
|---|---|
| Review | Quote the passages that need attention, explain the problem, and suggest a small change. |
| Edit | Revise the passage, explain the important changes, and flag unresolved questions. |
| Check voice | Compare passages with samples you approve, allowing different subjects to have different rhythms. |

Supply the passage, the paragraphs around it, who it is for, and what it needs to explain. Include the relevant sources if you want the assistant to check whether the wording matches them.

Here is a starting prompt:

> Read the skill and its required references. Review this passage and the paragraphs around it. It should help a general reader understand what the experiment measured and what we can conclude. Identify up to three important problems and quote the affected wording. Suggest changes before rewriting. Preserve the study's limits and flag anything you cannot check.

After reviewing the suggestions, choose which changes to make. Compare the result with the original, especially any wording about causes, uncertainty, or the people a finding applies to.

## What to watch for

The skill asks the assistant to preserve meaning, examine weak writing habits, and check its own revision. Its checklist calls some requirements “hard gates,” but those are instructions to the model, not independently enforced tests.

A fluent revision can still be wrong. Source checking requires actually inspecting the source. The [evidence-record template](../templates/EVIDENCE_RECORD.md) helps keep track of what was checked and what remains uncertain.

The skill also prohibits inventing details during an ordinary edit. Our book contains explicitly fictional illustrations; those do not justify adding unrecorded dialogue or motives to a real person's story.

The included skill and reference guides retain their [MIT license](../skills/edit-human-science-prose/LICENSE) and attribution to Peter Yang's `no-ai-slop` project. The skill's effect on this book has not been tested separately from the other revisions.
