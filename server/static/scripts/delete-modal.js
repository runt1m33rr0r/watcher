(function() {
    "use strict";
    
    $(".modal-button").on("click", function() {
        var modalTitle = $(this).attr("modal-title");
        var modalBody = $(this).attr("modal-body");

        $("#deleteModal .modal-title").text(modalTitle);
        $("#deleteModal .modal-body").text(modalBody);
    });
})();