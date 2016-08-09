/**
 * Created by lightless on 16-8-7.
 */

$(document).ready(function () {
    $("a").click(function (event) {
        event.preventDefault();
    });

    $("#banner h1").hide().fadeIn(1000);
    $("#banner p").hide().fadeIn(1000);
    $("#banner a").hide().fadeIn(1000);

});
