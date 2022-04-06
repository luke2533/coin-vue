// Add green red for positive and negative values

function tokenId() {
    var token = document.getElementsByClassName("token");
    for (let i = 0; i < token.length; i++) {
        token[i].setAttribute("id", "token_"+i);
    }
}
window.onload = tokenId();

// Home page

$('#pills-tab a').on('click', function (e) {
    e.preventDefault()
    $(this).tab('show')
})

// Add record page