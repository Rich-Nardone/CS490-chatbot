import * as React from 'react';
import {Button} from './Button';
import {Socket} from './Socket';
import {Music} from './Music';
import {Messages} from './Messages';
import {Users} from './Users';
import {GoogleButton} from './GoogleButton';

export function Content() {
  return (
    <div>
      <h1>~lofi bot~</h1>
      <GoogleButton />
      <Music />
      <Users />
      <Messages />
      <Button />
    </div>
  );
}
