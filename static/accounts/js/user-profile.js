$(document).ready(function () {
  $("#connect-btn").on("click", function (e) {
    if (!isAuthenticated) {
      alert("لطفا به حساب خود وارد شوید.");
      e.preventDefault();
    }
  });

  // Function to fetch count from API
  async function fetchCount() {
    try {
      const response = await fetch(
        `/api/auth/get-user-ads-count/${usersUsername}/`
      );
      
      if (!response.ok) {
        throw new Error("Failed to fetch");
      }
      const data = await response.json();
      $("#ads-count").text(data.count);
    } catch (error) {
      console.error("Error fetching count:", error);
    }
  }

  // Call fetchCount() initially
  fetchCount();

  // Fetch count every 5 seconds
  setInterval(fetchCount, 5000);
});
