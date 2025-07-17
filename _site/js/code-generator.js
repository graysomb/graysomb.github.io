/* code-generator.js - random code generator logic */
// Sample code snippets for generation
const codeSamples = [
  "for (let i = 0; i < 10; i++) { console.log(i); }",  
  "function greet(name) { return `Hello, ${name}!`; }",  
  "if (x > y) { x = x - y; } else { y = y - x; }",  
  "const square = n => n * n;",  
  "let arr = [1,2,3,4].map(n => n * 2);",  
  "class Person { constructor(name) { this.name = name; } }",  
  "const promise = new Promise((res, rej) => res('done'));",  
  "try { doSomething(); } catch (e) { console.error(e); }"
];

function generateRandomCode() {
  const idx = Math.floor(Math.random() * codeSamples.length);
  return codeSamples[idx];
}

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('generate-btn');
  const output = document.getElementById('code-output');
  if (btn && output) {
    btn.addEventListener('click', () => {
      output.textContent = generateRandomCode();
    });
    // Generate initial code on load
    output.textContent = generateRandomCode();
  }
});