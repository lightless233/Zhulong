/**
 * Created by lightless on 2016/8/20.
 */

$("document").ready(function () {

    $("#register-btn").click(function (e) {
        e.preventDefault();

        var username = $("#username").val();
        var email = $("#email").val();
        var password = $("#password").val();
        var csrf_token = $('meta[name=csrf-token]').attr('content');

        var payloads = {
            "username": username,
            "email": email,
            "password": password
        };

        // $.post("/register", payloads, function (return_data) {
        //     console.log(return_data);
        // });

        $.ajax({
            type: "POST",
            url: "/register",
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", csrf_token);
            }, success: function (return_data) {
                console.log(return_data);
            }
        });
    });

});

