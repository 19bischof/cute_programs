let cont = document.getElementsByTagName("grid-container")[0]

function inject_tiles(count) {
    for (i = 0; i < count; i++) {
        tile = document.createElement('grid-item')
        tile.innerHTML = "testword"
        tile.style.color = '#FFFF00'
        cont.appendChild(tile)
    }
}
inject_tiles(24)

function dealer(event_item) {
    num = Array.from(cont.children).indexOf(event_item.target)
    console.log(num)
}


[...document.getElementsByTagName("grid-item")].forEach(element => {
    element.addEventListener('click', dealer)
});