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
})();