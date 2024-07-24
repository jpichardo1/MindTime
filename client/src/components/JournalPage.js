import React, { useState, useEffect } from 'react';
import JournalList from './JournalList';
import JournalForm from './JournalForm';

function JournalPage() {
  console.log('JournalPage render');  // Log render

  const [journals, setJournals] = useState([]);
  const [editingJournal, setEditingJournal] = useState(null);
  const dayId = 1; // Set the appropriate day_id based on your application logic

  useEffect(() => {
    console.log('useEffect triggered');  // Log useEffect

    const fetchJournals = async () => {
      console.log('fetchJournals called');  // Log fetchJournals call
      try {
        const response = await fetch('/journals');
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Fetched journals:', data);  // Log fetched data
        setJournals(data);
      } catch (error) {
        console.error('Error fetching journals:', error);
      }
    };

    fetchJournals();
  }, []); // Empty dependency array ensures this runs only once

  const handleSave = (newJournal) => {
    if (editingJournal) {
      setJournals(journals.map(journal => (journal.id === newJournal.id ? newJournal : journal)));
    } else {
      setJournals([...journals, newJournal]);
    }
    setEditingJournal(null);
  };

  const handleEdit = (journal) => {
    setEditingJournal(journal);
  };

  const handleDelete = async (id) => {
    try {
      const response = await fetch(`/journals/${id}`, {
        method: 'DELETE'
      });
      if (response.ok) {
        setJournals(journals.filter(journal => journal.id !== id));
      } else {
        console.error('Failed to delete journal entry');
      }
    } catch (error) {
      console.error('Error deleting journal entry:', error);
    }
  };

  return (
    <div>
      <h2>Journal Entries</h2>
      <JournalList journals={journals} onEdit={handleEdit} onDelete={handleDelete} />
      <h2>{editingJournal ? 'Edit Journal Entry' : 'Add New Journal Entry'}</h2>
      <JournalForm onSave={handleSave} dayId={dayId} journal={editingJournal} />
    </div>
  );
}

export default JournalPage;
