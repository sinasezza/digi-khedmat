$(document).ready(function () {
  // Handle image click to show in modal
  $("#resume-btn").on("click", function () {
    $("#resume-modal").removeClass("hidden");
  });

  // Close modal when clicking outside the image or close button
  $("#resume-modal, #closeModal").on("click", function (e) {
    if (e.target === this || $(e.target).is("#closeModal")) {
      $("#resume-modal").addClass("hidden");
    }
  });

  var toggleFavoriteButton = $("#toggle-favorite-btn");
  var favoriteIcon = toggleFavoriteButton.find(".favorite-icon");

  // Function to toggle the favorite button icon
  function toggleFavoriteIcon() {
    if (favoriteIcon.attr("src") === save_img) {
      favoriteIcon.attr("src", unsave_img);
    } else {
      favoriteIcon.attr("src", save_img);
    }
  }

  async function addFavorite() {
    try {
      const response = await fetch("/api/auth/add-favorite/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
          advertisement_id: advertisementId,
          advertisement_type: advertisementType,
        }),
      });

      if (!response.ok) {
        throw new Error("Error adding favorite");
      }

      // Toggle the favorite button icon
      toggleFavoriteIcon();

      alert("این آگهی به علاقه مندی های شما اضافه شد.");

      const data = await response.json();
      // Update number of favorites on page
      favoriteId = data["favorite_id"];
      isFavorite = true;
    } catch (error) {
      console.error("Error adding favorite:", error.message);
    }
  }

  async function deleteFavorite() {
    try {
      const response = await fetch(`/api/auth/delete-favorite/${favoriteId}/`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
      });

      if (!response.ok) {
        throw new Error("Error deleting favorite");
      }

      // Toggle the favorite button icon
      toggleFavoriteIcon();

      alert("این آگهی از علاقه مندی های شما حذف شد.");

      isFavorite = false;
    } catch (error) {
      console.error("Error deleting favorite:", error.message);
    }
  }

  // Handle favorite button click
  toggleFavoriteButton.on("click", async function () {
    if (!userAuthenticated) {
      alert("لطفا به حساب خود وارد شوید یا حسابی بسازید.");
      return;
    }

    if (isFavorite) {
      await deleteFavorite();
    } else {
      await addFavorite();
    }

    fetchSidebarCounts();
  });

  $("#copy-link-btn").on("click", function () {
    // Get the current URL
    var currentUrl = window.location.href;

    // Create a temporary textarea element
    var tempTextArea = document.createElement("textarea");

    // Set the value of the textarea to the current URL
    tempTextArea.value = currentUrl;

    // Append the textarea to the body
    document.body.appendChild(tempTextArea);

    // Select the text inside the textarea
    tempTextArea.select();

    try {
      // Copy the selected text to the clipboard
      document.execCommand("copy");

      // Alert the user that the URL has been copied
      alert("لینک آگهی کپی شد");
    } catch (err) {
      console.error("Unable to copy:", err);
    } finally {
      // Remove the temporary textarea from the body
      document.body.removeChild(tempTextArea);
    }
  });
});
