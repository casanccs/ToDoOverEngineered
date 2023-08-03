import {useState, useEffect} from 'react';
import { Link } from "react-router-dom";

export default function NotesList(){

    let [notes, setNotes] = useState([])

    useEffect(() => {
        getNotes();
    }, [])

    async function getNotes(){
        let response = await fetch('/api/notes/')
        let data = await response.json()
        console.log(data)
        setNotes(data)
    }


    return (
        <div>
            <h1>Notes Page</h1>
            <Link to={'/note/new'}>Create Note</Link>
            {notes.map((note) => (
                <Link to={`/note/${note.id}`} key={note.id}>
                    <h3>{note.title}</h3>
                    <p>{note.text}</p>
                </Link>   
            ))}
        </div>
        
    )
}