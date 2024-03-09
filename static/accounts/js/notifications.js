$(document).ready(function() {
    $('.delete-btn').on('click', function() {
        var $deleteBtn = $(this);
        var notificationId = $deleteBtn.closest('li').data('notification-id');
    
        // Show confirmation dialog
        if (confirm("آیا این اعلان را حذف میکنید؟")) {
            handleDelete(notificationId, $deleteBtn);
        } else {
            // User clicked cancel, do nothing
            return;
        }
    });
    

    $('.mark-as-read-btn').on('click', function() {
        var $seenBtn = $(this);
        var notificationId = $seenBtn.closest('li').data('notification-id');
        handleMarkAsRead(notificationId, $seenBtn);
    });

    // Function to handle delete action
    function handleDelete(notificationId, $deleteBtn) {
        var csrftoken = getCookie('csrftoken');
        fetch(`/api/auth/delete-notification/${notificationId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrftoken
            },
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error deleting notification');
            }
            console.log('Notification deleted successfully');
            // Remove the notification from the DOM using the stored reference
            $deleteBtn.closest('li').remove();
        })
        .catch(error => {
            console.error('Error deleting notification:', error.message);
        });
    }

    // Function to handle mark as read action
    function handleMarkAsRead(notificationId, $seenBtn) {
        var csrftoken = getCookie('csrftoken');
        var isSeen = $seenBtn.hasClass('seen');
        fetch(`/api/auth/notification-mark-as-read/${notificationId}/`, {
            method: 'PATCH',
            headers: {
                'X-CSRFToken': csrftoken
            },
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error marking notification as read');
            }
            console.log('Notification marked as read successfully');

            // Toggle the button's class based on its previous state
            if (isSeen) {
                $seenBtn.removeClass('text-green-800 hover:text-white bg-green-600 hover:bg-green-200 focus:ring-2 focus:ring-green-500');
                $seenBtn.addClass('text-green-500 hover:text-white bg-green-200 hover:bg-green-600 focus:ring-2 focus:ring-green-700');
                $seenBtn.text('خوانده نشده');
            } else {
                $seenBtn.removeClass('text-green-500 hover:text-white bg-green-200 hover:bg-green-600 focus:ring-2 focus:ring-green-700');
                $seenBtn.addClass('text-green-800 hover:text-white bg-green-600 hover:bg-green-200 focus:ring-2 focus:ring-green-500');
                $seenBtn.text('خوانده شده');
            }

            // Toggle the seen class
            $seenBtn.toggleClass('seen', !isSeen);
        })
        .catch(error => {
            console.error('Error marking notification as read:', error.message);
        });
    }
});
