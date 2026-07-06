import React from 'react'

import "../styles/Note.css"
export default function Note({ note, onDelete, onSummarize, summary }) {
  const formattedDate = note.created_at
    ? new Date(note.created_at).toLocaleString()
    : "Date not available";

  return (
    <div className="note-container">
      <p className="note-title">{note.title}</p>
      <p className="note-content">{note.content}</p>
      <p className="note-date">{formattedDate}</p>
      {summary ? <p className="note-summary">{summary}</p> : null}
      <button className="delete-button" onClick={() => onDelete(note.id)}>
        Delete
      </button>
      <button className="delete-button" onClick={() => onSummarize(note.id)}>
        Summarize
      </button>
    </div>
  );
}
