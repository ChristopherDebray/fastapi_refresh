# seeds/run_seeds.py
import sys
sys.path.append('/app')

from app.db.database import SessionLocal
from app.module.user.infrastructure.persistence.user_model import UserModel
from seeds.data.users import USERS

def seed_users(db):
    if db.query(UserModel).count() > 0:
        print("Users already seeded, skipping.")
        return
    
    for data in USERS:
        user = UserModel(**data)
        db.add(user)
    
    db.commit()
    print(f"Seeded {len(USERS)} users.")

def run():
    db = SessionLocal()
    try:
        seed_users(db)
    finally:
        db.close()

if __name__ == "__main__":
    run()