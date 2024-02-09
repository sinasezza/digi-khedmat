$(document).ready(function() {
  $('#toggleSidebarBtn').click(function() {
    $('body').toggleClass('sidebar-open');
    $("#sidebar").toggleClass("hidden");
  });
});