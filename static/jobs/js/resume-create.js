$(document).ready(function() {
    $('#addExperience').click(function() {
      $('#experienceForms').append(`<div class="border border-gray-300 p-4 rounded-lg">${experienceForm}</div>`);
      experienceFormNum++;
      $('#id_experience-TOTAL_FORMS').val(experienceFormNum);
    });

    $('#addSkill').click(function() {
      $('#skillForms').append(`<div class="border border-gray-300 p-4 rounded-lg">${skillForm}</div>`);
      skillFormNum++;
      $('#id_skill-TOTAL_FORMS').val(skillFormNum);
    });

    $('#addEducation').click(function() {
      $('#educationForms').append(`<div class="border border-gray-300 p-4 rounded-lg">${educationForm}</div>`);
      educationFormNum++;
      $('#id_education-TOTAL_FORMS').val(educationFormNum);
    });

    $('#addAchievement').click(function() {
      $('#achievementForms').append(`<div class="border border-gray-300 p-4 rounded-lg">${achievementForm}</div>`);
      achievementFormNum++;
      $('#id_achievement-TOTAL_FORMS').val(achievementFormNum);
    });

    $('#addLanguage').click(function() {
      $('#languageForms').append(`<div class="border border-gray-300 p-4 rounded-lg">${languageForm}</div>`);
      languageFormNum++;
      $('#id_language-TOTAL_FORMS').val(languageFormNum);
    });
  });