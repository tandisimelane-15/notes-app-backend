from app import app
from models import db, User, Note
from faker import Faker
import random

fake = Faker()


def seed_data():
    with app.app_context():
        print("Clearing existing data...")
        Note.query.delete()
        User.query.delete()
        db.session.commit()

        print("Seeding users...")
        users = []
        for _ in range(5):
            user = User(username=fake.unique.user_name())
            user.password = "password123"  
            users.append(user)
            db.session.add(user)
        db.session.commit()

        print("Seeding notes...")
        for user in users:
            for _ in range(random.randint(3, 8)):
                note = Note(
                    title=fake.sentence(nb_words=4),
                    content=fake.paragraph(nb_sentences=3),
                    user_id=user.id,
                )
                db.session.add(note)
        db.session.commit()

        print(f"Seeded {len(users)} users, each with 3-8 notes.")
        print("Sample login -> username:", users[0].username, "| password: password123")


if __name__ == "__main__":
    seed_data()