var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");
canvas.width = document.documentElement.clientWidth
canvas.height = document.documentElement.clientHeight
canvas.height = window.innerHeight
canvas.width = window.innerWidth
var sprites = new Array(8)
var xPos = 0, yPos = canvas.height/2
var sprite_index = 0
var my_image = new Image()
my_image.src = "sprites/first.png"      //to get width and height, no other use
var sprite_height
var sprite_width
my_image.onload = () => {    
    sprite_width = my_image.width *2
    sprite_height = my_image.height * 2
    yPos = yPos - sprite_height / 2
}

for (var i = 0; i < 8; i++) {
    sprites[i] = new Image()
}
sprites[0].src = "first.png"
sprites[1].src = "second.png"
sprites[2].src = "third.png"
sprites[3].src = "fourth.png"
sprites[4].src = "fifth.png"
sprites[5].src = "sixth.png"
sprites[6].src = "seventh.png"
sprites[7].src = "eigth.png"


function render() {
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    if (xPos + sprite_width > canvas.width) {
        ctx.drawImage(sprites[Math.floor(sprite_index) % 8],xPos - canvas.width,yPos,sprite_width,sprite_height)
    }
    ctx.drawImage(sprites[Math.floor(sprite_index) % 8],xPos,yPos,sprite_width,sprite_height)
}
function update() {
    render()
    xPos = xPos + 4
    if (xPos >= canvas.width) {
        xPos = 0
    }
    
    sprite_index = sprite_index + 0.04
    
}

setInterval(update,16.67)