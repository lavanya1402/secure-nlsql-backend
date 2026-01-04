from src.db.database import engine, Base
from src.db import models  # noqa: F401

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("✅ DB initialized: project180.db")
