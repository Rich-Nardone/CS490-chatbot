import * as React from 'react';
import { Socket } from './Socket';

const countStyle = {
  width: '60px',
  borderRadius: '15px',
  height:'50px',
  fontColor:'black'
};

export function Users() {
    const [count, setCount] = React.useState(0);
    function updateCount () {
    React.useEffect(() => {
            Socket.on('connection', (data) => {
                console.log("A user has "+data["connection"] );
                setCount(data["count"]);
            });
        });
    }
    updateCount();
    return (
        <div style={countStyle}>
            Users: {count}
        </div>
    );
}

