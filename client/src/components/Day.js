import React from 'react';

function Day({ day, month, year, tasks, onSelectTask, onDeleteTask }) {
  return (
    <div className="day">
      <h3>{day}</h3>
      {tasks.map(task => (
        <div key={task.id} className="task">
          <span>{task.description}</span>
          <button onClick={() => onSelectTask(task)}>Edit</button>
          <button onClick={() => onDeleteTask(task.id)}>Delete</button>
        </div>
      ))}
    </div>
  );
}

export default Day;
