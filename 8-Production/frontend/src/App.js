import './App.css';
import NotesList from './NotesList'
import {Routes, Route} from 'react-router-dom'
import Note from './Note'
import Login from './Login'
import CreateAccount from './CreateAccount'
import {useState, useEffect} from 'react';

export async function getCSRFToken() {
  const response = await fetch('/api/get-csrf-token/', {
    credentials: 'include',
  });
  const data = await response.json();
  return data.csrfToken;
}

function App() {

  let [user, setUser] = useState({})


  useEffect(() => {
    getUser();
  },[])

  async function getUser(){
    let response = await fetch('/api/user')
    let data = await response.json()
    console.log(data)
    setUser(data)
    if (data.username === '' || response.status === 403) {
      if  (window.location.pathname !== "/login" && window.location.pathname !== "/createAccount"){
        window.location.replace('/login')
      }
    }
  }


  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<NotesList user={user}/>} />
        <Route path="/note/:id" element={<Note user={user}/>} />
        <Route path="/login" element={<Login />} />
        <Route path="/createAccount" element={<CreateAccount />} />
      </Routes>
    </div>
  );
}

export default App;
