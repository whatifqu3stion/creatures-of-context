# Creatures of Context

*Understanding Behavior in a World We Share*

This book grew out of a question I wanted to understand better: **what becomes possible when we understand someone's behavior more accurately, and where does that understanding reach its limits?** AI helped me explore it. As the conversation developed, I wanted to keep something of what we had found. The book became that record, and an attempt to make the book I hadn't been able to find.

I understand the discomfort around an AI-written book. There are questions about whose voice you're hearing, whether the information deserves your trust, and what gets lost when writing becomes easy to produce. AI did a substantial amount of the research, drafting, and rewriting here. I chose the direction, questioned the results, and asked for changes. This project is an honest account of that experiment, including the parts that remained difficult.

## Read the book

The book follows behavior through bodies, learned expectations, everyday routines, relationships, and shared rules. Its examples sometimes end with a workable change, sometimes with a clearer disagreement.

**Reader beta · 18 October 2026 · 13 chapters · 64 source notes**

[Markdown](output/Creatures_of_Context.md) · [PDF](output/Creatures_of_Context.pdf) · [EPUB](output/Creatures_of_Context.epub)

The opening begins with a manager's message: *Can we talk tomorrow?*

> You might keep eating dinner. You might put down your fork.

The words on the phone are the same. Understanding the response takes us into the relationship, the recent past, and what the conversation could cost.

## What helped, and what didn't

The process was messy. We tried plans, editing instructions, comparisons with other nonfiction, repeated reviews, and rewrites from other models. Those changed together, so I can't isolate which tool deserves credit for an improvement.

