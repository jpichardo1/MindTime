import React from 'react';
import JournalCard from './JournalCard';

function JournalList({ journals, onEdit, onDelete }) {
  console.log('JournalList render with journals:', journals);  // Log render and journals data
  return (
    <div>
      {journals.map(journal => (
        <JournalCard key={journal.id} journal={journal} onEdit={onEdit} onDelete={onDelete} />
      ))}
    </div>
  );
}

export default JournalList;
