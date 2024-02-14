$(document).ready(function() {
    // When the button with data-modal-toggle attribute is clicked
    $('[data-modal-toggle]').click(function() {
        // Get the target modal ID from data-modal-target attribute
        var targetModal = $(this).data('modal-target');
        // Toggle the visibility of the modal with the target ID
        $('#' + targetModal).toggleClass('hidden');
        
        // Get the barter slug associated with the clicked button
        var barterSlug = $(this).data('barter-slug');
        // Set the barter slug as a data attribute in the confirm delete button
        $('#confirm-delete').data('barter-slug', barterSlug);
    });
  
    // When the button with data-modal-hide attribute is clicked
    $('[data-modal-hide]').click(function() {
        // Get the target modal ID from data-modal-hide attribute
        var targetModal = $(this).data('modal-hide');
        // Hide the modal with the target ID
        $('#' + targetModal).addClass('hidden');
    });

    // When the "Yes, I'm sure" button is clicked
    $('#confirm-delete').click(function() {
        let csrftoken = getCookie("csrftoken");
        // Get the barter slug from the data attribute
        var barterSlug = $(this).data('barter-slug');
      
        // Send API request to backend for deletion
        fetch(`/api/barters/barter-delete/${barterSlug}/`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            // Add any request body if needed
        })
        .then(response => {
            if (response.ok) {
                // Handle success response
                console.log('Barter deleted successfully.');
                // Remove the deleted barter item from the UI
                $(`#${barterSlug}`).remove();
                // Hide the modal
                $('#popup-modal').addClass('hidden');
            } else {
                // Handle error response
                console.error('Failed to delete barter.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
