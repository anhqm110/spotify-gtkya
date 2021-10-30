var likeCounter = 0;
var dislikeCounter = 0;


function incrementLike() {
    likeCounter++
    bar_percent = document.getElementById("my_completion_bar").style.width;
    bar_width = "";
    
    for (let i=0; i < (bar_percent.length - 1); i++) {
        bar_width = bar_percent[i];
    }
    if (parseInt(bar_width) < 100){
        incrementProgressBar(bar_width)
    }
    console.log(likeCounter)
}

function incrementDislike() {
    dislikeCounter++
    console.log(dislikeCounter)
}

function incrementProgressBar(bar_width) {
    bar_percent = document.getElementById("my_completion_bar").style.width;

    if (bar_percent != "1%") {
        new_bar_width = 10 + parseInt(bar_width);
        document.getElementById("my_completion_bar").style.width = "new_bar_width" + "%";
    }
    else {
        document.getElementById("my_completion_bar").style.width = "10%";
    }
    console.log(bar_width)
   
    console.log(bar_percent)

}