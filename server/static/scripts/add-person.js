(function() {
    "use strict";

    var minNameLength = 2;
    var nameValid = false;
    
    $("#nameInput").on("input", function() {
        if ($(this).val().length >= minNameLength && 
            $(this).val().match("[a-zA-Z ]+$")) {
            $(this).removeClass("is-invalid");
            nameValid = true;
        } else {
            $(this).addClass("is-invalid");
            nameValid = false;
        }
    });

    $("#imageForm").on("submit", function(ev) {
        if (!nameValid) {
            ev.preventDefault();
            ev.stopPropagation();
        }
    });
})();