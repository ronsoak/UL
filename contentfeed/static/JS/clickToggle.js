function clickToggle() {
    var c = document.getElementById("dropmenu");
    var l = document.getElementById("droplink");
    if(c.style.display == "block")
    {
        c.style.display = "none"
        l.blur();
    }
    else{
        c.style.display = "block"
    }

}