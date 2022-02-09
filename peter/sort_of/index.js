canvas = document.getElementById("canvas");
ctx = canvas.getContext("2d");
canvas.width = document.documentElement.clientWidth -20
canvas.height = document.documentElement.clientHeight -20
var count = 0
var span = document.getElementById("span")
var span2 = document.getElementById("span2")
 function Sleep(milliseconds) {
    return new Promise(resolve => setTimeout(resolve, milliseconds));
   }

 class Sort_Arrays {
    constructor() {
        this.margin = 2
        this.width = 3
        
        var length = Math.floor(canvas.width/(this.width+this.margin))
        // length = 100
        this.max = length *0.9
        this.array = new Array(length);
        for (var i = 0; i < this.array.length; i++) {
            this.array[i] = Math.floor(Math.random()*this.max)+1 //makes 0 impossible and max possible (+1)
        }
        this.my_rend = new Renderer()

    }
    shuffle(){
        this.array.sort((a,b)=>{return (Math.random()-0.5)})
    }
    draw(){
        ctx.clearRect(0,0,canvas.width,canvas.height)
        ctx.beginPath()
        var index = 0
        this.array.forEach(n =>{
            ctx.rect((this.width+this.margin)*index,canvas.height,this.width,-n*canvas.height/this.max)


            index +=1

        })
        ctx.fill()
        
        
    }
     
     async delayed_draw(sorted,inserted_i_new,inserted_i_old){
        var index = 0
        await Sleep(16)
        ctx.clearRect(0,0,canvas.width,canvas.height)
        var index = 0
        sorted.forEach( n =>{
            ctx.beginPath()

            if (inserted_i_new == index){
                ctx.fillStyle="red"
            }else{
                ctx.fillStyle = "black"
            }
            ctx.rect((this.width+this.margin)*index,canvas.height,this.width,-n*canvas.height/this.max)
            ctx.fill()


            index +=1

        })
        for(var i = index; i < this.array.length;i++){
            ctx.beginPath()
            if (inserted_i_old+1 == i){
                ctx.fillStyle="yellow"
            }else{
                ctx.fillStyle = "black"
            }
            ctx.rect((this.width+this.margin)*index,canvas.height,this.width,-this.array[i]*canvas.height/this.max)
            ctx.fill()

            index +=1
        }
        return 1
        
    }
     async Insert_Sort(){
        this.my_rend.start_rend()
        this.draw()
        var sorted = new Array()

        for (var i = 0;i < this.array.length;i++){

            for (var k = 0; k < sorted.length;k++){
                if (sorted[k] < this.array[i] ){
                    continue
                }else{
                    break
                }
            }
        sorted.splice(k,0,this.array[i])
        await this.delayed_draw(sorted,k,i)
        }

        this.array = sorted
        
        this.my_rend.display_rend()

    }
}
class Renderer{
    constructor(){
        this.start = 0
    }
    start_rend(){
        this.start = new Date().getTime()

    }
    display_rend(){
        span.innerHTML = "Time: " + (new Date().getTime() - this.start)/1000 +  "s"
        span2.innerHTML ="frames displayed: " + Math.floor((new Date().getTime() - this.start)*0.06) //0.06 because of 60 fps
    }

}
var my_array = new Sort_Arrays()
my_array.Insert_Sort()