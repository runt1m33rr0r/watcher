(function() {
    'use strict';

    $.each($(".nav-link"), function() {
        if ($(this).attr("href") == window.location.pathname) {
            $(this).addClass("active");
        } else {
            $(this).removeClass("active");
        }
    });

    $.each($(".dropdown"), function() {
        var dropdown = $(this)
        
        $.each(dropdown.find(".dropdown-menu .dropdown-item"), function() {
            if ($(this).attr("href") == window.location.pathname) {
                dropdown.addClass("active");
                return false;
            } else {
                dropdown.removeClass("active");
            }
        });
    });

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $("#errorMessage").hide();
    $("#successMessage").hide();
})();

function showMessage(successId, errorId, message) {
    $(".template-message").remove();

    var messageElement = $(successId);
    messageElement = messageElement.clone();
    $("#main").prepend(messageElement);

    messageElement.hide();
    $(errorId).hide();
    
    messageElement.show();
    messageElement.prepend(message);
}

function showSuccessMessage(message) {
    showMessage("#successMessage", "#errorMessage", message);
}

function showErrorMessage(message) {
    showMessage("#errorMessage", "#successMessage", message);
}