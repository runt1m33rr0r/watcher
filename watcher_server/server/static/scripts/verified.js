(function() {
    'use strict';

    if (window.location.pathname == "/verified") {
        $("#allLink").addClass("font-weight-bold");
    }

    $(".delete-button").on("click", function() {
        $.ajax({
            url: "/verified",
            method: "DELETE",
            data: JSON.stringify({
                id: $(this).attr("detection"),
            }),
            success: function(data) {
                location.reload();
            }
        });
    });
})();