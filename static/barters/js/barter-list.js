$(document).ready(function () {
  // Function to fetch views count for each barter item
  async function fetchViewsCount() {
    $("#barter-list .barter-item").each(async function () {
      const barterSlug = $(this).data('slug');

      try {
        const response = await fetch(`/api/barters/barter-fetch-views/${encodeURIComponent(barterSlug)}/`);
        if (!response.ok) {
          throw new Error("Failed to fetch");
        }
        const data = await response.json();
        $(this).find(".barter-item-view").text(`${data.views} بازدید`);
      } catch (error) {
        console.error("Error fetching views count:", error);
      }
    });
  }

  // Call fetchViewsCount() initially
  fetchViewsCount();

  // Fetch views count every 5 seconds
  setInterval(fetchViewsCount, 5000);
});
