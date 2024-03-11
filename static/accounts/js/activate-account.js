$(document).ready(function () {
  // Function to handle error message removal timer
  function setErrorMessageTimer(errorElement) {
    setTimeout(function () {
      errorElement.empty(); // Remove the error message
    }, 5000); // Adjust the delay time (in milliseconds) as needed
  }

  // Function to validate phone number pattern
  function validatePhoneNumberPattern(phoneValue) {
    // Check if phone number starts with 0 and is all numbers
    return (
      phoneValue.startsWith("0") &&
      /^\d+$/.test(phoneValue) &&
      phoneValue.length &&
      phoneValue.length >= 11 &&
      phoneValue.length <= 20
    );
  }

  $("#otp-btn").on("click", async function () {
    var phoneNumber = $("#otp-input").val();

    // Check if the phone number consists of only digits
    if (!validatePhoneNumberPattern(phoneNumber)) {
      $("#otp-message").append(`<p class="text-red-500 text-xs italic">شماره تلفن باید فقط شامل اعداد و دارای طول معتبر باشد.</p>`);
      setErrorMessageTimer($('#otp-message')); // Set timer to remove error message
      return; // Exit the function if the phone number contains non-digit characters
    }

    response = await fetch("/api/auth/send-otp/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json; charset=UTF-8",
        "X-CSRFToken": "{{ csrf_token }}",
      },
      body: JSON.stringify({ phone_number: phoneNumber }),
    });

    let data = await response.json();

    alert(data.message);

    if (response.status == 200) {
      $("#otp-message").empty();
      $("#otp-code-section").removeClass("hidden");
      $("#otp-btn").addClass("hidden");
      $("#submit-btn").removeClass("hidden");
      $("#otp-input").focus();
    }
  });
});