// ==UserScript==
// @name        history daemon
// @namespace   Violentmonkey Scripts
// @match       https://www.webnovel.com/book/*
// @grant       GM_xmlhttpRequest
// @version     1.0
// @author      -
// @@run-at        document-start
// @description 7/23/2023, 11:22:51 AM
// ==/UserScript==

const register_listener = () => {
    // Function to send a POST request to the FastAPI server
    function sendPostRequest() {
      console.log('sending request')
      const data = {url: window.location.href}
      GM_xmlhttpRequest({
        method: "POST",
        url: "http://localhost:34227/append_history/",
        data: JSON.stringify(data),
        timeout: 3000,
        ontimeout: () => {alert("history server couldn't be reached!")},
        onload: function (response) {
          if (response.status > 400) {
            alert('history server: ', response.statusText, response.responseText)
          }
          console.log(response.responseText);
        },
      });
    }
    sendPostRequest()
    document.addEventListener("keydown", function (e) {
      if (e.ctrlKey  &&  e.altKey && e.key == 'u') {
        sendPostRequest();
      }}) // 'u'
  
    old_href = window.location.href
    function siteChanged() {
      console.debug("check if changed...")
      if (window.location.href === old_href) {
        return
      }
      old_href = window.location.href
      sendPostRequest()
    }
    setTimeout(() => {setInterval(siteChanged, 1000)},5000)
    // Example: Trigger the action when the page loads
    //sendPostRequest();
  }
  register_listener()