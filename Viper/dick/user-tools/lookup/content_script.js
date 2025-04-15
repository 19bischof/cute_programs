// content_script.js
(function () {
  "use strict";

  const API_URL = "http://127.0.0.1:8000/lookup/";
  // Create the popup element
  const popup = createPopup();

  function createPopup() {
    const popup = document.createElement("div");
    popup.style.position = "absolute";
    popup.style.backgroundColor = "#1e1e1e";
    popup.style.color = "#f5f5f5";
    popup.style.border = "1px solid #444";
    popup.style.borderRadius = "3px";
    popup.style.padding = "5px 10px";
    popup.style.boxShadow = "0 2px 5px rgba(0, 0, 0, 0.2)";
    popup.style.zIndex = "1000";
    popup.style.display = "none";
    popup.style.maxWidth = "300px";
    popup.style.wordWrap = "break-word";
    popup.style.fontSize = "14px";
    document.body.appendChild(popup);
    return popup;
  }

  function showPopup(definition, x, y) {
    // Split definition text into parts based on newlines or numbered list markers
    const parts = definition.split(/\n\n|(?=\d+\.\s)/);
    const container = document.createElement("div");
    container.style.maxHeight = "200px";
    container.style.overflowY = "auto";
    popup.innerHTML = "";
    parts.forEach((part) => {
      const trimmed = part.trim();
      if (trimmed !== "") {
        const p = document.createElement("p");
        p.textContent = trimmed;
        container.appendChild(p);
      }
    });
    popup.appendChild(container);
    popup.style.left = `${x}px`;
    popup.style.top = `${y}px`;
    popup.style.display = "block";
  }

  function hidePopup() {
    popup.style.display = "none";
  }

  async function doubleClickListener(event) {
    const selectedText = window.getSelection().toString().trim().toLowerCase();
    if (selectedText) {
      let definition;
      try {
        const response = await fetch(API_URL + selectedText);
        if (!response.ok) {
          definition = "Definition not found";
        } else {
          const data = await response.json();
          definition = data[selectedText] || "Definition not found.";
        }
      } catch (error) {
        definition = 'Error retrieving definition';
      }
      // Show the popup at the mouse click position
      showPopup(definition, event.pageX, event.pageY);
    }
  }

  function singleClickListener(event) {
    if (!popup.contains(event.target)) {
      hidePopup();
    }
  }

  function registerListeners() {
    console.log("Dictionary Lookup Extension registered.");
    document.addEventListener("dblclick", doubleClickListener);
    document.addEventListener("click", singleClickListener);
  }

  registerListeners();
})();
