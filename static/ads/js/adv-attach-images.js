$(document).ready(function () {
    const input = $("#imagesInput");
    const form = $("#formData");
  
    input.on('change', (e) => {
      form.submit();
    });
  
    // Show delete button on hover
    $('.relative').on('mouseenter', function () {
      $(this).find('.delete-button').css('opacity', 1);
    }).on('mouseleave', function () {
      $(this).find('.delete-button').css('opacity', 0);
    });
  
    // Handle delete button click
    $('.delete-button').on('click', function () {
      let imageId = $(this).data('image-id');
      deleteImage(imageId);
    });
  
    // Handle image click to show in modal
    $('.relative img').on('click', function () {
      const imageUrl = $(this).attr('src');
      $('#fullSizeImage').attr('src', imageUrl);
      $('#imageModal').removeClass('hidden');
    });
  
    // Close modal when clicking outside the image
    $('#imageModal').on('click', function (e) {
      if (e.target === this) {
        $(this).addClass('hidden');
      }
    });
  
    function deleteImage(imageId) {
      // Perform delete action or show a confirmation modal
      console.log('Delete image with id:', imageId);
      // Add your delete logic here, e.g., AJAX request to server
      fetch(`/api/ads/stuff-ads-image-delete/${imageId}/`, {
          method: 'DELETE',
          headers: {
              'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
          }
      })
      .then(response => {
          if (!response.ok) {
            throw new Error('Error deleting image');
          }
          // Image deleted successfully
          $(`[data-image-id="${imageId}"]`).closest('.relative').remove();
          // Optionally, you can reload the page to reflect changes
          // window.location.reload();
      })
      .catch(error => {
          // Error occurred while deleting the image
          console.error('Error deleting image:', error);
      });
    }
  });