// toggle sidebar on click
$("#toggleSidebarBtn").click(function () {
  $("body").toggleClass("sidebar-open");
  $("#sidebar").toggleClass("hidden");

  if ($("body").hasClass("sidebar-open")) fetchSidebarCounts();
});

// Function to retrieve CSRF token from cookies
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Function to fetch sidebar counts using API
async function fetchSidebarCounts() {
  try {
    const response = await fetch("/api/auth/get-sidebar-counts/", {
      method: "GET",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    // Update the counts in the sidebar
    console.log(`favorite counts is ${data.favorites_count}`);
    $("#unseen-notifications-count").text(data.unseen_notifications_count);
    $("#favorites-count").text(data.favorites_count);
    $("#resumes-count").text(data.resumes_count);
  } catch (error) {
    console.error("Error fetching sidebar counts:", error);
  }
}
