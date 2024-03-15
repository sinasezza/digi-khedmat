$(document).ready(function () {
  const input = $("#imagesInput");
  const form = $("#formData");

  function checkFileType(file) {
    var ext = file.name.split(".").pop().toLowerCase();
    switch (ext) {
      case "jpg":
      case "jpeg":
      case "png":
        return true;
      default:
        return false;
    }
  }

  // Add event listener to the file upload
  input.on("change", (e) => {
    const files = e.target.files;
    if (files.length > 0) {
      const fileSize = files[0].size; // Size of the first file
      if (!checkFileType(files[0])) {
        alert("شما تنها اجازه دارید عکس آپلود کنید.");
        // Clear the file input
        input.val("");
        return;
      }
      const maxSize = 5 * 1024 * 1024; // 5MB in bytes
      if (fileSize > maxSize) {
        alert("حجم فایل نباید بیشتر از 5 مگابایت باشد.");
        // Clear the file input
        input.val("");
        return;
      }
      // Prevent form submission
      e.preventDefault();
      // Submit the form programmatically
      form[0].submit();
    }
  });

  // Handle image click to show in modal
  $(".relative img").on("click", function () {
    const imageUrl = $(this).attr("src");
    $("#fullSizeImage").attr("src", imageUrl);
    $("#imageModal").removeClass("hidden");
  });

  // Close modal when clicking outside the image
  $("#imageModal").on("click", function (e) {
    if (e.target === this) {
      $(this).addClass("hidden");
    }
  });

  // Handle delete button click
  $(".delete-button").on("click", function () {
    let imageId = $(this).data("image-id");
    deleteImage(imageId);
  });

  function deleteImage(imageId) {
    // Perform delete action or show a confirmation modal
    console.log("Delete image with id:", imageId);
    // Add your delete logic here, e.g., AJAX request to server
    fetch(`/api/ads/stuff-adv-image-delete/${imageId}/`, {
      method: "DELETE",
      headers: {
        "X-CSRFToken": $('input[name="csrfmiddlewaretoken"]').val(),
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Error deleting image");
        }
        // Image deleted successfully
        $(`[data-image-id="${imageId}"]`).closest(".relative").remove();
        // Optionally, you can reload the page to reflect changes
        // window.location.reload();
      })
      .catch((error) => {
        // Error occurred while deleting the image
        console.error("Error deleting image:", error);
      });
  }

  $("#register").on("click", function (e) {
    const imgCount = $("#image-items").find("img").length; // Count the number of <img> elements
    if (!(imgCount >= 1 && imgCount <= 9)) {
      e.preventDefault();
      alert("شما باید حداقل 1 و حداکثر 9 تصویر بارگزاری کنید.");
    }
  });
});
