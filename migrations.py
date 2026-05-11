# migrations.py
from sqlalchemy import create_engine, text
from database import SQLALCHEMY_DATABASE_URL

def run_migrations():
    """
    Simple migration runner. 
    In a real app, use Alembic. This is a simplified version.
    """
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
    with engine.connect() as conn:
        # Example: Add a 'category' column to products if it doesn't exist
        # Note: SQLite syntax used here
        try:
            conn.execute(text("ALTER TABLE products ADD COLUMN category VARCHAR(50)"))
            print("Migration applied: Added 'category' column to products")
        except Exception as e:
            # Column likely already exists
            print(f"Migration skipped or failed: {e}")
        
        conn.commit()

if __name__ == "__main__":
    run_migrations()