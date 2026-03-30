export default function NoteCard({ note, onEdit, onDelete, onView }) {
  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleString("tr-TR", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const preview =
    note.content.length > 120
      ? note.content.slice(0, 120) + "..."
      : note.content;

  return (
    <div className="note-card" onClick={() => onView(note)}>
      <div className="note-card-header">
        <h3 className="note-title">{note.title}</h3>
        <div className="note-actions" onClick={(e) => e.stopPropagation()}>
          <button
            className="btn-icon"
            title="Düzenle"
            onClick={() => onEdit(note)}
          >
            ✏️
          </button>
          <button
            className="btn-icon btn-danger"
            title="Sil"
            onClick={() => onDelete(note.id)}
          >
            🗑️
          </button>
        </div>
      </div>
      <p className="note-preview">{preview}</p>
      {note.tags && note.tags.length > 0 && (
        <div className="note-tags">
          {note.tags.map((tag) => (
            <span key={tag} className="tag">
              {tag}
            </span>
          ))}
        </div>
      )}
      <p className="note-date">{formatDate(note.updated_at)}</p>
    </div>
  );
}
