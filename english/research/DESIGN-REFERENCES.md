# Design references for the English RAG presentation

Research date: 2026-11-13. Status: reference research and proposed visual direction; no presentation has been created by this research task.

Current delivery constraints confirmed by the parent: 12 slides, B2 English, 10–12 minutes, PPTX plus a printable EN/RU DOCX script. Visual choices should leave time for explanation rather than require rapid reading of dense slide text.

## Scope and method

The references below are real technical slide decks from identifiable first-party presenters or official conference sources. They are useful examples, not an objective ranking of the world's best presentations. Design observations are my interpretation of the rendered slides, rather than claims made by their authors.

I downloaded the three PDFs to `/private/tmp`, extracted their text with the already available `pypdf`, rendered the selected pages with the already available Poppler `pdftoppm`, and **opened the rendered PNGs for visual inspection**. Page numbers below are one-based PDF pages, including covers. No dependencies were installed.

The web PDF screenshot tool was attempted: some NVIDIA requests timed out and the DeepMind PDF exceeded the web fetch size limit. Local rendering succeeded, so the observations are based on actual slide images, not search snippets alone.

## 1. NVIDIA: Bringing Generative AI to Life with NVIDIA Jetson

- Author: Dustin Franklin, Principal Engineer; cover date November 7, 2023.
- [Official NVIDIA PDF](https://info.nvidia.com/rs/156-OFN-742/images/Bringing_Generative_AI_to_Life.pdf?version=0), 30 pages.
- Visually inspected **pages 1, 6, 25**.
- Page 1 combines a black field, oversized white title, and a large green sculptural form. Page 6 gives most of the canvas to a two-series chart with directly visible bar values. Page 25 changes to a text/architecture split and uses the accent color to identify the important processing blocks.
- Adopt: strong contrast, one unmistakable accent, chart-first evidence pages, and different compositions for explanation versus measurement.
- Adapt: use fewer diagram nodes and larger labels for a B2 classroom audience. Do not reuse NVIDIA branding, benchmark numbers, or green styling as if they belonged to our project.
- Local inspected renders: `/private/tmp/rag-nvidia-jetson2023-p1.png`, `-p6.png`, `-p25.png`.

## 2. Google DeepMind and collaborators: Inference Scaling for Long-Context Retrieval Augmented Generation

- [Official ICLR 2025 slide PDF](https://iclr.cc/media/iclr-2025/Slides/31886.pdf), 38 pages; [associated paper](https://arxiv.org/abs/2410.04343).
- Visually inspected **pages 1, 9, 23, 28**.
- Page 1 establishes hierarchy with an exceptionally large title and a restrained geometric illustration. Page 9 places a short explanation beside a simplified input/output diagram. Page 23 groups evidence across datasets; page 28 interrupts the dense scientific sequence with one large takeaway and a selectively colored phrase.
- Adopt: diagrams with a small number of clearly labeled stages, deliberate alternation of explanation and evidence, and a conclusion that can be understood at a glance.
- Adapt: page 23's eight small panels would be too dense for our short classroom deck. Show one chart with a clear metric and conclusion instead. The original uses a light theme; its hierarchy and sequencing can be translated into the requested dark theme.
- Local inspected renders: `/private/tmp/rag-deepmind-iclr2025-p1.png`, `-p9.png`, `-p23.png`, `-p28.png`.

## 3. Microsoft RAGHack: Intro to GraphRAG

- Presenters: John Alexander and Apurva Mody, Microsoft; event September 6, 2024.
- [Official Microsoft event](https://developer.microsoft.com/en-us/reactor/events/23432/), [Microsoft's session resource thread linking the slides](https://github.com/microsoft/RAG_Hack/discussions/55), [presenter's PDF](https://github.com/ms-johnalex/intro-to-graphrag/blob/main/RAGHackSession-Intro-to-GraphRAG.pdf).
- This is a Microsoft developer-event deck, **not a verified Microsoft Research lab deck**.
- Visually inspected **pages 3 and 19** of the 24-page PDF.
- Page 3 uses near-black, white typography, generous empty space, and a left-aligned title. Page 19 uses a dark blue background and a diagram to explain how text becomes a graph and communities.
- Adopt: the quiet dark canvas and a visible document-to-graph story.
- Adapt: page 19 has too many simultaneous elements for our audience. Our overview should expose about four main stages; the real graph belongs on a separate page with a simple explanatory caption.
- Local inspected renders: `/private/tmp/rag-microsoft-raghack2024-p3.png`, `-p19.png`.

## Real primary-source visuals suitable for screenshots

### A. GraphRAG documentation: real graph plus English source caption

- [Official GraphRAG welcome page](https://microsoft.github.io/graphrag/).
- [Original graph JPEG](https://microsoft.github.io/graphrag/img/GraphRag-Figure1.jpg).
- The page identifies the figure as a knowledge graph generated with GPT-4 Turbo. The graph itself uses colored node clusters and has no language labels; its existing caption and surrounding documentation are English. The original asset was downloaded and **visually opened**: `/private/tmp/rag-graphrag-official-figure1.jpg`.
- Recommended slide use: capture the actual documentation region containing the graph, its original English caption, and enough heading context to identify the source. Add a separate concise English explanation that dots represent entities and colors represent communities, consistent with the page's description.
- Important distinction: the downloaded JPEG is an **original source figure**, not a browser screenshot. Capture the real page during production if the assignment literally requires screenshots. Do not fabricate a browser window around the figure or claim this graph came from our own experiment.

### B. Anthropic: Contextual Retrieval practical example

- [Original Anthropic article](https://www.anthropic.com/research/contextual-retrieval), published September 19, 2024; the older `/engineering/contextual-retrieval` URL redirects here.
- Recommended screenshot region: the section titled **Introducing Contextual Retrieval**, specifically the genuine `original_chunk` / `contextualized_chunk` code example. It demonstrates a financial-information chunk that becomes clearer when company and reporting-period context is added. This is a source-authored example, not a student experiment or an observed production customer exchange.
- Optional supporting original assets: [preprocessing diagram](https://assets.claude.com/2496e7c6fedd7ffaa043895c23a4089638b0c21b.png), [retrieval-results chart](https://assets.claude.com/7f8d739e491fe6b3ba0e6a9c74e4083d760b88c9.png). Both were downloaded and **visually opened** as `/private/tmp/rag-anthropic-contextual-flow.png` and `/private/tmp/rag-anthropic-contextual-results.png`.
- The article reports top-20 retrieval failure rates; those values must not be relabeled as overall answer accuracy. Use a real page screenshot for the practical example and a separately redrawn, accurately cited native chart for quantitative results.

No browser screenshot of either live page has been created in this research task. The source pages, their figure assets, and the PDF slide renders have been verified; actual page capture remains a production step.

## Proposed visual concept: evidence moving through a system

This is a recommendation derived from the inspected references, pending the parent's final deck plan.

- **Canvas:** 16:9, deep navy `0B1220`; slightly lighter regions `142035`; bright text `F7FAFC`; secondary text `B9C6D8`.
- **Meaningful color:** cyan `39D0D8` for retrieved evidence, muted blue `6F91E8` for model/system stages, amber `F5C76A` for limitations or a finding worth discussing. These colors reflect document flow, rather than copying a company's identity.
- **Typography:** Arial for compatibility; titles around 34–42 pt, body 20–24 pt, diagram labels at least 18 pt when feasible. Use a small number of short English sentences on each slide; put the longer bilingual explanation in notes/script.
- **Unifying motif:** a document fragment connected to an answer through a visible retrieval path. Use it where it explains the content, rather than adding decorative stripes, neon grids, or floating robot artwork.
- **Layout rhythm:** alternate a large title composition, a compact numbered agenda, a problem/evidence comparison, a four-stage process, a source screenshot with an explanatory caption, a native comparison table, a genuine graph screenshot, a chart taking most of the canvas, and a spacious conclusion. The twelve slides should share a system but not repeat one card layout.
- **Screenshots:** retain the source's true light background in a clean inset within the dark canvas. Capture at high resolution, crop to a legible evidence region, and keep English captions and source attribution. Do not recolor screenshot contents or replace them with generated UI.
- **Charts:** display an explicit metric, units, legend if needed, and short takeaway. Make factual values editable in PowerPoint; use one accent series and quiet comparison series. Avoid reducing a research paper's full multipanel figure until it becomes unreadable.
- **Table:** limit the visible comparison to about three methods and four meaningful criteria. Keep source-dependent qualifications in concise notes.
- **Conclusion:** one memorable sentence plus two or three compact findings. A bibliography can be combined with the final required slide or sources cited on relevant slides, depending on the agreed twelve-slide structure.

## Production handoff

1. Capture the two actual English source regions described above.
2. Verify each screenshot at presentation scale before placing it.
3. Keep the slide content independent of the visual-reference authors' logos or commercial claims.
4. Use official `anthropics/skills@pptx` guidance for building, file validation, and slide-by-slide visual QA: [SKILL.md](https://github.com/anthropics/skills/blob/main/skills/pptx/SKILL.md).
