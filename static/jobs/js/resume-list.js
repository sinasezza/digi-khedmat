$(document).ready(function () {
  // Event listener for delete buttons in sent resumes
  $(".delete-resume").on("click", function () {
    let csrftoken = getCookie("csrftoken");
    let resumeId = $(this).data("resume-id");
    let confirmation = confirm(
      "آیا مطمئنید که می‌خواهید این رزومه را حذف کنید؟"
    );

    if (confirmation) {
      // Make a DELETE request to the API endpoint
      $.ajax({
        url: `/api/jobs/resumes/resume-delete/${resumeId}/`,
        type: "DELETE",
        headers: {
          "X-CSRFToken": csrftoken,
        },
        success: function (response) {
          // Remove the deleted resume from the DOM
          $(`#resume-${resumeId}`).remove();
          alert("رزومه با موفقیت حذف شد.");
        },
        error: function (xhr, status, error) {
          console.error(xhr.responseText);
          alert("مشکلی در حذف رزومه به وجود آمده است.");
        },
      });
    }
  });

  // Event listener for delete buttons in sent resume files
  $(".delete-resume-file").on("click", function () {
    let csrftoken = getCookie("csrftoken");
    let resumeFileId = $(this).data("resume-file-id");
    let confirmation = confirm(
      "آیا مطمئنید که می‌خواهید این فایل رزومه را حذف کنید؟"
    );

    if (confirmation) {
      // Make a DELETE request to the API endpoint
      $.ajax({
        url: `/api/jobs/resumes/resume-file-delete/${resumeFileId}/`,
        type: "DELETE",
        headers: {
          "X-CSRFToken": csrftoken,
        },
        success: function (response) {
          // Remove the deleted resume file from the DOM
          $(`#resume-file-${resumeFileId}`).remove();
          alert("فایل رزومه با موفقیت حذف شد.");
        },
        error: function (xhr, status, error) {
          console.error(xhr.responseText);
          alert("مشکلی در حذف فایل رزومه به وجود آمده است.");
        },
      });
    }
  });
});
