var canvas = document.getElementById("canvas");
// canvas.height = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0)
// canvas.width = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0)
// canvas.height = window.innerHeight
// canvas.width = window.innerWidth
canvas.height = document.documentElement.clientHeight
canvas.width = document.documentElement.clientWidth
var ctx = canvas.getContext('2d');

class Clock {

    constructor(x, y, radius) {
        this.x = x
        this.y = y
        this.radius = radius
        this.seconds = new Clock_hands(this.radius * 0.9, 5, "red")
        this.minutes = new Clock_hands(this.radius * 0.9, 10, "black")
        this.hours = new Clock_hands(this.radius * 0.7, 20, "black")
        this.Clock_hands = [this.seconds, this.minutes, this.hours]
        this.face = new Image()
        this.face.src = "clock.png"
        this.date = new Date()
    }

    calc_angles() {
        this.date = new Date()
        this.seconds.angle = this.date.getSeconds() / 60 * 2 * Math.PI
        this.minutes.angle = this.date.getMinutes() / 60 * 2 * Math.PI
        this.hours.angle = this.date.getHours() / 12 * 2 * Math.PI + this.minutes.angle / 12 //for continuous motin on hour hand

        // because hands are at 12:00 at 3:00
        this.seconds.angle = this.seconds.angle - Math.PI / 2
        this.minutes.angle = this.minutes.angle - Math.PI / 2
        this.hours.angle = this.hours.angle - Math.PI / 2
    }
    draw() {
        ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height)
        ctx.drawImage(this.face, this.x - this.radius, this.y - this.radius, this.radius * 2, this.radius * 2)
        ctx.beginPath()
        ctx.arc(this.x, this.y, this.radius * 0.04, 0, 2 * Math.PI)
        ctx.fill()
        ctx.stroke()
        this.Clock_hands.forEach(e => {
            ctx.translate(this.x, this.y)
            ctx.beginPath()
            ctx.rotate(e.angle)
            ctx.rect(0, 0 - e.width / 2, e.height, e.width)
            ctx.fillStyle = e.color
            ctx.fill()
            ctx.rotate(2 * Math.PI - e.angle)

            ctx.translate(-this.x, -this.y)
        })
    }

}
class Clock_hands {
    constructor(height, width, color) {
        this.height = height
        this.width = width
        this.angle = 0
        this.color = color
    }

}
class Renderer {

    constructor(canvas, ctx, clock) {

        this.canvas = canvas
        this.ctx = ctx
        this.clock = clock



    }

    update() {
        this.clock.calc_angles()
        this.clock.draw()


    }
}
if (ctx.canvas.height > ctx.canvas.width) {
    clock_radius = ctx.canvas.width / 2
} else {
    clock_radius = ctx.canvas.height / 2
}
var clock = new Clock(ctx.canvas.width / 2, ctx.canvas.height / 2, clock_radius)
var renderer = new Renderer(canvas, ctx, clock);



setInterval(renderer.update, 1000)