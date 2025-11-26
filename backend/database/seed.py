"""
Database Seeding Script
Creates sample criminal records for testing
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import get_db
from database.repository import RecordRepository
from datetime import datetime
import uuid

# Sample data - Enhanced with diverse records
sample_records = [
    {
        'record_id': str(uuid.uuid4()),
        'name': 'John Anderson',
        'age': 35,
        'gender': 'Male',
        'height': 180,
        'weight': 75,
        'eye_color': 'Brown',
        'hair_color': 'Black',
        'crime_type': 'Robbery',
        'crime_date': datetime(2024, 1, 15),
        'location': 'New York',
        'status': 'active',
        'description': 'Male, 30s, short black hair, brown eyes, beard',
        'aliases': ['JD', 'Johnny'],
        'tattoos': ['Dragon on left arm'],
        'scars': []
    },
    {
        'record_id': str(uuid.uuid4()),
        'name': 'Sarah Williams',
        'age': 28,
        'gender': 'Female',
        'height': 165,
        'weight': 60,
        'eye_color': 'Blue',
        'hair_color': 'Blonde',
        'crime_type': 'Fraud',
        'crime_date': datetime(2024, 3, 10),
        'location': 'Los Angeles',
        'status': 'active',
        'description': 'Female, 20s, long blonde hair, blue eyes, oval face',
        'aliases': ['Sarah J'],
        'tattoos': [],
        'scars': []
    },
    {
        'record_id': str(uuid.uuid4()),
        'name': 'Michael Chen',
        'age': 42,
        'gender': 'Male',
        'height': 175,
        'weight': 85,
        'eye_color': 'Brown',
        'hair_color': 'Black',
        'crime_type': 'Assault',
        'crime_date': datetime(2023, 11, 5),
        'location': 'Chicago',
        'status': 'caught',
        'description': 'Male, 40s, short black hair, narrow eyes',
        'aliases': ['Mike', 'MC'],
        'tattoos': ['Star on neck'],
        'scars': ['Scar on right cheek']
    },
    {
        'record_id': str(uuid.uuid4()),
        'name': 'Emily Rodriguez',
        'age': 31,
        'gender': 'Female',
        'height': 168,
        'weight': 62,
        'eye_color': 'Brown',
        'hair_color': 'Dark Brown',
        'crime_type': 'Theft',
        'crime_date': datetime(2024, 5, 20),
        'location': 'Miami',
        'status': 'active',
        'description': 'Female, 30s, curly brown hair, brown eyes',
        'aliases': ['Em', 'Emmy'],
        'tattoos': ['Rose on shoulder'],
        'scars': []
    },
    {
        'record_id': str(uuid.uuid4()),
        'name': 'David Martinez',
        'age': 29,
        'gender': 'Male',
        'height': 178,
        'weight': 72,
        'eye_color': 'Hazel',
        'hair_color': 'Brown',
        'crime_type': 'Burglary',
        'crime_date': datetime(2024, 2, 14),
        'location': 'Houston',
        'status': 'active',
        'description': 'Male, late 20s, wavy brown hair, hazel eyes',
        'aliases': ['Dave'],
        'tattoos': [],
        'scars': ['Scar above left eyebrow']
    },
    {
        'record_id': str(uuid.uuid4()),
        'name': 'Lisa Thompson',
        'age': 26,
        'gender': 'Female',
        'height': 170,
        'weight': 58,
        'eye_color': 'Green',
        'hair_color': 'Red',
        'crime_type': 'Vandalism',
        'crime_date': datetime(2024, 4, 8),
        'location': 'Seattle',
        'status': 'active',
        'description': 'Female, mid 20s, short red hair, green eyes',
        'aliases': ['Liz'],
        'tattoos': ['Butterfly on ankle'],
        'scars': []
    },
    {
        'record_id': str(uuid.uuid4()),
        'name': 'Robert Taylor',
        'age': 38,
        'gender': 'Male',
        'height': 185,
        'weight': 90,
        'eye_color': 'Blue',
        'hair_color': 'Blonde',
        'crime_type': 'Drug Trafficking',
        'crime_date': datetime(2023, 9, 22),
        'location': 'Phoenix',
        'status': 'active',
        'description': 'Male, late 30s, short blonde hair, blue eyes, beard',
        'aliases': ['Rob', 'Bobby'],
        'tattoos': ['Skull on right arm'],
        'scars': ['Scar on chin']
    },
    {
        'record_id': str(uuid.uuid4()),
        'name': 'Amanda Foster',
        'age': 33,
        'gender': 'Female',
        'height': 163,
        'weight': 55,
        'eye_color': 'Brown',
        'hair_color': 'Black',
        'crime_type': 'Embezzlement',
        'crime_date': datetime(2024, 6, 3),
        'location': 'Boston',
        'status': 'active',
        'description': 'Female, early 30s, straight black hair, brown eyes, glasses',
        'aliases': ['Mandy'],
        'tattoos': [],
        'scars': []
    },
]

def seed_database():
    """Seed database with sample records"""
    print("Seeding database...")
    
    try:
        repo = RecordRepository()
        
        for record in sample_records:
            try:
                repo.create(record)
                print(f"✓ Created record: {record['name']}")
            except Exception as e:
                print(f"✗ Error creating {record['name']}: {str(e)}")
        
        print(f"\n✓ Database seeded successfully with {len(sample_records)} records")
        
    except Exception as e:
        print(f"✗ Error seeding database: {str(e)}")

if __name__ == '__main__':
    seed_database()
