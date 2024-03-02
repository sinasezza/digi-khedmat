$(document).ready(function() {
  let experienceForm = $('#experience_empty_form > div');
  let skillForm = $('#skill_empty_form > div');
  let educationForm = $('#education_empty_form > div');
  let achievementForm = $('#achievement_empty_form > div');
  let languageForm = $('#language_empty_form > div');
  
  const formRegex = new RegExp(`-__prefix__-`, "g");

  $('#addExperience').click(function() {
    let newForm = experienceForm.clone(true)
    newForm.html(newForm.html().replace(formRegex, `-${experienceFormNum}-`));
    $('#experienceForms').append(newForm);
    $('#id_experience-TOTAL_FORMS').val(++experienceFormNum); // Update total form count for experience formset
  });

  $('#addSkill').click(function() {
    let newForm = skillForm.clone(true)
    newForm.html(newForm.html().replace(formRegex, `-${skillFormNum}-`));
    $('#skillForms').append(newForm);
    $('#id_skill-TOTAL_FORMS').val(++skillFormNum);  // Update total form count for skill formset
  });

  $('#addEducation').click(function() {
    let newForm = educationForm.clone(true)
    newForm.html(newForm.html().replace(formRegex, `-${educationFormNum}-`));
    $('#educationForms').append(newForm);
    $('#id_education-TOTAL_FORMS').val(++educationFormNum);  // Update total form count for education formset
  });

  $('#addAchievement').click(function() {
    let newForm = achievementForm.clone(true)
    newForm.html(newForm.html().replace(formRegex, `-${achievementFormNum}-`));
    $('#achievementForms').append(newForm);
    $('#id_achievement-TOTAL_FORMS').val(++achievementFormNum);  // Update total form count for achievement formset
  });

  $('#addLanguage').click(function() {
    let newForm = languageForm.clone(true)
    newForm.html(newForm.html().replace(formRegex, `-${languageFormNum}-`));
    $('#languageForms').append(newForm);
    $('#id_language-TOTAL_FORMS').val(++languageFormNum);  // Update total form count for language formset
  });
});
