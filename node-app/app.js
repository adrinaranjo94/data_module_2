const express = require("express");
const app = express();

app.get("/api/test", (req, res) => {
  res.json({ message: "Hello from Express!" });
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Express server running on port ${PORT}`);
});
