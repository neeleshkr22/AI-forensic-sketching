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

# Sample data
sample_records = [
    {
        'record_id': str(uuid.uuid4()),
        'name': 'John Doe',
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
        'description': 'Suspected in multiple robbery cases',
        'aliases': ['JD', 'Johnny'],
        'tattoos': ['Dragon on left arm'],
        'scars': []
    },
    {
        'record_id': str(uuid.uuid4()),
        'name': 'Jane Smith',
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
        'description': 'Identity theft and financial fraud',
        'aliases': ['JS'],
        'tattoos': [],
        'scars': []
    },
    {
        'record_id': str(uuid.uuid4()),
        'name': 'Michael Johnson',
        'age': 42,
        'gender': 'Male',
        'height': 175,
        'weight': 85,
        'eye_color': 'Green',
        'hair_color': 'Brown',
        'crime_type': 'Assault',
        'crime_date': datetime(2023, 11, 5),
        'location': 'Chicago',
        'status': 'caught',
        'description': 'Arrested for assault charges',
        'aliases': ['Mike', 'MJ'],
        'tattoos': ['Star on neck'],
        'scars': ['Scar on right cheek']
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
