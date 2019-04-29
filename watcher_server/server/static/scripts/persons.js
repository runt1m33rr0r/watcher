(function() {
    'use strict';

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