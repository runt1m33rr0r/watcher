(function() {
    'use strict';

    var fileImage = $("#fileImage");
    var processed = fileImage.attr("processed")
    if (processed != "") {
        var base64 = "data:image/jpeg;base64," + processed;
        fileImage.attr("src", base64);
    }
})();