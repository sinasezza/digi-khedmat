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

  // Function to retrieve CSRF token from cookies
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      var cookies = document.cookie.split(";");
      for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});
