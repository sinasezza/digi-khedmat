$(document).ready(function() {
  $('#toggleSidebarBtn').click(function() {
    $('body').toggleClass('sidebar-open');
    $("#sidebar").toggleClass("hidden");
  });


  // handling notification websocket
  let notifyProtocol = window.location.protocol == 'https:' ? 'wss' : 'ws';
  let notifyUrl = `${notifyProtocol}://${window.location.host}/ws/notifications/`;

  const notifySocket = new WebSocket(notifyUrl);
  

  notifySocket.onmessage = function (e) {
    let data = JSON.parse(e.data);
    console.log('data is', data);
  }

});