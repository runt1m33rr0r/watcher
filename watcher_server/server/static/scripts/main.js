(function() {
    'use strict';

    $.each($(".nav-link"), function() {
        if ($(this).attr("href") == window.location.pathname) {
            $(this).addClass("active");
        } else {
            $(this).removeClass("active");
        }
    });
})();