# Native Office runtime verification

Verified locally on 2026-11-13 using installed Microsoft PowerPoint and Word. No global security or Accessibility settings were changed.

## PowerPoint: confirmed working API

Primary local source: `/Applications/Microsoft PowerPoint.app/Contents/Resources/PowerPoint.sdef`.

Runtime checks confirmed:

- `save presentation in (POSIX file path) as save as PDF` exports successfully.
- `add effect sequence for shape fx animation type fade trigger on page click` creates a native entrance effect.
- `trigger with previous` groups the remaining objects of an explanatory stage into the same click.
- `set duration of timing of effect to 0.3` works.
- Fade slide transitions of 0.35 seconds with manual advancement work.
- Generated shape names are preserved and can be used through `shape "name" of slide`.
- The slideshow-window property is spelled **`slideshow view`**, not `slide show view`.

The original `repeat with slideRef in slides of presentation` collection iteration stalled. Indexed iteration resolved it: `repeat with slideIndex from 1 to 12`, then `set slideRef to slide slideIndex of presentation`. A similar collection loop over presentations returned AppleScript error -2763. Prefer indexed references.

The generic `delete effect` command returned parameter error -50. Clean repeated builds were produced by closing only this task's own active presentation without saving and reopening the generated base before adding effects.

## Final presentation outputs

The native animated presentation and static PDF were generated from **`output/RAG_for_Secure_Code_base_v4.pptx`**, including the final `Architecture` correction on slide 2 and the revised `Both versions must be classified correctly` explanation on slide 6.

- `output/RAG_for_Secure_Code.pptx`
- `output/RAG_for_Secure_Code.pdf`

The deck contains twelve slides. Native entrance effects were added on slides 1, 4, 5, 6, 7, 8, 10 and 11; all twelve slides have native Fade transitions. The manifest supplies eighteen explanatory click groups.

The repeatable generator `src/office.cjs` preserves the parent's v4 path, indexed-loop fix, and correct slideshow-property spelling. Word export was separated so its folder-access prompt cannot stall the presentation build. The successful concrete native script is also retained as `src/office-helper-animate-v4.applescript`.

## Playback proof

The saved final file was played in native PowerPoint:

- Slide 4 initial state hides the animated pipeline/code and retains static titles and explanation.
- One Next command reveals the preparation pipeline while the show remains on the same slide (`current show position` 1 → 1 in a slide-4-only test range).
- Slide 8 initial state hides the agent/tool diagram and code.
- One Next command reveals AG2 agents while the remaining stages stay hidden.

Actual screen captures:

- `/private/tmp/rag-animation-4-initial.png`
- `/private/tmp/rag-animation-4-step1.png`
- `/private/tmp/rag-animation-8-initial.png`
- `/private/tmp/rag-animation-8-step1-late.png`

Immediate captures occasionally showed incomplete macOS compositing; later captures showed the correct settled state. The final file was saved before temporary playback-range testing. The open application's settings were restored to all slides, starting at 1 and ending at 12, without resaving the tests over the final file. The parent independently verified that the saved file is not limited to a test range.

## Word export and document preview

Primary local source: `/Applications/Microsoft Word.app/Contents/Resources/Word.sdef`.

Word opened `output/RAG_Speaking_Notes_EN_RU.docx` correctly. The first page was visually inspected in Word: author, group, English text, Russian translation and cue formatting rendered correctly. Word reported sixteen pages.

Initial PDF-export attempts timed out because Word displayed a modal **Grant Access** request for the exact workspace `output` directory. This was an application sandbox prompt, not malformed DOCX content. Repeated save retries should be avoided because they can queue duplicate dialogs.

After the narrow folder-access workflow was resolved, the export completed successfully and returned `Word PDF saved`:

- **`output/RAG_Speaking_Notes_EN_RU.pdf` — 16 pages, approximately 141 KB.**

The successful invocation uses an HFS path derived through `(POSIX file path) as text` and `save as active document file name pdfPath file format format PDF`. The reusable path-independent generator is **`src/office-helper-word.cjs`**. Run it to write `src/office-helper-word.applescript`, then execute that generated script with the required GUI permission. Select only this project's output folder if Word presents the native access dialog.

System Events reported `UI elements enabled = true`; no global Accessibility switch was enabled. Only the exact task output directory was authorized. Parent-side rendering and visual QA of all sixteen PDF pages follows the successful export.

## Files to keep in source control

- Keep `src/office.cjs` and `src/office-helper-word.cjs` as the reproducible script generators.
- Keep this runtime report.
- Generated `.applescript` files, one-off status/transition/playback probes, old base exports and temporary screen captures are diagnostics. They are not required source files and should be excluded from the commit. The final deliverables are the canonical PPTX, DOCX and PDFs selected by the parent.
