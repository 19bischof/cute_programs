// canvas.height = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0)
// canvas.width = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0)
// canvas.height = window.innerHeight
// canvas.width = window.innerWidth

class Clock {
    constructor(x, y, radius, time_diff) {
        this.x = x;
        this.y = y;
        this.radius = radius;
        this.time_diff = time_diff;
        this.seconds = new Clock_hands(this.radius * 0.9, 5, "red");
        this.minutes = new Clock_hands(this.radius * 0.9, 10, "black");
        this.hours = new Clock_hands(this.radius * 0.7, 20, "black");
        this.Clock_hands = [this.seconds, this.minutes, this.hours];
        this.face = new Image();
        this.face.src = "clock.png";
        this.get_date = () => {
            return new Date(new Date().getTime() + this.time_diff);
        };
        this.audio_el = document.getElementById("ticktock");
        this.audio_file = "tick.mp3";
    }

    calc_angles() {
        this.date = this.get_date();
        this.seconds.angle = (this.date.getSeconds() / 60) * 2 * Math.PI;
        this.minutes.angle = (this.date.getMinutes() / 60) * 2 * Math.PI;
        this.hours.angle =
            (this.date.getHours() / 12) * 2 * Math.PI +
            this.minutes.angle / 12 +
            this.seconds.angle / (60 * 12); //for continuous motion on hour hand

        // because hands are at 12:00 at 3:00
        this.seconds.angle = this.seconds.angle - Math.PI / 2;
        this.minutes.angle = this.minutes.angle - Math.PI / 2;
        this.hours.angle = this.hours.angle - Math.PI / 2;
    }
    draw(ctx) {
        ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
        ctx.drawImage(
            this.face,
            this.x - this.radius,
            this.y - this.radius,
            this.radius * 2,
            this.radius * 2
        );
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius * 0.04, 0, 2 * Math.PI);
        ctx.fill();
        ctx.stroke();
        this.Clock_hands.forEach((e) => {
            ctx.translate;
            ctx.translate(this.x, this.y);
            ctx.beginPath();
            ctx.rotate(e.angle);
            ctx.rect(0, 0 - e.width / 2, e.height, e.width);
            ctx.fillStyle = e.color;
            ctx.fill();
            ctx.rotate(2 * Math.PI - e.angle);

            ctx.translate(-this.x, -this.y);
        });
    }
    audio() {
        // console.log(this.audio_file);
        if (this.audio_file == "tock.mp3") {
            this.audio_file = "tick.mp3";
        } else {
            this.audio_file = "tock.mp3";
        }
        this.audio_el.src = this.audio_file;
        this.audio_el.play();
    }
}
class Clock_hands {
    constructor(height, width, color) {
        this.height = height;
        this.width = width;
        this.angle = 0;
        this.color = color;
    }
}
class Renderer {
    constructor(time_diff) {
        this.time_diff = time_diff;
        this.canvas = document.getElementById("canvas");
        this.update_canvas_and_clock();
        this.get_date = () => {
            return new Date(new Date().getTime() + this.time_diff);
        };

        this.previous_seconds = -1; //if current second != prev_seconds => update()
        window.onresize = this.update_canvas_and_clock.bind(this);
    }
    event_loop() {
        let d = this.get_date();
        let cur_seconds = d.getSeconds();
        if (cur_seconds != this.previous_seconds) {
            this.previous_seconds = cur_seconds;
            this.do_update();
        }

        setTimeout(this.event_loop.bind(this), 1000 - d.getMilliseconds());
    }

    do_update() {
        this.clock.audio();
        this.clock.calc_angles();
        this.clock.draw(this.ctx);
    }
    update_canvas_and_clock() {
        this.canvas.height = document.documentElement.clientHeight;
        this.canvas.width = document.documentElement.clientWidth;
        this.ctx = this.canvas.getContext("2d");
        let clock_radius = 0;
        if (canvas.height > canvas.width) {
            clock_radius = canvas.width / 2;
        } else {
            clock_radius = canvas.height / 2;
        }
        this.clock = new Clock(
            this.ctx.canvas.width / 2,
            this.ctx.canvas.height / 2,
            clock_radius,
            this.time_diff
        );
    }
}

function online_time() {
    let machine_time = new Date();
    fetch("http://worldtimeapi.org/api/timezone/Europe/Berlin", { cache: 'no-store' })  //no-store,so the browser always fetches from server and not cache
        .then((value) => {
            return value.json();
        })
        .then((data) => {
            let real_utc_datetime = new Date(data["utc_datetime"]);
            console.log("fetched time:", real_utc_datetime.getSeconds())
            console.log("local time:", machine_time.getSeconds())
            let avg_ping = 30
            let time_diff = -avg_ping + (real_utc_datetime - machine_time); //add time_diff to all timings
            if (Math.abs(time_diff) < 30) {
                time_diff = 0;
            }
            let pronoun = "behind";
            if (time_diff < 0) {
                pronoun = "ahead";
            }
            document.getElementById("local_time_diff").textContent =
                "The local Time is " +
                pronoun +
                " by " +
                Math.abs(time_diff / 1000)
                    .toFixed(2)
                    .toString() +
                " seconds!";
            return time_diff;
        })
        .then((time_diff) => {
            var my_render = new Renderer(time_diff);
            my_render.event_loop();
        });
}
online_time();
