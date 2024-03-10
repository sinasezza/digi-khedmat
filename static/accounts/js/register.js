$(document).ready(function() {
  // Function to handle error message removal timer
  function setErrorMessageTimer(errorElement) {
    setTimeout(function() {
      errorElement.empty(); // Remove the error message
    }, 5000); // Adjust the delay time (in milliseconds) as needed
  }

  // Function to validate phone number using API
  async function validatePhoneNumberWithAPI(phoneValue) {
    try {
      // Make a POST request to your API endpoint for phone number validation
      const response = await fetch('/api/auth/check-field-existence/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // You may need to include CSRF token if your API requires it
        },
        body: JSON.stringify({
          field_name: 'phone_number',
          field_value: phoneValue
        })
      });

      // Parse the JSON response
      const data = await response.json();

      // Return the validation result from the API
      return data.result;
    } catch (error) {
      console.error('Error:', error.message);
      // Return false in case of an error
      return false;
    }
  }

  // Function to validate phone number pattern
  function validatePhoneNumberPattern(phoneValue) {
    // Check if phone number starts with 0 and is all numbers
    return  phoneValue.startsWith('0') && (/^\d+$/.test(phoneValue)) && phoneValue.length && phoneValue.length >= 11 && phoneValue.length <= 20;
  }

  // Phone input change event
  $('#phone_number').change(async function() {
    var phoneValue = $(this).val();
    try {
      const patternIsValid = validatePhoneNumberPattern(phoneValue);
      
      let apiIsValid = true; // Default value if pattern is not valid
      if (patternIsValid) {
        apiIsValid = await validatePhoneNumberWithAPI(phoneValue);
      }

      // Handle errors separately for pattern validation
      if (!patternIsValid) {
        var patternErrorElement = $('#phone_number-errors');
        patternErrorElement.append(`<p class="text-red-500 text-xs italic">شماره تلفن وارد شده معتبر نیست. لطفاً یک شماره تلفن معتبر با فرمت درست وارد کنید.</p>`);
        $(this).val(''); // Clear the invalid phone number
        setErrorMessageTimer(patternErrorElement); // Set timer to remove error message
      }

      // Handle errors separately for API validation
      if (!apiIsValid) {
        var apiErrorElement = $('#phone_number-errors');
        apiErrorElement.append(`<p class="text-red-500 text-xs italic">این شماره تلفن قبلا استفاده شده است.</p>`);
        $(this).val(''); // Clear the invalid phone number
        setErrorMessageTimer(apiErrorElement); // Set timer to remove error message
      }
    } catch (error) {
      console.error('Error:', error.message);
    }
  });

  // Function to validate email using API
  async function validateEmailWithAPI(emailValue) {
    try {
      // Make a POST request to your API endpoint for email validation
      const response = await fetch('/api/auth/check-field-existence/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // You may need to include CSRF token if your API requires it
        },
        body: JSON.stringify({
          field_name: 'email',
          field_value: emailValue,
        })
      });

      // Parse the JSON response
      const data = await response.json();

      // Return the validation result from the API
      return data.result;
    } catch (error) {
      console.error('Error:', error.message);
      // Return false in case of an error
      return false;
    }
  }

  // Function to validate email
  function validateEmailPattern(emailValue) {
    // Email validation regex pattern
    var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailPattern.test(emailValue);
  }

  // Email input change event
  $('#email').change(async function() {
    var emailValue = $(this).val();
    try {
      const patternIsValid = validateEmailPattern(emailValue);

      let apiIsValid;
      if (patternIsValid) {
        apiIsValid = await validateEmailWithAPI(emailValue);
      } else {
        apiIsValid = true;
      }

      // Handle errors separately for API and pattern validation
      if (!patternIsValid) {
        var patternErrorElement = $('#email-errors');
        patternErrorElement.append(`<p class="text-red-500 text-xs italic">آدرس ایمیل وارد شده معتبر نیست. لطفاً یک آدرس ایمیل معتبر وارد کنید.</p>`);
        $(this).val(''); // Clear the invalid email value
        setErrorMessageTimer(patternErrorElement); // Set timer to remove error message
      }

      if (!apiIsValid) {
        var apiErrorElement = $('#email-errors');
        apiErrorElement.append(`<p class="text-red-500 text-xs italic">این آدرس ایمیل قبلا استفاده شده است.</p>`);
        $(this).val(''); // Clear the invalid email value
        setErrorMessageTimer(apiErrorElement); // Set timer to remove error message
      }
    } catch (error) {
      console.error('Error:', error.message);
    }
  });


  $('#confirm_password').change(function() {
    pass1 = $('#password').val();
    pass2 = $(this).val();
    if (pass1 !== pass2) {
      $('#confirm_password-errors').append(`<p class="text-red-500 text-xs italic">تکرار رمز با رمز قبلی یکسان نیست.</p>`);
    }
  });

  function validateUsername(usernameValue) {
    return fetch('/api/auth/check-field-existence/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        field_name: 'username',
        field_value: usernameValue,
      })
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Error in Check username');
      }    
      return response.json();
    })
    .then(data => {
      // Return the validation result
      return data['result'];
    })
    .catch(error => {
      console.error('Error in Check username:', error.message);
      // Return false in case of an error
      return false;
    });
  }
  
  $('#username').change(async function() {
    usernameValue = $(this).val();
    try {
      const isValid = await validateUsername(usernameValue);
      if (!isValid) {
        var errorElement = $('#username-errors');
        errorElement.append(`<p class="text-red-500 text-xs italic">این نام کاربری قبلا استفاده شده است.</p>`);
        $(this).val(''); // Clear the invalid username value
        setErrorMessageTimer(errorElement); // Set timer to remove error message
      }
    } catch (error) {
      console.error('Error:', error.message);
    }
  });
});