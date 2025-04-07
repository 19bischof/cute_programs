// ==UserScript==
// @name        Dictionary Lookup with Popup
// @namespace   Violentmonkey Scripts
// @match       https://www.royalroad.com/*
// @grant       none
// @version     1.7
// @author      -
// @description  Dictionary lookup with a nice popup menu
// ==/UserScript==

(async function () {
    "use strict";
  
    const DICTIONARY_URL = "http://127.0.0.1:8000/lookup/";
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
  
    document.addEventListener("dblclick", async function (event) {
      const selectedText = window.getSelection().toString().trim().toLowerCase();
      if (selectedText) {
        try {
          const response = await fetch(DICTIONARY_URL + selectedText);
          let definition;
          if (!response.ok) {
            definition = "Definition not found";
          } else {
            const data = await response.json();
            definition = data[selectedText] || "Definition not found.";
          }
          // Show the popup at the mouse position
          showPopup(definition, event.pageX, event.pageY);
        } catch (error) {
          console.error("Error fetching definition:", error);
          hidePopup();
        }
      }
    });
  
    // Hide the popup when clicking anywhere else
    document.addEventListener("click", function (event) {
      if (!popup.contains(event.target)) {
        hidePopup();
      }
    });
  })();
  