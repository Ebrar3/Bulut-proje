import { useState, useEffect, useCallback } from "react";
import { notesService } from "./services/notesApi";
import NoteList from "./components/NoteList";
import NoteForm from "./components/NoteForm";
import NoteDetail from "./components/NoteDetail";
import "./App.css";

export default function App() {
  const [notes, setNotes] = useState([]);
  const [tags, setTags] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // UI state
  const [showForm, setShowForm] = useState(false);
  const [editingNote, setEditingNote] = useState(null);
  const [viewingNote, setViewingNote] = useState(null);

  // Filters
  const [search, setSearch] = useState("");
  const [activeTag, setActiveTag] = useState("");

  const fetchNotes = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const params = {};
      if (search) params.search = search;
      if (activeTag) params.tag = activeTag;
      const data = await notesService.getAll(params);
      setNotes(data);
    } catch {
      setError("Notlar yüklenemedi. Lütfen tekrar deneyin.");
    } finally {
      setLoading(false);
    }
  }, [search, activeTag]);

  const fetchTags = useCallback(async () => {
    try {
      const data = await notesService.getTags();
      setTags(data);
    } catch {
      // Tags are non-critical, ignore errors
    }
  }, []);

  useEffect(() => {
    fetchNotes();
  }, [fetchNotes]);

  useEffect(() => {
    fetchTags();
  }, [fetchTags, notes]);

  const handleCreate = async (noteData) => {
    try {
      await notesService.create(noteData);
      setShowForm(false);
      await fetchNotes();
    } catch {
      setError("Not oluşturulamadı.");
    }
  };

  const handleUpdate = async (noteData) => {
    try {
      await notesService.update(editingNote.id, noteData);
      setEditingNote(null);
      setShowForm(false);
      await fetchNotes();
    } catch {
      setError("Not güncellenemedi.");
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Bu notu silmek istediğinize emin misiniz?")) return;
    try {
      await notesService.delete(id);
      await fetchNotes();
    } catch {
      setError("Not silinemedi.");
    }
  };

  const handleEdit = (note) => {
    setEditingNote(note);
    setViewingNote(null);
    setShowForm(true);
  };

  const handleFormCancel = () => {
    setShowForm(false);
    setEditingNote(null);
  };

  const handleSearchChange = (e) => {
    setSearch(e.target.value);
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1>📝 Notlarım</h1>
          <button className="btn btn-primary" onClick={() => { setEditingNote(null); setShowForm(true); }}>
            + Yeni Not
          </button>
        </div>
        <div className="search-bar">
          <input
            type="search"
            placeholder="Notlarda ara..."
            value={search}
            onChange={handleSearchChange}
          />
        </div>
        {tags.length > 0 && (
          <div className="tag-filter">
            <button
              className={`tag ${activeTag === "" ? "tag-active" : ""}`}
              onClick={() => setActiveTag("")}
            >
              Tümü
            </button>
            {tags.map((tag) => (
              <button
                key={tag}
                className={`tag ${activeTag === tag ? "tag-active" : ""}`}
                onClick={() => setActiveTag(tag === activeTag ? "" : tag)}
              >
                {tag}
              </button>
            ))}
          </div>
        )}
      </header>

      <main className="app-main">
        {error && (
          <div className="error-banner">
            {error}
            <button onClick={() => setError(null)}>✕</button>
          </div>
        )}

        {showForm ? (
          <NoteForm
            initialData={editingNote}
            onSubmit={editingNote ? handleUpdate : handleCreate}
            onCancel={handleFormCancel}
          />
        ) : (
          <NoteList
            notes={notes}
            loading={loading}
            onEdit={handleEdit}
            onDelete={handleDelete}
            onView={(note) => setViewingNote(note)}
          />
        )}
      </main>

      {viewingNote && (
        <NoteDetail
          note={viewingNote}
          onClose={() => setViewingNote(null)}
          onEdit={(note) => { setViewingNote(null); handleEdit(note); }}
        />
      )}
    </div>
  );
}
