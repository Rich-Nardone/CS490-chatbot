import * as React from 'react';
import { Socket } from './Socket';

const divStyle = {
  backgroundImage: 'url(' + 'static/lofi-background.jpg' + ')',
  padding: '40px',
  height: '400px',
  width: '1000px',
  objectFit: 'contain',
  overflow: 'auto',
  borderRadius: '15px',
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
    const [name, setName] = React.useState('');
    function displayMessages() {
        React.useEffect(() => {
            Socket.on('messages received', (data) => {
                console.log("Received message from server for" + data['name'] );
                setMessages(data['allMessages']);
            });
        });
    }
    displayMessages();
    return (
            <div style={divStyle}>
                {messages.map(item => {
                    if(item[0] === "client"){
                        return <ol style={client}><p>User~</p><p>  {item[1]}</p><p>{item[2]}</p></ol>;
                    }
                    if(item[0] === "server"){
                        return <ol style={server}><p>lofi~</p><p>  {item[1]}</p><p>{item[2]}</p></ol>;
                    }
                    if(item[0] === "image"){
                        return <ol style={server}><img src={item[1]} alt="rendered picture" width="500" height="600"/></ol>;
                    }
                    if(item[0] === "link"){
                        return <ol style={server}><a href={item[1]}>rendered link</a></ol>;
                    }
                })}
            </div> 
    );
}