import * as React from 'react';
import ReactDOM from 'react-dom';
import { Socket } from './Socket';
import GoogleLogin from 'react-google-login';
import { useGoogleLogout } from 'react-google-login'
 
function handleSubmit(response) {
    console.log(response);
    Socket.emit('new google user', {
        'name': response['profileObj']['name'],
        'propic': response['profileObj']['imageUrl']
    });
    console.log('Sent the name ' + response['profileObj']['name'] + ' to server!');
}
function handleFailure(response) {
    console.log(response);
    alert("Try again: Failed to login to Google Account");
}

export function GoogleButton() {
    return <GoogleLogin
    clientId="441337686833-afmhrf35a9l72dui53r94ggtgja42me3.apps.googleusercontent.com"
    buttonText="Login"
    onSuccess={handleSubmit}
    onFailure={handleFailure}
    cookiePolicy={'single_host_origin'}
  />;

}
