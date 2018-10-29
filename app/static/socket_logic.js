namespace = '/test';

var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

socket.on('my_response', function(msg) {
    $('#log').append('<br>' + $('<div/>').text('Received #' + msg.count + ': ' + msg.data).html());
});


socket.emit('message');


socket.on('users', function(msg) {

    var users = msg.users
    var str = '<div>'

    JSON.parse(users).forEach(function(user) {
      str +=   '<div id="' + user.id + '" class="user_list"> <h2>' + user.name + '</h2> <p>heh text..</p> </div>'
    }); 

    str += '</div>';
    document.getElementById("userContainer").innerHTML = str;   


    JSON.parse(users).forEach(function(user) {
        var something = document.getElementById(user.id);

        something.style.cursor = 'pointer';
        something.onclick = function() {
            document.getElementById("name").innerHTML = user.name;
            socket.emit('request_chat', {friend_id: user.id})
        };
    })

}); 

socket.on('chat', function(messages) {

    var div = document.getElementById('chat');

    JSON.parse(messages['chat']).forEach(function(message) {

        if (message.sender == 2){
            div.innerHTML += '<div class="container"> <p align="right">' + message.message + '</p> </div>'
        } else {
            div.innerHTML += '<div class="container darker"> <p  align="left">' + message.message + '</p> </div>'
        }

    })

    div.scrollTop = div.scrollHeight;

}) 

socket.on('server_send_message_to_client', function(message) {

    var div = document.getElementById('chat');
        div.innerHTML += '<div class="container"> <p align="left">' + message.message + '</p> </div>'

    div.scrollTop = div.scrollHeight;
})         


$('form#broadcast').submit(function(event) {
    socket.emit('client_send_message_to_server', {data: $('#broadcast_data').val()});


    var div = document.getElementById('chat');
    div.innerHTML += '<div class="container darker" align="right"> <p>' + $('#broadcast_data').val() + '</p> </div>'
    div.scrollTop = div.scrollHeight;

    document.getElementById('broadcast_data').value = ''
    return false;
});
