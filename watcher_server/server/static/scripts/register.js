(function() {
    "use strict";

    var minUsernameLength = 6;
    var minPasswordLength = 6;
    var maxPasswordLength = 30;
    var usernameValid = false;
    var passwordValid = false;
    
    $("#userInput").on("input", function() {
        if ($(this).val().length >= minUsernameLength && 
            $(this).val().match("^[A-z0-9]+$")) {
            $(this).removeClass("is-invalid");
            usernameValid = true;
        } else {
            $(this).addClass("is-invalid");
            usernameValid = false;
        }
    });

    function isPasswordValid(password) {
        if (password.length >= minPasswordLength && 
            password.length <= maxPasswordLength) {
            return true;
        } else {
            return false;
        }
    }

    function validateRepeatPassword() {
        if ($("#repeatPassword").val() == $("#inputPassword").val() &&
            isPasswordValid($("#repeatPassword").val())) {
            $("#repeatPassword").removeClass("is-invalid");
            passwordValid = true;
        } else {
            $("#repeatPassword").addClass("is-invalid");
            passwordValid = false;
        }
    }

    $("#inputPassword").on("input", function() {
        if (isPasswordValid($(this).val())) {
            $(this).removeClass("is-invalid");
        } else {
            $(this).addClass("is-invalid");
        }

        validateRepeatPassword();
    });

    $("#repeatPassword").on("input", function() {
        validateRepeatPassword();
    });

    $("form").on("submit", function(ev) {
        if (!usernameValid || !passwordValid) {
            ev.preventDefault();
            ev.stopPropagation();
        }
    });
})();