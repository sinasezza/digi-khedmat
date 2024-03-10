$(document).ready(function() {
  // Handle image click to show in modal
  $('.barter-image').on('click', function () {
    const imageUrl = $(this).attr('src');
    $('#fullSizeImage').attr('src', imageUrl);
    $('#imageModal').removeClass('hidden');
  });

  // Close modal when clicking outside the image or close button
  $('#imageModal, #closeModal').on('click', function (e) {
    if (e.target === this || $(e.target).is('#closeModal')) {
      $('#imageModal').addClass('hidden');
    }
  });

  var toggleFavoriteButton = $("#toggle-favorite-btn");
  var favoriteIcon = toggleFavoriteButton.find('.favorite-icon');

  // Function to toggle the favorite button icon
  function toggleFavoriteIcon() {
    if (favoriteIcon.attr('src') === save_img) {
      favoriteIcon.attr('src', unsave_img);
    } else {
      favoriteIcon.attr('src', save_img);
    }
  }


  function addFavorite() {
    fetch('/api/auth/add-favorite/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
      },
      body: JSON.stringify({
        advertisement_id: advertisementId,
        advertisement_type: advertisementType,
      })
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Error adding favorite');
      }
      // Toggle the favorite button icon
      toggleFavoriteIcon();

      alert('این آگهی به علاقه مندی های شما اضافه شد.');
      return response.json();
    })
    .then(data => {
      // Update number of favorites on page
      favoriteId = data['favorite_id'];
      isFavorite = true;
    })
    .catch(error => {
      console.error('Error adding favorite:', error.message);
    });
  }

  function deleteFavorite() {
    fetch(`/api/auth/delete-favorite/${favoriteId}/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
      },
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Error deleting favorite');
      }
      // Toggle the favorite button icon
      toggleFavoriteIcon();
      // Update button text or style to indicate the favorite is added

      alert('این آگهی از علاقه مندی های شما حذف شد.');
      
      isFavorite = false;
    })
    .catch(error => {
      console.error('Error deleting favorite:', error.message);
    });
  }

  // Handle favorite button click
  toggleFavoriteButton.on('click', function() {
    if (!userAuthenticated) {
      alert("لطفا به حساب خود وارد شوید یا حسابی بسازید.");
      return;
    }

    if(isFavorite)
      // delete
      deleteFavorite();
    else
      // add
      addFavorite();
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



