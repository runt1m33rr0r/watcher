(function() {
    'use strict';

    $.each($(".nav-link"), function() {
        if ($(this).attr("href") == window.location.pathname) {
            $(this).addClass("active");
        } else {
            $(this).removeClass("active");
        }
    });

    $.each($(".dropdown"), function() {
        var dropdown = $(this)
        
        $.each(dropdown.find(".dropdown-menu .dropdown-item"), function() {
            if ($(this).attr("href") == window.location.pathname) {
                dropdown.addClass("active");
                return false;
            } else {
                dropdown.removeClass("active");
            }
        });
    });
})();