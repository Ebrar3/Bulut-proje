export default function NoteDetail({ note, onClose, onEdit }) {
  const formatDate = (dateStr) =>
    new Date(dateStr).toLocaleString("tr-TR", {
      year: "numeric",
      month: "long",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{note.title}</h2>
          <div className="modal-actions">
            <button className="btn-icon" onClick={() => onEdit(note)}>
              ✏️
            </button>
            <button className="btn-icon" onClick={onClose}>
              ✕
            </button>
          </div>
        </div>
        <div className="modal-body">
          <pre className="note-content-full">{note.content}</pre>
          {note.tags && note.tags.length > 0 && (
            <div className="note-tags">
              {note.tags.map((tag) => (
                <span key={tag} className="tag">
                  {tag}
                </span>
              ))}
            </div>
          )}
        </div>
        <div className="modal-footer">
          <span className="note-date">
            Oluşturuldu: {formatDate(note.created_at)}
          </span>
          <span className="note-date">
            Güncellendi: {formatDate(note.updated_at)}
          </span>
        </div>
      </div>
    </div>
  );
}
