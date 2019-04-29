(function() {
    'use strict';

    var fileImage = $("#fileImage");
    if ($("fileImage").attr("src") == "") {
        fileImage.hide();
    }
    
    var validImageTypes = ['image/jpeg', 'image/png'];
    var isFileValid = false;

    $("#imageForm div input").on("input", function() {
        var file = $(this).prop('files')[0];
        var fileType = file["type"];

        if (validImageTypes.includes(fileType)) {
            isFileValid = true;

            fileImage.show();
            
            var fr = new FileReader();
            fr.readAsDataURL(file);
            fr.onload = function () {
                fileImage.attr("src", fr.result);
            }

            $(this).removeClass("is-invalid");
        } else {
            isFileValid = false;

            $(this).addClass("is-invalid");
        }
    });

    $("#imageForm").on("submit", function(ev) {
        if (!isFileValid) {
            ev.preventDefault();
            ev.stopPropagation();
        }
    });
})();