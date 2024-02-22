$(document).ready(function() {
  var addFavoriteButton = $("#add-favorite-btn");

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

  addFavoriteButton.on('click', function() {
    var csrftoken = getCookie('csrftoken');
    var advertisementId = "{{ barter.id }}";  // Assuming the barter object has an ID field
    var advertisementType = "BarterAdvertising";  // Assuming the advertisement type is "BarterAdvertising"

    fetch('/api/auth/add-favorite/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
      },
      body: JSON.stringify({
        advertisement_id: advertisementId,
        advertisement_type: advertisementType
      })
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Error adding favorite');
        $(this).find('.favorite-icon').toggleClass('bg-slate-700');
      }
      console.log('Favorite added successfully');
      // Update button text or style to indicate the favorite is added
    })
    .catch(error => {
      console.error('Error adding favorite:', error.message);
    });
  });
});
