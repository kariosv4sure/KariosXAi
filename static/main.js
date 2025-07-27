// static/main.js

document.addEventListener("DOMContentLoaded", () => {
  const textarea = document.querySelector("textarea");

  // Auto-expand textarea height
  textarea.addEventListener("input", () => {
    textarea.style.height = "auto";
    textarea.style.height = `${textarea.scrollHeight}px`;
  });
});
