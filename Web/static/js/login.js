/**
 * Created by lightless on 2016/8/20.
 */

$("document").ready(function () {
    
    $("#login-btn").click(function (e) {
        e.preventDefault();

        var username_or_email = $("#username").val();
        var password = $("#password").val();
        var csrf_token = $('meta[name=csrf-token]').attr('content');

        var payloads = {
            "username_or_email": username_or_email,
            "password": password
        };

        $.ajax({
            type: "POST",
            url: "/account/login",
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
                $("#login-result").html(alert_message).hide().fadeIn(1000);
            }
        });

    });

});

