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
            data: payloads,
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", csrf_token);
            }, success: function (return_data) {
                var alert_message = '<div class="alert alert-' + return_data.tag +
                    ' alert-dismissible fade in flash-alert" role="alert">' +
                    '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
                    '<span aria-hidden="true">&times;</span>' +
                    '<span class="sr-only">Close</span>' +
                    '</button>' +
                    return_data.msg +
                    '</div>';
                $("#reg-result").html(alert_message).hide().fadeIn(1000);
            }
        });
    });

});

