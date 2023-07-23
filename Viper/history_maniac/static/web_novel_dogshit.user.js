// ==UserScript==
// @name        webnovel - anti bullshit
// @namespace   Violentmonkey Scripts
// @match       https://www.webnovel.com/book/*
// @grant       none
// @version     1.0
// @author      -
// @run-at        document-start
// @description 7/23/2023, 11:51:45 AM
// ==/UserScript==

const clearInts = () => {
    for (let i = 10;i < 10000;i++) {
      clearInterval(i);
    }
    }
    setTimeout(clearInts,1500)
    
    
    
    