import './App.css';
import NotesList from './NotesList'
import {Routes, Route} from 'react-router-dom'
import Note from './Note'
function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<NotesList />} />
        <Route path="/note/:id" element={<Note />} />
      </Routes>
    </div>
  );
}

export default App;
