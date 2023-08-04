import { useParams, Link, redirect} from "react-router-dom";
import {useState, useEffect} from 'react';
import { getCSRFToken } from "./App"

//THIS IS IMPORTANT!!! For the input "value" attribute, I first used "note?.title", but it didn't update the screen. It's because we must reset the note STATE, which we don't do every keystroke.
export default function Note({user}){
    let noteId = useParams()['id']
    let [note, setNote] = useState({title: '', text: ''})

    useEffect(() => {
        getNote()
    }, [])

    async function getNote(){
        if (noteId == "new"){ // If creating new note, don't fetch a note
            return 0;
        }
        let response = await fetch(`/api/note/${noteId}`) // GET
        let data = await response.json()
        console.log(data)
        setNote(data)
    }

    async function createNote(e){
        e.preventDefault()
        const csrfToken = await getCSRFToken()
        let response = await fetch(`/api/note/${noteId}`, {
            method: "POST",
            headers: {
                "Content-type": "application/json",
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify(note)
        })
        let data = await response.json()
        console.log(data)
        window.location.replace('/')
    }

    async function updateNote(e){
        e.preventDefault()
        const csrfToken = await getCSRFToken()
        let response = await fetch(`/api/note/${noteId}`, { // PUT
            method: "PUT",
            headers: {
                "Content-type": "application/json",
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify(note)
        })
        let data = await response.json()
        console.log(data)
        window.location.replace('/')
    }

    async function deleteNote(){ // An issue is after deleting the note and sending me back to Notes List, the deleted note is still there because it didn't refresh the page!!
        const csrfToken = await getCSRFToken()
        let response = await fetch(`/api/note/${noteId}`, {
            method: "DELETE",
            headers: {
                'X-CSRFToken': csrfToken,
            },
        })
        let data = await response.json()
        console.log(data)
        window.location.replace('/')
    }


    return (
        <div>
            <Link to="/">Notes List</Link>
            <br />
            {noteId != "new" && (<Link onClick={deleteNote}>Delete Note</Link>)}
            <form>
                <label>Title: </label>
                <input type="text" value={note.title} onChange={e => setNote({...note, title: e.target.value})}/>
                <br />
                <label>Text:</label>
                <input type="text" value={note.text} onChange={e => setNote({...note, text: e.target.value})}/>
                <br />
                {noteId === "new" ? (<input type="submit" onClick={createNote} value="Create Note" />): (<input type="submit" onClick={updateNote} value="Update Note" />)}
            </form>
        </div>
    )
}