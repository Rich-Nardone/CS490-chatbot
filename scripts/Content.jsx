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
};

const server = {
  alignSelf: 'left',
  border: '3px solid #A9A9A9',
  padding: '10px',
  width: '150px'
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
                    return <ol style={client}>{item}</ol>;
                })}
            </div> 
            <Button />
        </div>
    );
}
