"""
Criminal Records Dataset Loader
Loads criminal records from CSV into MongoDB
"""

import pandas as pd
import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

from database.db import get_db
from database.models import CriminalRecord
from datetime import datetime


def load_criminal_records():
    """Load criminal records from CSV file into MongoDB"""
    
    # Read CSV file
    csv_path = Path(__file__).parent / 'criminal_records.csv'
    print(f"📂 Reading dataset from: {csv_path}")
    
    df = pd.read_csv(csv_path)
    print(f"✅ Loaded {len(df)} records from CSV")
    
    # Connect to database
    db = get_db()
    collection = db['criminal_records']
    
    # Clear existing records
    print("🗑️  Clearing existing records...")
    collection.delete_many({})
    
    # Insert records
    records_inserted = 0
    for _, row in df.iterrows():
        try:
            record = {
                'record_id': row['record_id'],
                'name': row['name'],
                'age': int(row['age']),
                'gender': row['gender'],
                'crime_type': row['crime_type'],
                'location': row['location'],
                'status': row['status'],
                'description': row['description'],
                'confidence_score': float(row['confidence_score']),
                'date_added': row['date_added'],
                'last_seen': row['last_seen'],
                'features': [],  # Placeholder for facial features
                'photo_url': f"https://randomuser.me/api/portraits/{'men' if row['gender'] == 'Male' else 'women'}/{records_inserted % 90}.jpg"
            }
            
            collection.insert_one(record)
            records_inserted += 1
            
        except Exception as e:
            print(f"❌ Error inserting record {row['record_id']}: {e}")
    
    print(f"✅ Successfully inserted {records_inserted} records into MongoDB")
    
    # Show statistics
    male_count = collection.count_documents({'gender': 'Male'})
    female_count = collection.count_documents({'gender': 'Female'})
    
    print("\n📊 Dataset Statistics:")
    print(f"   Total Records: {records_inserted}")
    print(f"   Male Records: {male_count}")
    print(f"   Female Records: {female_count}")
    print(f"   Confidence Range: {df['confidence_score'].min():.2f} - {df['confidence_score'].max():.2f}")
    
    # Show sample records
    print("\n📝 Sample Records:")
    for record in collection.find().limit(3):
        print(f"   - {record['name']} ({record['gender']}, {record['age']}) - {record['crime_type']} - {record['confidence_score']:.2%}")


if __name__ == '__main__':
    try:
        print("🚀 Starting Criminal Records Dataset Loader...")
        load_criminal_records()
        print("\n✅ Dataset loaded successfully!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
