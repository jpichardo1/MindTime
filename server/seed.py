#!/usr/bin/env python3

# Standard library imports
from datetime import datetime, timezone

# Local imports
from config import app, db, bcrypt
from models import User, Journal, Task, Year, Month, Day

if __name__ == '__main__':
    with app.app_context():
        print("Starting seed...")

        # Delete all records from tables
        User.query.delete()
        Journal.query.delete()
        Task.query.delete()
        Year.query.delete()
        Month.query.delete()
        Day.query.delete()

        # Create sample users
        user1 = User(username="alice", password_hash=bcrypt.generate_password_hash("password1").decode('utf-8'))
        user2 = User(username="bob", password_hash=bcrypt.generate_password_hash("password2").decode('utf-8'))
        user3 = User(username="charlie", password_hash=bcrypt.generate_password_hash("password3").decode('utf-8'))

        db.session.add_all([user1, user2, user3])
        db.session.commit()

        # Create sample years
        year1 = Year(year=2022)
        year2 = Year(year=2023)
        year3 = Year(year=2024)

        db.session.add_all([year1, year2, year3])
        db.session.commit()

        # Create sample months
        month1 = Month(month=1, year_id=year1.id)
        month2 = Month(month=2, year_id=year1.id)
        month3 = Month(month=3, year_id=year1.id)
        # Continue this pattern for all months and years...

        db.session.add_all([month1, month2, month3])
        db.session.commit()

        # Create sample days
        day1 = Day(day=1, month_id=month1.id)
        day2 = Day(day=2, month_id=month1.id)
        day3 = Day(day=3, month_id=month1.id)
        # Continue this pattern for all days...

        db.session.add_all([day1, day2, day3])
        db.session.commit()

        # Create sample journals
        journal1 = Journal(
            content="Today was a great day!",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            day_id=day1.id,
            user_id=user1.id
        )
        journal2 = Journal(
            content="I learned a lot of new things.",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            day_id=day2.id,
            user_id=user2.id
        )
        journal3 = Journal(
            content="Feeling grateful for everything.",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            day_id=day3.id,
            user_id=user3.id
        )
        # Continue this pattern for more journal entries...

        db.session.add_all([journal1, journal2, journal3])
        db.session.commit()

        # Create sample tasks
        task1 = Task(
            description="Complete the project report.",
            completed=True,
            day_id=day1.id
        )
        task2 = Task(
            description="Go grocery shopping.",
            completed=False,
            day_id=day2.id
        )
        task3 = Task(
            description="Clean the house.",
            completed=True,
            day_id=day3.id
        )
        # Continue this pattern for more tasks...

        db.session.add_all([task1, task2, task3])
        db.session.commit()

        print('Database seeded!')
