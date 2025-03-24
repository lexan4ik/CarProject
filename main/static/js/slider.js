$(document).ready(function () {
$('.product-info-image-main').slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    arrows: false,
    fade: true,
    asNavFor: '.product-info-images-additional',
    varibaleWidth: true,

    });
    $('.product-info-images-additional').slick({
    slidesToShow: 3,
    slidesToScroll: 1,
    asNavFor: '.product-info-image-main',
    dots: false,
    centerMode: true,
    focusOnSelect: true
    });
})