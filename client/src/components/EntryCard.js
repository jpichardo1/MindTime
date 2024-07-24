import React from 'react';

function EntryCard({ entry }) {
  if (!entry) {
    return null;
  }

  return (
    <div className="entry-card">
      <h3>{entry.title || 'No Title'}</h3>
      <p>{entry.content || 'No Content'}</p>
      <p>{new Date(entry.created_at).toLocaleString()}</p>
      <p>{new Date(entry.updated_at).toLocaleString()}</p>
      <button>Edit</button>
      <button>Delete</button>
    </div>
  );
}

export default EntryCard;
