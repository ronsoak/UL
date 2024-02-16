window.addEventListener('scroll', function() {
    let scroll = window.scrollY;
    var t1 = document.getElementById("t1")
    var t2 = document.getElementById("titleText")
    if (scroll < 400) {
        t2.setAttribute('data-title','RECONNECT');
        t1.style.display = "none";

    }
    else {
        t2.setAttribute('data-title','RE');
        t1.style.display = "none";
    }
});