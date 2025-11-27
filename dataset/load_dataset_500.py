"""
Load 500 Criminal Records into MongoDB with Sketch Images
"""

import pandas as pd
import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

from database.db import get_db


def load_criminal_records_500():
    """Load 500 criminal records from CSV file into MongoDB"""
    
    # Read CSV file
    csv_path = Path(__file__).parent / 'criminal_records_500.csv'
    print(f"📂 Reading dataset from: {csv_path}")
    
    if not csv_path.exists():
        print(f"❌ File not found: {csv_path}")
        print(f"ℹ️  Run 'python generate_dataset_500.py' first to create the dataset")
        return
    
    df = pd.read_csv(csv_path)
    print(f"✅ Loaded {len(df)} records from CSV")
    
    # Connect to database
    db = get_db()
    collection = db.get_collection('criminal_records')
    
    # Clear existing records
    print("🗑️  Clearing existing records...")
    collection.delete_many({})
    
    # Insert records
    records_inserted = 0
    print("💾 Inserting records into MongoDB...")
    
    for idx, row in df.iterrows():
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
                'photo_url': row['sketch_url']  # Sketch-style image
            }
            
            collection.insert_one(record)
            records_inserted += 1
            
            # Progress indicator
            if records_inserted % 50 == 0:
                print(f"   Progress: {records_inserted}/{len(df)} records inserted...")
            
        except Exception as e:
            print(f"❌ Error inserting record {row['record_id']}: {e}")
    
    print(f"\n✅ Successfully inserted {records_inserted} records into MongoDB")
    
    # Show statistics
    male_count = collection.count_documents({'gender': 'Male'})
    female_count = collection.count_documents({'gender': 'Female'})
    
    # Get confidence statistics
    all_records = list(collection.find())
    confidence_scores = [r['confidence_score'] for r in all_records]
    
    print("\n📊 Dataset Statistics:")
    print(f"   Total Records: {records_inserted}")
    print(f"   Male Records: {male_count}")
    print(f"   Female Records: {female_count}")
    print(f"   Confidence Range: {min(confidence_scores):.2f} - {max(confidence_scores):.2f}")
    print(f"   Average Confidence: {sum(confidence_scores)/len(confidence_scores):.2f}")
    
    # Crime type distribution
    crime_counts = {}
    for record in all_records:
        crime = record['crime_type']
        crime_counts[crime] = crime_counts.get(crime, 0) + 1
    
    print("\n🔍 Top 10 Crime Types:")
    for crime, count in sorted(crime_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"   - {crime}: {count} records")
    
    # Show sample records with sketch URLs
    print("\n📝 Sample Records with Sketch Images:")
    for record in collection.find().limit(5):
        print(f"   - {record['name']} ({record['gender']}, {record['age']}) - {record['crime_type']} - {record['confidence_score']:.0%}")
        print(f"     Sketch URL: {record['photo_url']}")


if __name__ == '__main__':
    try:
        print("🚀 Starting Criminal Records Dataset Loader (500 records)...")
        load_criminal_records_500()
        print("\n✅ Dataset loaded successfully!")
        print("\nℹ️  Sketch images will be displayed in the frontend at:")
        print("   http://localhost:5173/results")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
