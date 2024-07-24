import React, { useState, useEffect } from 'react';

function TaskForm({ onSave, task }) {
  const [description, setDescription] = useState(task ? task.description : '');
  const [completed, setCompleted] = useState(task ? task.completed : false);
  const [dayId, setDayId] = useState(task ? task.day_id : '');

  async function handleSubmit(e) {
    e.preventDefault();
    const newTask = {
      description,
      completed,
      day_id: parseInt(dayId, 10)
    };
    onSave(newTask);
    setDescription('');
    setCompleted(false);
    setDayId('');
  }

  useEffect(() => {
    if (task) {
      setDescription(task.description);
      setCompleted(task.completed);
      setDayId(task.day_id);
    }
  }, [task]);

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder="Task Description"
        required
      />
      <input
        type="number"
        value={dayId}
        onChange={(e) => setDayId(e.target.value)}
        placeholder="Day ID"
        required
      />
      <label>
        Completed
        <input type="checkbox" checked={completed} onChange={(e) => setCompleted(e.target.checked)} />
      </label>
      <button type="submit">Save Task</button>
    </form>
  );
}

export default TaskForm;
