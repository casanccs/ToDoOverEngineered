import { Link } from "react-router-dom";
import {useState} from 'react';
import { getCSRFToken } from "./App"

export default function CreateAccount(){
    let [username, setUsername] = useState('')
    let [password, setPassword] = useState('')

    async function submit(e){
        e.preventDefault()
        const csrfToken = await getCSRFToken()
        let response = await fetch('/api/user/', {
            method: 'POST',
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
        if (response.status == 201){
            window.location.replace('/')
        }
    }

    return (
        <div>
            <Link to="/login">Login</Link>
            <br />
            <form>
                <label>Username: </label>
                <input type="text" value={username} onChange={e => setUsername(e.target.value)}/>
                <br />
                <label>Password:</label>
                <input type="text" value={password} onChange={e => setPassword(e.target.value)}/>
                <br />
                <input type="submit" onClick={submit} value="Create Account" />
            </form>
        </div>
    )
}