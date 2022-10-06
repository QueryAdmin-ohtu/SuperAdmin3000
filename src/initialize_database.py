import os
from db import db
from app import create_app

app = create_app()
app.app_context().push()

def drop_tables():
    db.session.execute("""
        drop table if exists \"Admins\", \"Categories\", \"Category_results\", \"Industries\", \"Organizations\", \"Question_answers\",   \"Questions\", \"Survey_results\", \"Survey_user_groups\", \"Surveys\", \"User_answers\", \"Users\" cascade;
        """)
    db.session.commit()

def create_tables():
    os.system("psql -d test_superadmin -f schema.sql")

def initialize_database():
    drop_tables()
    create_tables()

if __name__ == "__main__":
    initialize_database()