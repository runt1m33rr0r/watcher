(function() {
    'use strict';

    var open = false;

    $("#content").click(function(e) {
        if (open) {
            $("#sidebar").addClass("open");
            open = false;
        } else {
            $("#sidebar").removeClass("open");
            open = true;
        }
    });

    $(".sidebar-search input").on("input", function() {
        var searchedVal = $(this).val().toLowerCase();

        $.each($("#sidebar-items .nav-link"), function() {
            var currentVal = $(this).text().toLowerCase();

            if (!currentVal.includes(searchedVal)) {
                $(this).hide();
            } else {
                $(this).show();
            }
        });
    });
})();