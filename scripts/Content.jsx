    
import * as React from 'react';

import { Box } from './Box';
import { Button } from './Button';
import { Socket } from './Socket';

export function Content() {
    const [addresses, setAddresses] = React.useState([]);
    
    function getNewAddresses() {
        React.useEffect(() => {
            Socket.on('addresses received', (data) => {
                console.log("Received addresses from server: " + data['allAddresses']);
                console.log("data: " + data);
                setAddresses(data['allAddresses']);
            })
        });
    }
    
    getNewAddresses();

    return (
        <div>
            <h1>~lofi bot~</h1>
            <Box />
            <Button />
        </div>
    );
}
