import { useState } from "react";

export default function NoteForm({ onSubmit, onCancel, initialData = null }) {
  const [title, setTitle] = useState(initialData?.title || "");
  const [content, setContent] = useState(initialData?.content || "");
  const [tagInput, setTagInput] = useState(
    initialData?.tags?.join(", ") || ""
  );
  const [error, setError] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!title.trim() || !content.trim()) {
      setError("Başlık ve içerik zorunludur.");
      return;
    }
    const tags = tagInput
      .split(",")
      .map((t) => t.trim())
      .filter(Boolean);
    onSubmit({ title: title.trim(), content: content.trim(), tags });
  };

  return (
    <form className="note-form" onSubmit={handleSubmit}>
      <h2>{initialData ? "Notu Düzenle" : "Yeni Not"}</h2>
      {error && <p className="form-error">{error}</p>}
      <div className="form-group">
        <label htmlFor="title">Başlık</label>
        <input
          id="title"
          type="text"
          placeholder="Not başlığı..."
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          maxLength={200}
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="content">İçerik</label>
        <textarea
          id="content"
          placeholder="Not içeriği..."
          value={content}
          onChange={(e) => setContent(e.target.value)}
          rows={8}
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="tags">Etiketler (virgülle ayırın)</label>
        <input
          id="tags"
          type="text"
          placeholder="aws, python, proje..."
          value={tagInput}
          onChange={(e) => setTagInput(e.target.value)}
        />
      </div>
      <div className="form-actions">
        <button type="submit" className="btn btn-primary">
          {initialData ? "Güncelle" : "Kaydet"}
        </button>
        <button type="button" className="btn btn-secondary" onClick={onCancel}>
          İptal
        </button>
      </div>
    </form>
  );
}
