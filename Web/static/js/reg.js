/**
 * Created by lightless on 2016/8/20.
 */

$("document").ready(function () {

    $("#register-btn").click(function (e) {
        e.preventDefault();

        var username = $("#username").val();
        var email = $("#email").val();
        var password = $("#password").val();

        var payloads = {
            "username": username,
            "email": email,
            "password": password
        };

        $.post("/register", payloads, function (return_data) {
            console.log(return_data);
        });
    });

});

