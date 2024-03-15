$(document).ready(function() {
    // When any button with class 'barter-item' is clicked
    $(document).on('click', '.barter-item-delete', function() {
        // Get the slug associated with the clicked button
        var barterSlug = $(this).data('slug');
        // Show the confirmation prompt
        var confirmDelete = confirm("آیا می‌خواهید این آگهی را حذف کنید؟");
        // If user confirms deletion
        if (confirmDelete) {
            let csrftoken = getCookie("csrftoken");
            // Send API request to backend for deletion
            fetch(`/api/barters/barter-delete/${barterSlug}/`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
            })
            .then(response => {
                if (response.ok) {
                    console.log('Barter deleted successfully.');
                    // Remove the deleted barter item from the UI
                    const barterItem = $(`#${barterSlug}`);
                    barterItem.remove();
                } else {
                    console.error('Failed to delete barter.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    });

    // When any button with class 'job-item' is clicked
    $(document).on('click', '.job-item-delete', function() {
        // Get the slug associated with the clicked button
        var jobSlug = $(this).data('slug');
        // Show the confirmation prompt
        var confirmDelete = confirm("آیا می‌خواهید این آگهی را حذف کنید؟");
        // If user confirms deletion
        if (confirmDelete) {
            let csrftoken = getCookie("csrftoken");
            // Send API request to backend for deletion
            fetch(`/api/jobs/job-delete/${jobSlug}/`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
            })
            .then(response => {
                if (response.ok) {
                    console.log('Job deleted successfully.');
                    // Remove the deleted job item from the UI
                    const jobItem = $(`#${jobSlug}`);
                    jobItem.remove();
                } else {
                    console.error('Failed to delete job.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    });

    // When any button with class 'stuff_adv-item' is clicked
    $(document).on('click', '.stuff_adv-item-delete', function() {
        // Get the slug associated with the clicked button
        var stuffAdvSlug = $(this).data('slug');
        // Show the confirmation prompt
        var confirmDelete = confirm("آیا می‌خواهید این آگهی را حذف کنید؟");
        // If user confirms deletion
        if (confirmDelete) {
            let csrftoken = getCookie("csrftoken");
            // Send API request to backend for deletion
            fetch(`/api/ads/stuff-adv-delete/${stuffAdvSlug}/`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
            })
            .then(response => {
                if (response.ok) {
                    console.log('Stuff advertisement deleted successfully.');
                    // Remove the deleted stuff advertisement item from the UI
                    const stuffAdvItem = $(`#${stuffAdvSlug}`);
                    stuffAdvItem.remove();
                } else {
                    console.error('Failed to delete stuff advertisement.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    });
});
