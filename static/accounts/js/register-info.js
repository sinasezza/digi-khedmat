$(document).ready(function () {
  // Function to handle error message removal timer
  function setErrorMessageTimer(errorElement) {
    setTimeout(function () {
      errorElement.empty(); // Remove the error message
    }, 5000); // Adjust the delay time (in milliseconds) as needed
  }

  function validateAgePattern(ageValue) {
    // Check if ageValue contains only digits
    if (!/^\d+$/.test(ageValue.trim())) {
      return false; // Age contains non-digit characters
    }

    // Convert ageValue to a number
    const age = parseInt(ageValue.trim(), 10);

    // Check if age is within the range of 0 to 100
    return age >= 0 && age <= 100;
  }

  // Check for age validity
  $("#age").change(function () {
    const ageValue = $(this).val();
    if (!validateAgePattern(ageValue)) {
      var errorElement = $("#age-errors");
      errorElement.empty(); // Clear existing error messages
      errorElement.append(
        `<p class="text-red-500 text-xs italic">سن وارد شده معتبر نیست.</p>`
      );
      $(this).val(""); // Clear the invalid age value
      setErrorMessageTimer(errorElement); // Set timer to remove error message
    }
  });


  function validateNationalCodePattern(nationalCodeValue) {
    // Remove any leading zeros
    nationalCodeValue = nationalCodeValue.replace(/^0+/, '');

    // Check if nationalCodeValue contains only digits
    if (!/^\d{10}$/.test(nationalCodeValue)) {
        return false;
    }

    // Calculate the check digit
    var check = nationalCodeValue.substr(9, 1);
    var sum = 0;
    for (var i = 0; i < 9; i++) {
        sum += parseInt(nationalCodeValue.charAt(i)) * (10 - i);
    }
    var remainder = sum % 11;

    // Validate the check digit
    if (remainder < 2 && check == remainder || remainder >= 2 && check == 11 - remainder) {
        return true;
    } else {
        return false;
    }
  }


  // Check for national code validity
  $("#national_code").change(function () {
    const nationalCodeValue = $(this).val();
    if (!validateNationalCodePattern(nationalCodeValue)) {
      var errorElement = $("#national_code-errors");
      errorElement.empty(); // Clear existing error messages
      errorElement.append(
        `<p class="text-red-500 text-xs italic">کد ملی وارد شده معتبر نیست.</p>`
      );
      $(this).val(""); // Clear the invalid national code value
      setErrorMessageTimer(errorElement); // Set timer to remove error message
    }
  });

  function generateValidNationalCode() {
    // Generate the first 9 digits randomly
    var firstNineDigits = '';
    for (var i = 0; i < 9; i++) {
        firstNineDigits += Math.floor(Math.random() * 10);
    }

    // Calculate the check digit
    var sum = 0;
    for (var i = 0; i < 9; i++) {
        sum += parseInt(firstNineDigits.charAt(i)) * (10 - i);
    }
    var remainder = sum % 11;
    var checkDigit;
    if (remainder < 2) {
        checkDigit = remainder;
    } else {
        checkDigit = 11 - remainder;
    }

    // Append the check digit to the first 9 digits
    var nationalCode = firstNineDigits + checkDigit;

    return nationalCode;
}

  // Generate 5 valid national codes
  for (var i = 0; i < 5; i++) {
      var nationalCode = generateValidNationalCode();
      console.log("Valid National Code " + (i + 1) + ": " + nationalCode);
  }
});
