# init_db.py
from app.db.session import engine, Base

def main():
    print("Creating all tables in the database...")
    Base.metadata.create_all(bind=engine)
    print("Done!")

if __name__ == "__main__":
    main()
