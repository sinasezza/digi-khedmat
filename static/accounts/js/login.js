$(document).ready(function() {
    $('#id_captcha_1').on('keydown', function(e) {
        // Get the value of the captcha input
        var captchaValue = $(this).val();

        // Check if the length of the captcha input exceeds 6 characters
        if (captchaValue.length > 6) {
            e.preventDefault();
        }
    });
});
