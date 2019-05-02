(function() {
    'use strict';

    var open = true;

    var leftElement = document.getElementById('sidebar');
    var swipeLeftDetector = new Hammer(leftElement);
    swipeLeftDetector.on("swipeleft", function() {
        if (open) {
            $("#sidebar").addClass("open");
            open = false;
        }
    });

    var rightElement = document.getElementById('content');
    var swipeRightDetector = new Hammer(rightElement);
    swipeRightDetector.on("swiperight", function() {
        if (!open) {
            $("#sidebar").removeClass("open");
            open = true;
        }
    });

    $(".sidebar-search input").on("input", function() {
        var searchedVal = $(this).val().toLowerCase();

        $.each($("#sidebarItems .nav-item .nav-link"), function() {
            var currentVal = $(this).text().toLowerCase();

            if (!currentVal.includes(searchedVal)) {
                $(this).hide();
            } else {
                $(this).show();
            }
        });
    });
})();