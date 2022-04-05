function tokenId() {
    var token = document.getElementsByClassName("token");
    for (let i = 0; i < token.length; i++) {
        token[i].setAttribute("id", "token_"+i);
    }
}
window.onload = tokenId();

// Home page

$(function () {
    $('#myTab li:last-child a').tab('show')
})

// Add record page