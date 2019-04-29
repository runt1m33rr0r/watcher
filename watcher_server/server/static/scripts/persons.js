(function() {
    'use strict';
    
    var validImageTypes = ['image/jpeg', 'image/png'];
    var isValidFile = false;

    $("#imageForm div input").on("input", function() {
        var file = $(this).prop('files')[0];
        var fileType = file["type"];

        if (validImageTypes.includes(fileType)) {
            isValidFile = true;

            var fr = new FileReader();
            fr.readAsDataURL(file);
            fr.onload = function () {
                $("#fileImage").attr("src", fr.result);
            }
        } else {
            isValidFile = false;
        }
    });
})();