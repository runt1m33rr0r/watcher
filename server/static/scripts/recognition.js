(function() {
    "use strict";

    var processed = $("div[processed]").attr("processed");

    if (processed != "") {
        var base64 = "data:image/jpeg;base64," + processed;
        $("#fileImage").attr("src", base64);
    }
})();