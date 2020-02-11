window.addEventListener('load', function () {

    function showHide() {
        var x = document.getElementById("options");
        if (x.style.display === "none") {
            x.style.display = "block";
        } else {
            x.style.display = "none";
        }
    }

    var divButton = document.getElementById("option_toggle");
    divButton.onclick = showHide;
})