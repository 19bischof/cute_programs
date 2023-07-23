// ==UserScript==
// @name        history daemon static
// @namespace   Violentmonkey Scripts
// @match       https://www.webnovel.com/book/*
// @grant       GM_xmlhttpRequest
// @version     1.0
// @author      -
// @run-at      document-end
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
  
    proof_that_interval_works = false
    old_href = window.location.href
    function siteChanged() {
      if (Date.now() - last_time > 2000) {
  
        proof_that_interval_works = true
      }
      console.debug("check if changed...")
      if (window.location.href === old_href) {
        return
      }
      old_href = window.location.href
      sendPostRequest()
    }
  
    interval_id = undefined
    last_time = undefined
    function interval_proof(e) {
      console.debug("proofing...")
      if (proof_that_interval_works) {
        document.removeEventListener("scroll",interval_proof)
        return
      }
      if (Date.now() - last_time < 4400) {
        return
      }
      last_time = Date.now()
      if (interval_id) {
        clearInterval(interval_id)
      }
      console.debug("new interval")
      interval_id = setInterval(siteChanged, 1000)
      interval_set_time = Date.now()
    }
    document.addEventListener("scroll", interval_proof)
  
    // Example: Trigger the action when the page loads
    //sendPostRequest();
  }
  register_listener()