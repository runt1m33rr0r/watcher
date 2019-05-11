(function() {
    'use strict';
    
    $(".image button").on("click", function() {
        var image = $("img[src=\"" + $(this).prev().attr("src") + "\"]");

        $.ajax({
            url: $(this).attr("url"),
            method: "DELETE",
            success: function(data) {
                if (data.success == true) {
                    image.remove();
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
                    location.reload();
                } else {
                    showErrorMessage(data.message);
                }
            }
        });
    });
})();