browser.storage.local.remove("data");

function _getBaseForms(word, endings) {
  const forms = [word];

  endings.forEach((ending) => {
    if (ending instanceof RegExp) {
      if (new RegExp(ending.source + "$").test(word)) {
        forms.push(
          word.slice(0, -1 * ending.source.replaceAll("?", "").length)
        );
      }
      return;
    }
    if (word.endsWith(ending)) {
      forms.push(word.slice(0, -1 * ending.length));
    }
  });
  return forms;
}
function getEnglishBaseForms(word) {
  const endings = [
    "s",
    "es",
    "d",
    "ed",
    "ing",
    "ment",
    "ness",
    "ly",
    /.ed/,
    /.ing/,
  ];

  return _getBaseForms(word, endings);
}

function getFrenchBaseForms(word) {
  const frenchEndings = [
    // Low-impact inflections
    "s", // plural
    "es", // feminine plural
    "e", // feminine
    "ée", // past participle (feminine)
    "ées", // past participle (fem. plural)
    "é", // past participle (masculine)
    "és", // past participle (masc. plural)

    // Participles
    "ant", // present participle (e.g. mangeant → manger)
    "ante", // feminine form
    "ants", // plural
    "antes", // feminine plural

    // Nominalizations
    "ment", // from verbs (e.g. jugement → juger)
    "ement", // e.g. avancement → avancer
    "issement", // e.g. établissement → établir

    // Abstract/derived noun forms
    "tion", // e.g. réalisation → réaliser
    "ations", // plural
    "éité", // e.g. humanité

    // Regex fallbacks
    /.é.e?s?/, // catch-all for participle/adj endings
    /.ant.e?s?/, // participle/adj variants
  ];

  return _getBaseForms(word, frenchEndings);
}

async function loadDictionary(key, url) {
  let { [key]: data } = await browser.storage.local.get(key);

  if (!data) {
    const response = await fetch(url);
    if (!response.ok) {
      console.error(`failed to fetch dictionary ${key} :(`);
      return;
    }

    data = await response.json();

    await browser.storage.local.set({
      [key]: data,
    });

    console.log(`dictionary file ${key} downloaded and stored`);
  }

  console.log(`dictionary ${key} loaded into memory :-)`);

  return data;
}
let en_webster,
  fr_vicon = [{}, {}];

(async () => {
  en_webster = await loadDictionary(
    "en_webster",
    "https://raw.githubusercontent.com/matthewreagan/WebstersEnglishDictionary/refs/heads/master/dictionary.json"
  );
  fr_vicon = await loadDictionary(
    "fr_Vicon",
    "https://raw.githubusercontent.com/19bischof/dictionaries/refs/heads/main/Vicon%20French-English%20Dictionary.json"
  );
})();

browser.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "lookup") {
    const word = message.word.toLowerCase();
    console.log("looking up:", word);
    let definition = "Definition not found.";

    const en_candidates = getEnglishBaseForms(word);
    for (const candidate of en_candidates) {
      if (en_webster[candidate]) {
        console.log("found definition for:", candidate);
        definition = en_webster[candidate];
        break;
      }
    }


    const fr_canditates = getFrenchBaseForms(word);
    for (const candidate of fr_canditates) {
      if (fr_vicon[candidate]) {
        console.log("found definition for:", candidate);
        definition = fr_vicon[candidate];
        break;
      }
    }
    sendResponse({ definition });
  }
});
