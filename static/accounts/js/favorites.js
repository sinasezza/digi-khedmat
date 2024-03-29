$(document).ready(function () {
  $('.delete-btn').on('click', function() {
    var $deleteBtn = $(this);
    var $favoriteID = $deleteBtn.closest('li').data('favorite-id');
    handleDelete($favoriteID, $deleteBtn);
  });

  // Function to remove favorite element
  function handleDelete(favoriteId, $deleteBtn) {
    let csrftoken = getCookie("csrftoken");
    if (confirm("آیا مطمئن هستید که می‌خواهید این علاقه مندی را حذف کنید؟")) {
      $.ajax({
        url: `/api/auth/delete-favorite/${favoriteId}/`,
        type: "DELETE",
        headers: {
          "X-CSRFToken": csrftoken,
        },
        success: function () {
          // Remove the favorite element from the DOM
          $deleteBtn.closest('li').remove();
        },
        error: function (xhr, textStatus, errorThrown) {
          console.error("Error deleting favorite:", textStatus);
        },
      });
    }
  }
});
