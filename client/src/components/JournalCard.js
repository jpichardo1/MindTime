import React from 'react';

function JournalCard({ journal, onEdit, onDelete }) {
  console.log('JournalCard render', journal);  // Log render and journal data
  return (
    <div className="journal-card">
      <h3>{journal.title}</h3>
      <p>{journal.content}</p>
      <p>{new Date(journal.created_at).toLocaleString()}</p>
      <p>{new Date(journal.updated_at).toLocaleString()}</p>
      <button onClick={() => onEdit(journal)}>Edit</button>
      <button onClick={() => onDelete(journal.id)}>Delete</button>
    </div>
  );
}

export default JournalCard;
