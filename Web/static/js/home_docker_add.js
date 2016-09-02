/**
 * Created by lightless on 2016/9/2.
 */

$(document).ready(function () {

    $(".image-select").click(function () {
        $(".image-select").removeClass("image-selected");
        $(this).addClass("image-selected");
    });

    $(".components-select").click(function () {
        $(".components-select").removeClass("components-selected");
        $(this).addClass("components-selected");
    });

});