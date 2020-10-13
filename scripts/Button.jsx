import * as React from 'react';
import { Socket } from './Socket';

const inputStyle = {
  width: '500px',
  borderRadius: '15px',
  height:'40px'
};

const buttonStyle = {
  borderRadius: '15px',
  height:'40px'
};


function handleSubmit(event) {
    let newMessage = document.getElementById("message_input");
    Socket.emit('new message input', {
        'message': newMessage.value,
    });
   
    
    console.log('Sent the message ' + newMessage.value + ' to server!');
    newMessage.value = ''
    
    event.preventDefault();
}

export function Button() {
    return (
        <form onSubmit={handleSubmit}>
            <input style={inputStyle} id="message_input" placeholder="Enter a message"></input>
            <button style={buttonStyle}>Send to Bot</button>
        </form>
    );
}
