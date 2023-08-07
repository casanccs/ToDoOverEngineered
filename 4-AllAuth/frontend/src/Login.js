import { Link } from "react-router-dom";
import {useState, useEffect} from 'react';
import { getCSRFToken } from "./App"
import jwt_decode from "jwt-decode"

export default function Login(){
    let [username, setUsername] = useState('')
    let [password, setPassword] = useState('')

    async function handleCallbackResponse(response){
        console.log("Encoded JWT ID token:" + response.credential)
        let userObject = jwt_decode(response.credential)
        console.log(userObject)
        const csrfToken = await getCSRFToken()
        let response2 = await fetch('/api/user/', {
            method: 'POST',
            headers: {
                "Content-type": "application/json",
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify(userObject)
        })
        let data = await response2.json()
        console.log(data)
        window.location.replace('/')
    }

    useEffect(() => {
        /* global google */
        google.accounts.id.initialize({
            client_id: "606411497659-cv24dn1633ncohv7erocj69fcr3rqv10.apps.googleusercontent.com",
            callback: handleCallbackResponse
        })
        google.accounts.id.renderButton(
            document.getElementById("signInDiv"),
            {theme: "outline", size: "large"}
        )
    },[])

    async function submit(e){
        e.preventDefault()
        const csrfToken = await getCSRFToken()
        let response = await fetch('/api/user/', {
            method: 'PUT',
            headers: {
                "Content-type": "application/json",
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({
                'username': username,
                'password': password,
            })
        })
        let data = await response.json()
        console.log(data)
        if (response.status === 200){
            window.location.replace('/')
        }
    }

    // async function GoogleLogin(e) { //This sets the sessionid
    //     e.preventDefault()
    //     const csrfToken = await getCSRFToken()
    //     let response = await fetch('/accounts/google/login/?process=login', {
    //         method: 'POST',
    //         headers: {
    //             'X-CSRFToken': csrfToken,
    //         },
    //     })
    //     let data = await response.json()
    //     console.log(data)
    // }

    return (
        <div>
            <Link to="/createAccount">Create Account</Link>
            <br />
            <form>
                <label>Username: </label>
                <input type="text" value={username} onChange={e => setUsername(e.target.value)}/>
                <br />
                <label>Password:</label>
                <input type="text" value={password} onChange={e => setPassword(e.target.value)}/>
                <br />
                <input type="submit" onClick={submit} value="Login" />
            </form>
            <div id="signInDiv"></div>
            {/* <Link to={'https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Fgoogle%2Flogin%2F&prompt=consent&response_type=code&client_id=606411497659-cv24dn1633ncohv7erocj69fcr3rqv10.apps.googleusercontent.com&scope=openid%20email%20profile&access_type=offline&service=lso&o2v=2&flowName=GeneralOAuthFlow'}>Google Login</Link> */}
            
        </div>
    )
}