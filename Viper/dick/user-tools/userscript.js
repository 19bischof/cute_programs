// ==UserScript==
// @name        Dictionary Lookup with Popup
// @namespace   What a day to be alive
// @match       https://*/*
// @grant       none
// @version     1.7
// @author      -
// @description  Dictionary lookup with a nice popup on double click
// ==/UserScript==

(async function () {
  "use strict";

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

  function postRender(text) {
    let parts = text.split(" -- ");
    let output = parts[0];
    for (let i = 1; i < parts.length; i++) {
      output +=
        '<br><i style="all: unset; font-style:italic; display:inline-block; margin: 5px 0;"> -- ' +
        parts[i] +
        " </i>";
    }
    return output;
  }

  function showPopup(definition, x, y) {
    const parts = definition.split(/\n\n|(?=\d+\.\s)/);
    const pureParts = [];
    parts.forEach((part, i) => {
      if (i == 0){
        pureParts.push(part)
        return
      }
      if (/\d+\.*\s*$/.test(part)) {
        // begins -> 1 Sam. iii. 12.\n\n ( prevents 1\n2.\n \n)
        pureParts[pureParts.length - 1] += part;
        return;
      }
      pureParts.push(part);
    });

    const container = document.createElement("div");
    container.style.maxHeight = "200px";
    container.style.overflowY = "auto";
    container.style.display = "flex";
    container.style.flexDirection = "column";
    container.style.gap = "20px";

    popup.innerHTML = "";

    pureParts.forEach((part) => {
      const trimmed = part.trim();
      if (trimmed !== "") {
        const p = document.createElement("p");
        p.style.all = "unset";
        p.innerHTML = postRender(trimmed);
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
      browser.runtime
        .sendMessage({ action: "lookup", word: selectedText })
        .then((response) => {
          showPopup(response.definition, event.pageX, event.pageY);
        })
        .catch((error) => {
          showPopup("Error :-(", event.pageX, event.pageY);
          console.debug(error);
        });
    }
  }

  function singleClickListener(event) {
    if (!popup.contains(event.target)) {
      hidePopup();
    }
  }

  function registerListeners() {
    console.debug("registered ;-0");
    document.addEventListener("dblclick", doubleClickListener);

    // Hide the popup when clicking anywhere else
    document.addEventListener("click", singleClickListener);
  }

  registerListeners();
})();
