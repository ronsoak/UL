function searchToggle() {
    var x = document.getElementById("searchbar");
    var y = document.getElementById("sbuttS");
    var z = document.getElementById("sbuttX");
    if(x.style.display !== "block" )
    {
        x.style.display = "block"
        y.style.visibility = "hidden"
        z.style.visibility = "visible"
    }
    else
    {
        x.style.display = "none"
        y.style.visibility = "visible"
        z.style.visibility = "hidden"
    }
};
