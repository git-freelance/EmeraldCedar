function init_gallery_testi() {
    var $owl_gallery_testi = $('.owl-gallery-testi');

    // Shuffle
    $owl_gallery_testi.each(function (i1, e1) {
        $(e1).children().sort(function () {
            return Math.round(Math.random()) - 0.5;
        }).each(function (i2, e2) {
            $(e2).appendTo($(e1));
        });
    });


    $owl_gallery_testi.owlCarousel({
        loop: true,
        nav: false,
        dots: false,
        items: 1,
        autoplay: true,
        autoplayHoverPause: true,
        onInitialize: function (element) {

        },
    });
}

$(function () {
    init_gallery_testi();
    //
    var menu_init = false;

    function init_menu() {
        if ($(window).width() <= 992 && !menu_init) {
            $("#nav-cats").mmenu({}, {
                offCanvas: {
                    pageSelector: "#wrapper"
                }
            });
            menu_init = true;
        } else {
            // init_desktop_menu();
        }
    }

    init_menu();

    $(window).resize(function () {
        init_menu();
    });
    //
});