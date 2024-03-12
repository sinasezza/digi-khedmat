$(document).ready(function () {
  $('#div_id_image').prop('hidden', true);

  let experienceForm = $("#experience_empty_form > div");
  let skillForm = $("#skill_empty_form > div");
  let educationForm = $("#education_empty_form > div");
  let achievementForm = $("#achievement_empty_form > div");
  let languageForm = $("#language_empty_form > div");

  const formRegex = new RegExp(`-__prefix__-`, "g");

  $("#addExperience").click(function () {
    let newForm = experienceForm.clone(true);
    newForm.html(newForm.html().replace(formRegex, `-${experienceFormNum}-`));
    $("#experienceForms").append(newForm);
    $("#id_experience-TOTAL_FORMS").val(++experienceFormNum); // Update total form count for experience formset
  });

  $("#addSkill").click(function () {
    let newForm = skillForm.clone(true);
    newForm.html(newForm.html().replace(formRegex, `-${skillFormNum}-`));
    $("#skillForms").append(newForm);
    $("#id_skill-TOTAL_FORMS").val(++skillFormNum); // Update total form count for skill formset
  });

  $("#addEducation").click(function () {
    let newForm = educationForm.clone(true);
    newForm.html(newForm.html().replace(formRegex, `-${educationFormNum}-`));
    $("#educationForms").append(newForm);
    $("#id_education-TOTAL_FORMS").val(++educationFormNum); // Update total form count for education formset
  });

  $("#addAchievement").click(function () {
    let newForm = achievementForm.clone(true);
    newForm.html(newForm.html().replace(formRegex, `-${achievementFormNum}-`));
    $("#achievementForms").append(newForm);
    $("#id_achievement-TOTAL_FORMS").val(++achievementFormNum); // Update total form count for achievement formset
  });

  $("#addLanguage").click(function () {
    let newForm = languageForm.clone(true);
    newForm.html(newForm.html().replace(formRegex, `-${languageFormNum}-`));
    $("#languageForms").append(newForm);
    $("#id_language-TOTAL_FORMS").val(++languageFormNum); // Update total form count for language formset
  });

  $("#pdf_file").change(function (event) {
    const file = event.target.files[0];

    // Check if a file is selected
    if (file) {
      const fileType = file.type;
      const fileSize = file.size / 1024 / 1024; // Convert size to MB

      // Allowed file types and maximum size
      const allowedTypes = ["application/pdf"];
      const maxSizeMB = 10;

      // Check file type
      if (!allowedTypes.includes(fileType)) {
        alert("لطفاً یک فایل PDF انتخاب کنید.");
        $("#pdf_file").val(""); // Clear the file input
        return;
      }

      // Check file size
      if (fileSize > maxSizeMB) {
        alert(`حجم فایل نباید بیشتر از ${maxSizeMB} مگابایت باشد.`);
        $("#pdf_file").val(""); // Clear the file input
        return;
      }
    }
  });

  $("#id_gender").change(function () {
    const selectedGender = $(this).val();
    const militaryServiceInput = $("#id_military_service");

    if (selectedGender === "female") {
      // If female is selected, fill the military service input with "خانم هستم" and disable it
      militaryServiceInput.val("خانم هستم");
      militaryServiceInput.prop("disabled", true);
    } else {
      // If male is selected, clear the military service input and enable it
      militaryServiceInput.val("");
      militaryServiceInput.prop("disabled", false);
    }
  });

  $("#id_image").change(function () {
    const file = this.files[0];
    const maxSize = 5 * 1024 * 1024; // 5MB in bytes
    const allowedTypes = ["image/jpeg", "image/png", "image/jpg"];

    // Check file type
    if (!allowedTypes.includes(file.type)) {
      alert("فرمت فایل باید jpg یا png باشد.");
      $(this).val(""); // Clear the file input
      return;
    }

    // Check file size
    if (file.size > maxSize) {
      alert("حجم فایل نباید بیشتر از 5 مگابایت باشد.");
      $(this).val(""); // Clear the file input
      return;
    }
  });

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
      phoneValue.length >= 11 &&
      phoneValue.length <= 20
    );
  }

  // Function to validate email pattern
  function validateEmailPattern(emailValue) {
    // Email validation regex pattern
    const emailPattern =
      /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return emailPattern.test(emailValue);
  }

  // Function to validate LinkedIn URL pattern
  function validateLinkedInPattern(urlValue) {
    // LinkedIn URL validation regex pattern
    const linkedInPattern = /^https:\/\/www\.linkedin\.com\/in\//;
    return urlValue === "" || linkedInPattern.test(urlValue);
  }

  // Function to validate GitHub URL pattern
  function validateGitHubPattern(urlValue) {
    // GitHub URL validation regex pattern
    const githubPattern = /^https:\/\/github\.com\//;
    return urlValue === "" || githubPattern.test(urlValue);
  }

  // Function to validate URL pattern
  function validateURLPattern(urlValue) {
    // URL validation regex pattern
    const urlPattern =
      /^(?:(?:(?:https?|ftp):)?\/\/)(?:\S+(?::\S*)?@)?(?:(?!-)[A-Za-z0-9-]{1,63}(?:(?:\.(?!-)[A-Za-z0-9-]{1,63})+)?)(?::\d{1,5})?(?:[/?#]\S*)?$/;
    return urlValue === "" || urlPattern.test(urlValue);
  }

  $("#id_telephone").change(function () {
    const phoneValue = $(this).val();
    const patternErrorElement = $("#telephone-errors");
    patternErrorElement.empty();
    if (!validatePhoneNumberPattern(phoneValue)) {
      patternErrorElement.append(
        `<p class="text-red-500 text-xs italic">شماره تلفن وارد شده معتبر نیست.</p>`
      );
      $(this).val(""); // Clear the input field
      setErrorMessageTimer(patternErrorElement);
    }
  });

  $("#id_email").change(function () {
    const emailValue = $(this).val();
    const patternErrorElement = $("#email-errors");
    patternErrorElement.empty();
    if (!validateEmailPattern(emailValue)) {
      patternErrorElement.append(
        `<p class="text-red-500 text-xs italic">آدرس ایمیل وارد شده معتبر نیست. لطفاً یک آدرس ایمیل معتبر وارد کنید.</p>`
      );
      $(this).val(""); // Clear the input field
      setErrorMessageTimer(patternErrorElement);
    }
  });

  $("#id_linkedin").change(function () {
    const urlValue = $(this).val();
    const patternErrorElement = $("#linkedin-errors");
    patternErrorElement.empty();
    if (!validateLinkedInPattern(urlValue)) {
      patternErrorElement.append(
        `<p class="text-red-500 text-xs italic">آدرس لینکدین باید با https://www.linkedin.com/in/ شروع شود.</p>`
      );
      $(this).val(""); // Clear the input field
      setErrorMessageTimer(patternErrorElement);
    }
  });

  $("#id_github").change(function () {
    const urlValue = $(this).val();
    const patternErrorElement = $("#github-errors");
    patternErrorElement.empty();
    if (!validateGitHubPattern(urlValue)) {
      patternErrorElement.append(
        `<p class="text-red-500 text-xs italic">آدرس گیتهاب باید با https://github.com/ شروع شود.</p>`
      );
      $(this).val(""); // Clear the input field
      setErrorMessageTimer(patternErrorElement);
    }
  });

  $("#id_website").change(function () {
    const urlValue = $(this).val();
    const patternErrorElement = $("#website-errors");
    patternErrorElement.empty();
    if (!validateURLPattern(urlValue)) {
      patternErrorElement.append(
        `<p class="text-red-500 text-xs italic">آدرس وبسایت وارد شده معتبر نیست.</p>`
      );
      $(this).val(""); // Clear the input field
      setErrorMessageTimer(patternErrorElement);
    }
  });
});
