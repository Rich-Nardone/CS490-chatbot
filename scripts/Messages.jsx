import * as React from 'react';
import { Socket } from './Socket';


const divStyle = {
  backgroundImage: 'url(' + 'static/lofi-background.jpg' + ')',
  padding: '40px',
  height: '400px',
  width: '1000px',
  objectFit: 'contain',
  overflow:'auto',
  borderRadius: '15px',
  scrollbarBaseColor: 'grey',
};

const client = {
  borderRadius: '15px',
  alignSelf: 'right',
  border: '3px solid #6495ED',
  padding: '10px',
  textAlign: 'right',
  fontSize: '20px',
};

const server = {
  borderRadius: '15px',
  alignSelf: 'left',
  border: '3px solid #696969',
  padding: '10px',
  textAlign: 'left',
  fontSize: '20px',
  fontStyle: 'italic'
};
export function Messages() {
    const [messages, setMessages] = React.useState([]);
    function displayMessages() {
        React.useEffect(() => {
            Socket.on('display', (data) => {
                console.log("Received messages from server: " + data);
                console.log("data: " + data[0]);
                setMessages(data['allMessages']);
            });
        });
    }
    
    displayMessages();
    
    return (
            <div style={divStyle}>
                {messages.map(item => {
                    return (<div><ol style={client}>{item[1]}</ol> <ol style={server}>{item[0]}</ol></div>);
                })}
            </div> 
    );
}
