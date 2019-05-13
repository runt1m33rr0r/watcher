(function() {
    "use strict";

    function handleSlider(sliderId) {
        var label = $(sliderId).prev();
        var labelText = label.text();

        label.text(labelText + $(sliderId).attr("value"));

        $(sliderId).on("input", function() {
            label.text(labelText + $(this).val());
        });
    }

    handleSlider("#sensitivity");
    handleSlider("#downscale");
    handleSlider("#alertTimeout");
    handleSlider("#cameraTimeout");
    handleSlider("#checkTimeout");
    handleSlider("#trainTimeout");

    $("#resetButton").on("click", function(ev) {
        ev.preventDefault();
        ev.stopPropagation();

        window.location.replace(window.location.href);
    });
})();