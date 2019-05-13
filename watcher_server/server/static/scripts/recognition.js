(function() {
    "use strict";

    var processed = $("section").attr("processed")
    if (processed != "") {
        var base64 = "data:image/jpeg;base64," + processed;
        $("#fileImage").attr("src", base64);
    }
})();