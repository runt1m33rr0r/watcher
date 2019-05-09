(function() {
    'use strict';

    if (window.location.pathname == "/detections") {
        $("#allLink").addClass("font-weight-bold");
    }
    
    $(".false-button").on("click", function() {
        $.ajax({
            url: "/detections",
            method: "DELETE",
            data: JSON.stringify({
                id: $(this).attr("detection"),
            }),
            success: function(data) {
                location.reload();
            }
        });
    });

    $(".accurate-button").on("click", function() {
        $.ajax({
            url: "/verified",
            method: "POST",
            data: JSON.stringify({
                id: $(this).attr("detection"),
            }),
            success: function(data) {
                location.reload();
            }
        });
    });
})();