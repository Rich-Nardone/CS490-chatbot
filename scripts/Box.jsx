import * as React from 'react';
import { Socket } from './Socket';

const divStyle = {
  backgroundImage: 'url(' + 'static/lofi-background.jpg' + ')',
  color: 'SlateBlue',
  padding: '40px',
  height: '500px',
  width: '50%',
  objectFit: 'contain',
  
};

export function Box() {
    return (
        <div style={divStyle}>
            Content
        </div>
    );
}