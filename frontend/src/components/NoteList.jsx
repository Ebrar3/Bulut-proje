import NoteCard from "./NoteCard";

export default function NoteList({ notes, loading, onEdit, onDelete, onView }) {
  if (loading) {
    return (
      <div className="loading">
        <span className="spinner" />
        <p>Notlar yükleniyor...</p>
      </div>
    );
  }

  if (notes.length === 0) {
    return (
      <div className="empty-state">
        <p>📝 Henüz not yok. İlk notunuzu ekleyin!</p>
      </div>
    );
  }

  return (
    <div className="notes-grid">
      {notes.map((note) => (
        <NoteCard
          key={note.id}
          note={note}
          onEdit={onEdit}
          onDelete={onDelete}
          onView={onView}
        />
      ))}
    </div>
  );
}
