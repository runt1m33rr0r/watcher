(function() {
    'use strict';

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

    var fileImage = $("#fileImage");
    var processed = fileImage.attr("processed")
    if (processed != "") {
        var base64 = "data:image/jpeg;base64," + processed;
        fileImage.attr("src", base64);
    }
})();