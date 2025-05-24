const express = require('express');
const path = require('path');
const app = express();
const port = 3000;

// Serve static files from the same directory
app.use(express.static(path.join(__dirname)));

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(port, () => {
  console.log(`Retro Terminal app listening at http://localhost:${port}`);
});