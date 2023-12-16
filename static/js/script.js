$(document).ready(function() {
    var stickyDivOffset = $('.sticky').offset().top;

    $(window).scroll(function() {
        if ($(window).scrollTop() > stickyDivOffset) {
            $('.sticky').addClass('fixed');
        } else {
            $('.sticky').removeClass('fixed');
        }
    });
});

document.addEventListener("DOMContentLoaded", function() {
    console.log("JavaScript is working!");
});