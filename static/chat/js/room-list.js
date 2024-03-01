$(document).ready(function () {
  // Function to toggle modal visibility
  function toggleModal() {
    var modal = $('#reportModal');
    if (modal.hasClass('hidden')) {
      modal.removeClass('hidden');
      $('body').addClass('overflow-hidden');
    } else {
      modal.addClass('hidden');
      $('body').removeClass('overflow-hidden');
    }
  }

  // Event listener for delete buttons
  $(".delete-room").on("click", function () {
    let csrftoken = getCookie("csrftoken");
    let roomName = $(this).data("room-name");
    let confirmation = confirm(
      "آیا مطمئنید که می‌خواهید این گفتگو را حذف کنید؟"
    );

    if (confirmation) {
      // Make a DELETE request to the API endpoint
      fetch(`/api/chat/room-delete/${roomName}/`, {
        method: 'DELETE',
        headers: {
          'X-CSRFToken': csrftoken
        }
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        // Remove the deleted room from the DOM
        $("#room-" + roomName).remove();
        alert("گفتگو با موفقیت حذف شد.");
      })
      .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
        alert("مشکلی در حذف گفتگو به وجود آمده است.");
      });
    }
  });

  // Event listener for report buttons
  $(".report-room").on("click", function () {
    // Show the report modal
    let roomName = $(this).data("room-name");
    $("#reportRoomName").val(roomName);
    toggleModal();
  });

  // Event listener for closing the modal
  $("#modal-close, #cancel-btn").on("click", function () {
    toggleModal();
  });

  // Event listener for submitting the report form
  $("#submit-btn").on("click", function () {
    let csrftoken = getCookie("csrftoken");
    let roomName = $("#reportRoomName").val();
    let message = $("#reportMessage").val();

    // Make a POST request to the report API endpoint
    fetch(`/api/chat/room-report/${roomName}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
      },
      body: JSON.stringify({ message: message })
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      alert("گفتگو گزارش شد.");
      // Close the report modal
      toggleModal();
    })
    .catch(error => {
      console.error('There has been a problem with your fetch operation:', error);
      alert("مشکلی در گزارش گفتگو به وجود آمده است.");
    });
  });

});
