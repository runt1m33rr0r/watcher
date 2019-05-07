(function() {
    'use strict';
    
    $(".false-button").on("click", function() {
        $.ajax({
            url: "/detections",
            method: "DELETE",
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            data: JSON.stringify({
                id: $(this).attr("detection"),
            }),
            success: function(data) {
                location.reload();
            }
        });
    });
})();