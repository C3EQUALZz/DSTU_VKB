// Generate the separate native Word PDF export script; no GUI is launched here.
const fs = require('fs');
const path = require('path');
const root = path.resolve(__dirname, '..');
const quote = value => JSON.stringify(value);
const source = path.join(root, 'output', 'RAG_Speaking_Notes_EN_RU.docx');
const target = path.join(root, 'output', 'RAG_Speaking_Notes_EN_RU.pdf');
const script = [
  'with timeout of 120 seconds',
  'tell application "Microsoft Word"',
  'activate',
  `open (POSIX file ${quote(source)})`,
  'set notesDoc to active document',
  'if (name of notesDoc) does not contain "RAG_Speaking_Notes_EN_RU" then error "Unexpected document"',
  `set pdfPath to (POSIX file ${quote(target)}) as text`,
  'save as notesDoc file name pdfPath file format format PDF add to recent files false',
  'end tell',
  'end timeout',
  'return "Word speaking notes exported to PDF."',
].join('\n');
fs.writeFileSync(path.join(__dirname, 'office-helper-word.applescript'), script + '\n');
console.log('Generated src/office-helper-word.applescript.');
console.log('If Word asks for folder access, select only this project’s output folder.');
