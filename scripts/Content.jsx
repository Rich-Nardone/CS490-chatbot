import * as React from 'react';
import { Button } from './Button';
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
export function Content() {
    const [messages, setMessages] = React.useState([]);
    
    function getNewMessages() {
        React.useEffect(() => {
            Socket.on('messages received', (data) => {
                console.log("Received messages from server: " + data['allAddresses']);
                console.log("data: " + data);
                setMessages(data['allMessages']);
            })
        });
    }
    
    getNewMessages();

    return (
        <div>
            <h1>~lofi bot~</h1>
            <div style={divStyle}>
                {messages.map(item => {
                    return <ol style={client}>client:{item}</ol>;
                })}
                {messages.map(item => {
                    return <ol style={server}>lofi bot:{item}</ol>;
                })}
            </div> 
            <Button />
        </div>
    );
}
