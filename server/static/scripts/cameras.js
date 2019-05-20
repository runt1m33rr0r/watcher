(function() {
    "use strict";

    $(".modal-button").on("click", function() {
        var url = $(this).attr("url");

        $("#deleteModal .modal-footer .btn-danger").on("click", function() {
            $.ajax({
                url: url,
                method: "DELETE",
                success: function(data) {
                    if (data.success == true) {
                        window.location.replace("/cameras");
                    } else {
                        showErrorMessage(data.message);
                    }
                }
            });
        });
    });
})();