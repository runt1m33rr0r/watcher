(function() {
    "use strict";

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
        if (document.cookie && document.cookie !== "") {
            var cookies = document.cookie.split(";");
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + "=")) {
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

    var csrftoken = getCookie("csrftoken");
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    function notify(title, content) {
        var notificationClone = $("#templateNotification").clone();
        notificationClone.addClass("notification");
        notificationClone.find(".toast-title").html(title);
        var today = new Date();
        var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
        notificationClone.find(".toast-time").html(time);
        notificationClone.find(".toast-body").html(content);

        $("#notifications").append(notificationClone);
        $(".notification").toast("show");
    }

    function initSocket() {
        return new WebSocket("ws://" + window.location.host + "/notifications");
    }

    var notificationSocket = initSocket();

    notificationSocket.onopen = function() {
        console.log("opened");
    }

    notificationSocket.onmessage = function(e) {
        var data = JSON.parse(e.data);
        var detectionUrl = window.location.protocol + "//" + window.location.host + 
            "/" + data["detection_url"];
        var detectionLink = "<a href=\"" + detectionUrl + "\">Open detection page.</a>"
        
        notify("Detected " + data["person_name"] + " in " + data["city_name"] + ".", detectionLink);
    };

    notificationSocket.onclose = function() {
        console.log("closed");
        notificationSocket = initSocket();
    };

    notificationSocket.onerror = function() {
        console.log("errored");
        notificationSocket = initSocket();
    }
})();

function showMessage(successId, errorId, message) {
    var messageElement = $(successId);
    messageElement = messageElement.clone();
    $("#messages").append(messageElement);

    $(errorId).addClass("d-none");
    messageElement.removeClass("d-none");
    messageElement.find(".message-text").html(message);
}

function showSuccessMessage(message) {
    showMessage("#successMessage", "#errorMessage", message);
}

function showErrorMessage(message) {
    showMessage("#errorMessage", "#successMessage", message);
}