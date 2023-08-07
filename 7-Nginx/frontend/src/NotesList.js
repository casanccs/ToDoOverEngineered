import {useState, useEffect} from 'react';
import { Link } from "react-router-dom";
import { getCSRFToken } from "./App"


export default function NotesList({user}){

    let [notes, setNotes] = useState([])

    useEffect(() => {
        getNotes();
    }, [])

    async function getNotes(){
        let response = await fetch('/api/notes/')
        let data = await response.json()
        if (response.status === 200){
            console.log(data)
            setNotes(data)
        }
    }

    async function Logout(){
        const csrfToken = await getCSRFToken()
        let response = await fetch('/api/user/', {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrfToken,
            },
            credentials: 'include',
        })
        let data = await response.json()
        console.log(data)
        window.location.replace('/login')
    }


    return (
        <div>
            <Link onClick={Logout}>Logout</Link>
            <h1>Notes Page</h1>
            <h3>User: {user.username}</h3>
            <Link to={'/note/new'}>Create Note</Link>
            {notes && notes.map((note) => (
                <Link to={`/note/${note.id}`} key={note.id}>
                    <h3>{note.title}</h3>
                    <p>{note.text}</p>
                </Link>   
            ))}
        </div>
        
    )
}