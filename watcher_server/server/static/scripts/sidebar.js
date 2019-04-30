(function() {
    'use strict';

    var open = false;

    var element = document.getElementById('content');
    var swipeDetector = new Hammer(element);
    swipeDetector.on("swipeleft", function() {
        if (open) {
            $("#sidebar").addClass("open");
            open = false;
        }
    });

    swipeDetector.on("swiperight", function() {
        if (!open) {
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