$("#open-button").css("display", "none");

$("#close-button").click(function(e) {
    e.preventDefault();

    $("#sidebar").css("display", "none");
    $("#open-button").css("display", "inline-block");
});

$("#open-button").click(function(e) {
    e.preventDefault();

    $("#sidebar").css("display", "inline-block");
    $("#open-button").css("display", "none");
});