$(document).ready(function() {
    $('#id_captcha_1').on('keydown', function() {
        // Get the value of the captcha input
        var captchaValue = $(this).val();

        // Check if the length of the captcha input exceeds 6 characters
        if (captchaValue.length > 6) {
            // If it exceeds, truncate the input to 6 characters
            captchaValue = captchaValue.slice(0, 6);
            // Update the value of the captcha input
            $(this).val(captchaValue);
        }
    });
});
