import React, { useState, useEffect } from 'react';
import { Calendar as BigCalendar, dateFnsLocalizer } from 'react-big-calendar';
import format from 'date-fns/format';
import parse from 'date-fns/parse';
import startOfWeek from 'date-fns/startOfWeek';
import getDay from 'date-fns/getDay';
import 'react-big-calendar/lib/css/react-big-calendar.css';

const locales = {
  'en-US': require('date-fns/locale/en-US')
};

const localizer = dateFnsLocalizer({
  format,
  parse,
  startOfWeek,
  getDay,
  locales
});

function CalendarPage() {
  const [years, setYears] = useState([]);
  const [selectedYear, setSelectedYear] = useState(null);
  const [selectedMonth, setSelectedMonth] = useState(null);
  const [selectedDay, setSelectedDay] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [events, setEvents] = useState([]);

  useEffect(() => {
    async function fetchYears() {
      try {
        const response = await fetch('/years');
        const data = await response.json();
        setYears(data);
      } catch (error) {
        console.error(error);
      }
    }
    fetchYears();
  }, []);

  useEffect(() => {
    if (selectedYear) {
      async function fetchMonths() {
        try {
          const response = await fetch(`/years/${selectedYear.id}/months`);
          const data = await response.json();
          setSelectedYear(prev => ({ ...prev, months: data }));
        } catch (error) {
          console.error(error);
        }
      }
      fetchMonths();
    }
  }, [selectedYear]);

  useEffect(() => {
    if (selectedMonth) {
      async function fetchDays() {
        try {
          const response = await fetch(`/months/${selectedMonth.id}/days`);
          const data = await response.json();
          setSelectedMonth(prev => ({ ...prev, days: data }));
        } catch (error) {
          console.error(error);
        }
      }
      fetchDays();
    }
  }, [selectedMonth]);

  useEffect(() => {
    if (selectedDay) {
      async function fetchTasks() {
        try {
          const response = await fetch(`/days/${selectedDay.id}/tasks`);
          const data = await response.json();
          setTasks(data);
          const formattedEvents = data.map(task => ({
            title: task.description,
            start: new Date(task.start),
            end: new Date(task.end)
          }));
          setEvents(formattedEvents);
        } catch (error) {
          console.error(error);
        }
      }
      fetchTasks();
    }
  }, [selectedDay]);

  function handleSelectEvent(event) {
    // Handle event selection (e.g., open a modal for editing)
  }

  return (
    <div>
      <h1>Calendar</h1>
      <select onChange={e => setSelectedYear(years.find(y => y.id === parseInt(e.target.value)))}>
        <option value="">Select Year</option>
        {years.map(year => (
          <option key={year.id} value={year.id}>{year.year}</option>
        ))}
      </select>

      {selectedYear && (
        <select onChange={e => setSelectedMonth(selectedYear.months.find(m => m.id === parseInt(e.target.value)))}>
          <option value="">Select Month</option>
          {selectedYear.months.map(month => (
            <option key={month.id} value={month.id}>{month.month}</option>
          ))}
        </select>
      )}

      {selectedMonth && (
        <select onChange={e => setSelectedDay(selectedMonth.days.find(d => d.id === parseInt(e.target.value)))}>
          <option value="">Select Day</option>
          {selectedMonth.days.map(day => (
            <option key={day.id} value={day.id}>{day.day}</option>
          ))}
        </select>
      )}

      <BigCalendar
        localizer={localizer}
        events={events}
        startAccessor="start"
        endAccessor="end"
        style={{ height: 500 }}
        onSelectEvent={handleSelectEvent}
      />
    </div>
  );
}

export default CalendarPage;
