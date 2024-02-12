$(document).ready(function () {
  const input = $("#imagesInput");
  const form = $("#formData");
  const registerBtn = $("#register");

  input.on('change', (e) => {
    form.submit();
  });

  registerBtn.on('click', (e) => {
    e.preventDefault();
    form.submit();
  });

  function deleteImage(image) {
    console.log(`image is ${image}`);
    console.log(`image value is ${image.val()}`);
  }

  let $carouselItems = $('[data-carousel-item]');

  $('[data-carousel-prev]').on('click', function () {
    currentIndex = (currentIndex - 1 + $carouselItems.length) % $carouselItems.length;
    showImage(currentIndex);
  });

  $('[data-carousel-next]').on('click', function () {
    currentIndex = (currentIndex + 1) % $carouselItems.length;
    showImage(currentIndex);
  });

  // Show delete button on hover
  $carouselItems.on('mouseenter', function () {
    $(this).find('.delete-button').css('opacity', 1);
  }).on('mouseleave', function () {
    $(this).find('.delete-button').css('opacity', 0);
  });

  // Handle delete button click
  $('.delete-button').on('click', function () {
    let imageId = $(this).data('image-id');
    deleteImage(imageId);
  });

  // Initial show
  showImage(currentIndex);

  function showImage(index) {
    $carouselItems.hide().eq(index).show();
  }

  function deleteImage(imageId) {
    // Perform delete action or show a confirmation modal
    console.log('Delete image with id:', imageId);
    // Add your delete logic here, e.g., AJAX request to server
    fetch(`/api/barters/delete-barter-image/${imageId}/`, {
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
        $(`[data-image-id="${imageId}"]`).closest('[data-carousel-item]').remove();
        window.location.reload();
    })
    .catch(error => {
        // Error occurred while deleting the image
        console.error('Error deleting image:', error);
    });
  }
});
