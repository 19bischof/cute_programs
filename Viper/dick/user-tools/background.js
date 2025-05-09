function getBaseForms(word) {
  const endings = ["s", "es", "d", "ed", "ing", "ment", "ness"];
  const forms = [word];

  endings.forEach(
    (ending) =>
      word.endsWith(ending) && forms.push(word.slice(0, -1 * ending.length))
  );

  return forms;
}

let dictionary = {};

async function loadDictionary() {
  let { data } = await browser.storage.local.get("data");

  if (!data) {
    const response = await fetch(
      "https://raw.githubusercontent.com/matthewreagan/WebstersEnglishDictionary/refs/heads/master/dictionary.json"
    );
    if (!response.ok) {
      console.error("failed to fetch dictionary :(");
      return;
    }

    data = await response.json();

    await browser.storage.local.set({
      data,
    });

    console.log("dictionary file downloaded and stored");
  }

  dictionary = data;
  console.log("dictionary loaded into memory :-)");
}

loadDictionary();

browser.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "lookup") {
    const word = message.word.toLowerCase();
    console.log("looking up:", word);
    const candidates = getBaseForms(word);
    let definition = "Definition not found.";

    for (const candidate of candidates) {
      if (dictionary[candidate]) {
        console.log("found definition for:", candidate);
        definition = dictionary[candidate];
        break;
      }
    }

    sendResponse({ definition });
  }
});
