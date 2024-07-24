import React, { useState, useEffect } from 'react';  // Add useEffect here
import DatePicker from 'react-datepicker';
import DailyEntries from './DailyEntries';
import DailyTasks from './DailyTasks';
import 'react-datepicker/dist/react-datepicker.css';

function DailyPage() {
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [entries, setEntries] = useState([]);
  const [tasks, setTasks] = useState([]);

  async function handleDateChange(date) {
    setSelectedDate(date);
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const day = date.getDate();

    try {
      const entryResponse = await fetch(`/journals?year=${year}&month=${month}&day=${day}`);
      const entriesData = await entryResponse.json();
      console.log('Fetched entries:', entriesData);  // Log fetched data
      setEntries(Array.isArray(entriesData) ? entriesData : []);

      const taskResponse = await fetch(`/tasks?year=${year}&month=${month}&day=${day}`);
      const tasksData = await taskResponse.json();
      console.log('Fetched tasks:', tasksData);  // Log fetched data
      setTasks(Array.isArray(tasksData) ? tasksData : []);
    } catch (error) {
      console.error('Error fetching data:', error);
      setEntries([]);
      setTasks([]);
    }
  }

  useEffect(() => {
    handleDateChange(selectedDate); // Fetch data for the initial date
  }, []);

  return (
    <div>
      <DatePicker selected={selectedDate} onChange={handleDateChange} />
      <DailyEntries entries={entries} />
      <DailyTasks tasks={tasks} />
    </div>
  );
}

export default DailyPage;
