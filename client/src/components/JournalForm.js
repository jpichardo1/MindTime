import React, { useState, useEffect } from 'react';

function JournalForm({ onSave, dayId, journal }) {
  console.log('JournalForm render');  // Log render

  const [content, setContent] = useState(journal ? journal.content : '');

  useEffect(() => {
    if (journal) {
      setContent(journal.content);
    }
  }, [journal]);

  async function handleSubmit(e) {
    e.preventDefault();
    console.log('handleSubmit called');  // Log handleSubmit
    try {
      const response = await fetch(journal ? `/journals/${journal.id}` : '/journals', {
        method: journal ? 'PATCH' : 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content,
          day_id: dayId,
        }),
      });
      if (response.ok) {
        const newJournal = await response.json();
        console.log('New journal added or updated:', newJournal);  // Log new journal
        onSave(newJournal);
        setContent('');  // Reset content after successful submission
      } else {
        console.error('Failed to save journal entry');
      }
    } catch (error) {
      console.error(error);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <textarea
        name="content"
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="Journal Content"
        required
      />
      <button type="submit">{journal ? 'Update Journal' : 'Save Journal'}</button>
    </form>
  );
}

export default JournalForm;
