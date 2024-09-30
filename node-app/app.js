const express = require("express");
const bodyParser = require("body-parser");

const app = express();
const PORT = 3000;

// Middleware
app.use(bodyParser.json());
app.use(express.static("public"));

// Lista de tareas (en memoria)
let todoList = [];

// Ruta principal para servir el HTML
app.get("/", (req, res) => {
  res.sendFile(__dirname + "/public/index.html");
});

// API: Obtener la lista de tareas
app.get("/api/todos", (req, res) => {
  res.status(200).json(todoList);
});

// API: Agregar una nueva tarea
app.post("/api/add", (req, res) => {
  const { task } = req.body;
  if (task) {
    todoList.push(task);
    return res.status(201).json({ message: "Task added successfully!" });
  }
  return res.status(400).json({ message: "Task is required!" });
});

// API: Eliminar una tarea
app.delete("/api/delete/:taskIndex", (req, res) => {
  const taskIndex = parseInt(req.params.taskIndex, 10);
  if (taskIndex >= 0 && taskIndex < todoList.length) {
    todoList.splice(taskIndex, 1);
    return res.status(200).json({ message: "Task deleted successfully!" });
  }
  return res.status(404).json({ message: "Task not found!" });
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
