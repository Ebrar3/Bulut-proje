import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [notes, setNotes] = useState([]);
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');

  const fetchNotes = async () => {
    const res = await axios.get('http://44.197.192.21:5000/api/notes');
    setNotes(res.data);
  };

  useEffect(() => {
    fetchNotes();
  }, []);

  const addNote = async () => {
    await axios.post('http://44.197.192.21:5000/api/notes', { title, content });
    setTitle('');
    setContent('');
    fetchNotes();
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Bulut Bilişim Not Defteri</h1>

      <input
        placeholder="Başlık"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />

      <br />

      <textarea
        placeholder="İçerik"
        value={content}
        onChange={(e) => setContent(e.target.value)}
      />

      <br />

      <button onClick={addNote}>Notu Kaydet</button>

      <hr />

      <h2>Notlarım</h2>

      {notes.map((note, index) => (
        <div key={index}>
          <h3>{note.title}</h3>
          <p>{note.content}</p>
        </div>
      ))}
    </div>
  );
}

export default App;