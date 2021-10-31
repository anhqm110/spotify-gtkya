let likeCount = 0;
let dislikeCount = 0;


function incrementLike() {
    likeCount++;
    if (likeCount >= 5 && dislikeCount >= 5) {
        window.location.href = "result_page.html"
    }
}

function incrementDislike() {
    dislikeCount++;
    if (likeCount >= 5 && dislikeCount >= 5) {
        window.location.href = "result_page.html"
    }
}