import * as React from 'react';
import { Button } from './Button';
import { Socket } from './Socket';
import { Music } from './Music';
import { Messages } from './Messages';

export function Content() {
    
    return (
        <div>
            <h1>~lofi bot~</h1>
            <Music />
            <Messages /> 
            <Button />
        </div>
    );
}
