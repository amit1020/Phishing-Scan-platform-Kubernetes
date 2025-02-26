$(document).ready(function() {
    // cool nav menu
    $(window).on('load resize', function() {
        var $thisnav = $('.current-menu-item').offset().left;

        $('.menu-item').hover(function() {
            var $left = $(this).offset().left - $thisnav;
            var $width = $(this).outerWidth();
            var $start = 0;
            $('.wee').css({ 'left': $left, 'width': $width });
        }, function() {
            var $initwidth = $('.current-menu-item').width();
            $('.wee').css({ 'left': '0', 'width': $initwidth });
        });
    });

});

document.addEventListener('contextmenu', function(event) {
    event.preventDefault();

});



function Navigation_menu_function() {
    console.log("Navigation_menu_function");
    Get_Pages("/login/");

}



async function Get_Pages(site) {
    try {
        const response = await fetch(site, {
            method: 'GET'
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        // מעבר לדף החדש
        window.location.href = site;
    } catch (error) {
        console.log('Fetch error: ', error);
    }
}