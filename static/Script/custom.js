setTimeout(function () {
    $('.messages').each(function () {
        this.style.display = "none"
        this.style.opacity = 0
    })
}, 3000);   

try{
    var close = document.getElementsByClassName("closebtn");
    close[0].onclick = function () {
        var div = this.parentElement;
        console.log(div)
        div.style.opacity = "0";
        setTimeout(function () { div.style.display = "none"; }, 600);
    }
}catch{

}