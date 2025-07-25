import { loadPyodide } from "https://cdn.jsdelivr.net/pyodide/v0.23.4/full/pyodide.mjs";

async function initPyodide() {
  return await loadPyodide({
    indexURL: "https://cdn.jsdelivr.net/pyodide/v0.23.4/full/"
  });
}

window.pyodide = await initPyodide();

// load the Python module into Pyodide's virtual filesystem
{
  const resp = await fetch("quine_ast_liv_0.py");
  const text = await resp.text();
  window.pyodide.FS.writeFile("quine_ast_liv_0.py", text);
}

const generateBtn = document.getElementById("generate-btn");
const output = document.getElementById("output");

generateBtn.addEventListener("click", async () => {
  const code = `
import ast
from quine_ast_liv_0 import generate_random_ast
node = generate_random_ast(3)
ast.unparse(node)
`;
  const result = await window.pyodide.runPythonAsync(code);
  output.textContent = result;
});