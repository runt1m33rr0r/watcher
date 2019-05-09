(function() {
    'use strict';

    function adjustSize() {
        var cardColumns = $('.card-columns');

        if ($(window).width() <= 800){
            cardColumns.css('width', '95%');
        } else {
            cardColumns.css('width', defaultWidth);
        }
    }

    var cards = $('.card');
    if (cards.length == 1) {
        var defaultWidth = '50%';

        $('.card-columns')
            .css('column-count', '1')
            .css('width', defaultWidth);
        adjustSize();
        $(window).resize(adjustSize);
    }
})();