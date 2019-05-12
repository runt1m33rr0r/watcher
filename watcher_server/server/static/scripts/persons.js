(function() {
    "use strict";
    
    $(".image button").on("click", function() {
        var image = $("img[src=\"" + $(this).prev().attr("src") + "\"]");

        $.ajax({
            url: $(this).attr("url"),
            method: "DELETE",
            success: function(data) {
                if (data.success == true) {
                    image.parent().remove();
                    showSuccessMessage(data.message);
                } else {
                    showErrorMessage(data.message);
                }
            }
        });
    });

    $(".delete-person").on("click", function() {
        $.ajax({
            url: $(this).attr("url"),
            method: "DELETE",
            success: function(data) {
                if (data.success == true) {
                    window.location.replace("/persons");
                } else {
                    showErrorMessage(data.message);
                }
            }
        });
    });
})();