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

    $(".modal-button").on("click", function() {
        var url = $(this).attr("url");

        $("#deleteModal .modal-footer .btn-danger").on("click", function() {
            $.ajax({
                url: url,
                method: "DELETE",
                success: function(data) {
                    if (data.success == true) {
                        window.location.replace("/persons/modify");
                    } else {
                        showErrorMessage(data.message);
                    }
                }
            });
        });
    });
})();