Voice was one of the hardest parts. We wanted science that was engaging and enjoyable to read. The prose could be clear sentence by sentence and still become predictable across a chapter: a scene, a study, a qualification, a careful conclusion. At the paragraph level, a finding was often followed by what it could not prove, then a balancing sentence. Scientific caution had become a repeated rhythm. We needed to keep the limits that change what a result means while removing explanations the surrounding text or notes already supplied. The [qualification comparison](methods/WORKED_EXAMPLES.md#7-reduce-qualifications-without-changing-the-finding) shows one attempt. I wouldn't claim we solved that. Some decisions were a matter of leaving a passage alone when another edit no longer seemed likely to help.

Specific requests worked better than broad ones. “Make it more human” gave us less to act on than “let the first attempt reveal the problem” or “show what the researchers actually did.” In the sleep chapter, leaving the phone downstairs fails when the parent stays up with a printed book instead. The example becomes more interesting when the reader discovers why the first explanation was incomplete.

We also cut too far in places. “The work has become clearer, not more possible” is a useful distinction, even though its form resembles other contrasts we were removing. A rule against a repetitive pattern cannot decide whether a particular sentence earns its place.

One recent edit made a study's limitation easier to picture:

**Before**

> These were observational records: illness could reduce movement, and other differences between more and less active people could contribute to the association.

**After**

> They also captured lives already in progress. Illness could reduce movement, and other differences between more and less active people could contribute to the association.

The explanation is still cautious, but its opening points back to the people being studied. It is longer; brevity was not the only aim.

The [paragraph comparisons](methods/WORKED_EXAMPLES.md) include seven pairs from earlier and recent work. Each identifies its sources and explains what the change gained or gave up.

## What the skills were good for

The skills we developed were saved instructions for the assistant. The included [editing skill](docs/USING_THE_SKILL.md) helped carry checks between tasks: preserve the claim, keep necessary uncertainty, inspect the source, and compare a revision with its original.

Those instructions were easier to write than to satisfy. A checklist could draw attention to repeated wording while missing a flat chapter. It could encourage caution without noticing that every result now had the same careful disclaimer. Asking the same system to write, apply its own rules, and pronounce the result finished also gave us too little distance from the work. The assistant sometimes called a draft finished before later reviews found substantial problems.

One small example shows why a polished sentence still needed scrutiny:

**Before**

> A method can become more effective at surveillance while making life worse for those watched.

**After**

> A method can become more effective at surveillance without improving the lives of those watched.

The second makes the point we needed: better performance does not establish a human benefit. The first adds a claim of harm. The difference is easy to miss when judging only fluency.

We eventually asked for reviews without our custom writing skill. The final integration edit did not use it either. The skill is available to inspect; its separate effect on the book has not been measured.

Would I use one again? Yes, but with a smaller job. I would keep a short set of requirements about sources, invented detail, and preserving meaning. Then I would separate the tasks: develop an explanation, read it for interest and rhythm, and check that the edits still fit the evidence. Those tasks need one another, but asking a single long instruction to do everything seemed to promise more than we could judge.

I would also expect to revise the instructions when they kept producing the same problem. A later pass is useful for catching mistakes; it should not become a routine repair job for habits we have already identified. The goal would be a repeatable process with room for judgment, not a formula that makes every paragraph sound alike.

We have now made one part of that separation automatic. [GitHub checks](https://github.com/whatifqu3stion/creatures-of-context/actions/workflows/verify-edition.yml) run on pull requests and changes to `main`, checking the submitted manuscript and reading files for consistency, footnote order, and internal navigation. This catches production mistakes without asking an editor to remember every technical check. Source review still has to establish what a claim supports; editorial review and reader feedback still have to assess clarity, enjoyment, and progression. The [division of responsibilities](methods/WORKFLOW.md#who-checks-what) explains what each review can establish.

## Different models, and a fresh conversation

Reviews and rewrites from other models drew attention to things we had become used to, especially repetitive qualifications and a middle section that could feel predictable. Some proposed cuts helped. Others removed useful warmth or changed the meaning. We compared passages and kept selected changes.

This was not a fair test of which model writes best. The prompts, drafts, and conversations differed. Agreement between models was a reason to investigate a passage, not a substitute for reading it or checking a source.

Working in one continuing conversation helped preserve decisions and the reasons behind them. It also made it easy to keep explaining what a passage was meant to achieve. A reader only has the passage. Starting a fresh conversation with the manuscript, its intended audience, and a few neutral questions helped us test that gap. Next time I would make that separation more deliberate: leave earlier reviews and preferred fixes out of the first reading, then bring useful findings back into the working conversation.

## What I would do next time

I'd make the work more repeatable by setting clear points to check it:

1. **Write a short brief.** State the question, audience, and what each chapter should help the reader understand. Allow a chapter to challenge the premise.
2. **Keep a claim record.** Save the source, what was actually inspected, and the limits the wording needs to retain. Add to it when writing introduces new detail.
3. **Try two different chapters early.** Compare substantial passages for clarity, enjoyment, and discovery before expanding a style guide or drafting the whole book.
4. **Separate revision from a fresh read.** Keep decisions in the working conversation; give a fresh reviewer the manuscript without our explanation of why it should work. Involve human readers sooner.
5. **Edit against named problems.** Compare before and after, check changed claims, and keep a good passage when the alternative offers no clear benefit.
6. **Finish a version and test it.** Rebuild the reading copies, check their navigation and layout, then collect reader responses before starting another broad revision.

That is the approach I'd try next, rather than a method this project has already proven. The [process account](methods/WORKFLOW.md) gives the fuller reasoning and limits.

## Status and project files

The complete reader beta has received AI-assisted editorial review and selective source checks. It has not received independent specialist review or an organized general-reader test. Useful feedback identifies where you became interested, started skimming, got confused, or found a claim the source does not support.

[Current status](docs/STATUS.md) · [Next steps](docs/ROADMAP.md) · [Build instructions](docs/BUILD.md) · [Source-check record](records/EVIDENCE_CHANGES.md) · [Evidence template](templates/EVIDENCE_RECORD.md)

---

Maintained by [whatifqu3stion](https://github.com/whatifqu3stion). The archived editing skill retains its [MIT license](skills/edit-human-science-prose/LICENSE) and attribution to Peter Yang's `no-ai-slop` project. The manuscript and other project materials do not currently have a general reuse license.
