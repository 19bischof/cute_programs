function getBaseForms(word) {
  const endings = ['s','es','d','ed','ing','ment'];
  const forms = [word];

  endings.forEach(ending =>
    word.endsWith(ending) && forms.push(word.slice(0, -1 * ending.length))
  );

  return forms;
}

let dictionary = {};

// Load the JSON once when the extension starts
fetch(browser.runtime.getURL("dictionary.json"))
  .then(response => response.json())
  .then(data => {
    dictionary = data;
    console.log("Dictionary loaded into memory");
  });


browser.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "lookup") {
    const word = message.word.toLowerCase();
    const candidates = getBaseForms(word);
    let definition = "Definition not found.";

    for (const candidate of candidates) {
      if (dictionary[candidate]) {
        definition = dictionary[candidate];
        break;
      }
    }

    sendResponse({ definition });
  }
  return true; // ensures the sendResponse stays open for async
});