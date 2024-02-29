$(document).ready(function () {
  // Event listener for delete buttons
  $(".delete-room").on("click", function () {
    let csrftoken = getCookie("csrftoken");
    let roomName = $(this).data("room-name");
    let confirmation = confirm(
      "آیا مطمئنید که می‌خواهید این گفتگو را حذف کنید؟"
    );

    if (confirmation) {
      // Make a DELETE request to the API endpoint
      $.ajax({
        url: `/api/chat/room-delete/${roomName}/`,
        type: "DELETE",
        headers: {
          "X-CSRFToken": csrftoken,
        },
        success: function (response) {
          // Remove the deleted room from the DOM
          $("#room-" + roomName).remove();
          alert("گفتگو با موفقیت حذف شد.");
        },
        error: function (xhr, status, error) {
          console.error(xhr.responseText);
          alert("مشکلی در حذف گفتگو به وجود آمده است.");
        },
      });
    }
  });

  // Event listener for report buttons
  $(".report-room").on("click", function () {
    let csrftoken = getCookie("csrftoken");
    let roomName = $(this).data("room-name");
    let confirmation = confirm(
      "آیا مطمئنید که می‌خواهید این گفتگو را گزارش کنید؟"
    );

    if (confirmation) {
      // Make a POST request to the report API endpoint
      $.ajax({
        url: `/api/chat/room-report/${roomName}/`,
        type: "POST",
        headers: {
          "X-CSRFToken": csrftoken,
        },
        success: function (response) {
          alert("گفتگو گزارش شد.");
        },
        error: function (xhr, status, error) {
          console.error(xhr.responseText);
          alert("مشکلی در گزارش گفتگو به وجود آمده است.");
        },
      });
    }
  });
});
