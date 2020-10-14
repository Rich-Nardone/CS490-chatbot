import * as React from 'react';
import { Socket } from './Socket';

export function Music() {
    return (
        <audio src="/static/lofi-music.mp3" controls autoPlay/>
        
    );
}
