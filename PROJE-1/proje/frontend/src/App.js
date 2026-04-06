import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [notes, setNotes] = useState([]);
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');

  const fetchNotes = async () => {
    try {
      const res = await axios.get('http://44.197.192.21:5000/api/notes');
      setNotes(res.data);
    } catch (error) {
      console.error("Notlar çekilemedi", error);
    }
  };

  useEffect(() => {
    fetchNotes();
  }, []);

  const addNote = async () => {
    if (!title) return alert("Başlık boş olamaz!");
    await axios.post('http://44.197.192.21:5000/api/notes', { title, content });
    setTitle('');
    setContent('');
    fetchNotes();
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.header}>☁️ Bulut Bilişim Not Defteri</h1>
      
      <div style={styles.formContainer}>
        <input 
          style={styles.input} 
          placeholder="Not Başlığı..." 
          value={title} 
          onChange={(e) => setTitle(e.target.value)} 
        />
        <textarea 
          style={styles.textarea} 
          placeholder="Not İçeriği..." 
          value={content} 
          onChange={(e) => setContent(e.target.value)} 
        />
        <button style={styles.button} onClick={addNote}>Kaydet</button>
      </div>

      <div style={styles.notesGrid}>
        {notes.map((note, index) => (
          <div key={index} style={styles.card}>
            <h3 style={styles.cardTitle}>{note.title}</h3>
            <p style={styles.cardContent}>{note.content}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

// Basit ve şık bir tasarım için CSS (Inline Styling)
const styles = {
  container: { fontFamily: 'Arial, sans-serif', maxWidth: '800px', margin: '0 auto', padding: '20px', backgroundColor: '#f4f7f6', minHeight: '100vh' },
  header: { textAlign: 'center', color: '#2c3e50', marginBottom: '30px' },
  formContainer: { display: 'flex', flexDirection: 'column', gap: '10px', backgroundColor: 'white', padding: '20px', borderRadius: '10px', boxShadow: '0 4px 6px rgba(0,0,0,0.1)', marginBottom: '30px' },
  input: { padding: '10px', fontSize: '16px', borderRadius: '5px', border: '1px solid #ccc' },
  textarea: { padding: '10px', fontSize: '16px', borderRadius: '5px', border: '1px solid #ccc', minHeight: '80px' },
  button: { padding: '12px', fontSize: '16px', backgroundColor: '#3498db', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer', fontWeight: 'bold' },
  notesGrid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))', gap: '20px' },
  card: { backgroundColor: 'white', padding: '15px', borderRadius: '10px', borderLeft: '5px solid #e74c3c', boxShadow: '0 2px 5px rgba(0,0,0,0.1)' },
  cardTitle: { margin: '0 0 10px 0', color: '#34495e' },
  cardContent: { margin: '0', color: '#7f8c8d' }
};

export default App;