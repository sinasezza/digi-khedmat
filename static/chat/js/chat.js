function gregorianToJalali(gregorianDate) {
  return moment(gregorianDate).locale('fa').format('YYYY/MM/DD - HH:mm:ss');
}

$(document).ready(function () {
  $("#message-list").animate({ scrollTop: 9999 }, 2000);
  $("#message-form > input").focus();

  let protocol = window.location.protocol == 'https:' ? 'wss' : 'ws';
  let url = `${protocol}://${window.location.host}/ws/chat/${roomName}/`;

  const chatSocket = new WebSocket(url);

  chatSocket.onmessage = function (e) {
    let data = JSON.parse(e.data);
    console.log('data is', data);

    if (data.type === 'chat') {
      const messages = JSON.parse(data.message); // Parse the JSON string to an array of message objects
      messages.forEach(message => {
        // Access the properties of each message object
        const content = message.fields.content;
        const created_at = message.fields.created_at;
        const from_user = message.fields.from_user;

        // Create HTML elements to display the message
        let messageElement;
        if (currentUser == from_user) {
          messageElement = $('<div>').html(`
            <div class="flex w-full mt-2 space-x-3 max-w-xs">
              <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300"></div>
              <div>
                <div class="bg-gray-300 p-3 rounded-r-lg rounded-bl-lg">
                  <p class="text-sm">${content}</p>
                </div>
                <span class="text-xs text-gray-500 leading-none">${gregorianToJalali(created_at)}</span>
              </div>
            </div>  
          `);
        } else {
          messageElement = $('<div>').html(`
            <div class="flex w-full mt-2 space-x-3 max-w-xs ml-auto justify-end">
              <div>
                <div class="bg-blue-600 text-white p-3 rounded-l-lg rounded-br-lg">
                  <p class="text-sm">${content}</p>
                </div>
                <span class="text-xs text-gray-500 leading-none">${gregorianToJalali(created_at)}</span>
              </div>
              <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300"></div>
            </div>
          `);
        }
        // Append the message HTML to the messages container
        $('#message-list').append(messageElement);
        $("#message-list").animate({ scrollTop: 9999 }, 1000);
      });
    } else if (data.type === 'chat.room_info') {
      // Update UI with chat room information
      let messages = $('#messages');
      messages.empty();

      for (let message of data.room_messages) {
        let li = $('<li>').html(`${message.from_user}: ${message.content}`);
        messages.append(li);
      }
    }
  }

  $('#message-form').on('submit', function (e) {
    e.preventDefault();
    let messageInput = $('[name="message"]');
    let message = messageInput.val().trim();

    if (message !== '') {
      chatSocket.send(JSON.stringify({
        'type': 'chat.message',
        'sender': senderUsername,
        'receiver': receiverUsername,
        'message': message,
      }));
      messageInput.val('');
    }
  });
});
