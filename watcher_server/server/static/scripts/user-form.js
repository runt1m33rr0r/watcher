(function() {
    "use strict";

    var usernameValid = false;
    var passwordValid = false;

    function validateUsername() {
        var userInput = $("#userInput");

        if (userInput.val().match("^[a-z0-9]+$") || userInput.val().length == 0) {
            userInput.removeClass("is-invalid");
            usernameValid = true;
        } else {
            userInput.addClass("is-invalid");
            usernameValid = false;
        }
    }
    
    $("#userInput").on("input", function() {
        validateUsername();
    });

    function validateRepeatPassword() {
        if ($("#repeatPassword").val() == $("#inputPassword").val()) {
            $("#repeatPassword").removeClass("is-invalid");
            passwordValid = true;
        } else {
            $("#repeatPassword").addClass("is-invalid");
            passwordValid = false;
        }
    }

    $("#inputPassword").on("input", function() {
        validateRepeatPassword();
    });

    $("#repeatPassword").on("input", function() {
        validateRepeatPassword();
    });

    $("form").on("submit", function(ev) {
        if (!usernameValid || !passwordValid) {
            console.log('prevent');
            ev.preventDefault();
            ev.stopPropagation();
        }
    });

    validateUsername();
    validateRepeatPassword();
})();