"""
Generate 500 Criminal Records with Sketch-style Images
Creates a comprehensive dataset with realistic sketch portraits
"""

import pandas as pd
import random
from datetime import datetime, timedelta

# Expanded name lists
male_first_names = [
    'James', 'John', 'Robert', 'Michael', 'William', 'David', 'Richard', 'Joseph', 'Thomas', 'Christopher',
    'Charles', 'Daniel', 'Matthew', 'Anthony', 'Mark', 'Donald', 'Steven', 'Andrew', 'Paul', 'Joshua',
    'Kenneth', 'Kevin', 'Brian', 'George', 'Timothy', 'Ronald', 'Edward', 'Jason', 'Jeffrey', 'Ryan',
    'Jacob', 'Gary', 'Nicholas', 'Eric', 'Jonathan', 'Stephen', 'Larry', 'Justin', 'Scott', 'Brandon',
    'Benjamin', 'Samuel', 'Raymond', 'Gregory', 'Alexander', 'Patrick', 'Frank', 'Dennis', 'Jerry', 'Tyler',
    'Aaron', 'Jose', 'Adam', 'Nathan', 'Henry', 'Zachary', 'Douglas', 'Peter', 'Kyle', 'Noah',
    'Ethan', 'Jeremy', 'Christian', 'Walter', 'Keith', 'Austin', 'Roger', 'Terry', 'Sean', 'Gerald',
    'Carl', 'Harold', 'Dylan', 'Arthur', 'Lawrence', 'Jordan', 'Jesse', 'Bryan', 'Billy', 'Bruce',
    'Albert', 'Willie', 'Gabriel', 'Logan', 'Alan', 'Juan', 'Wayne', 'Elijah', 'Randy', 'Roy',
    'Vincent', 'Ralph', 'Eugene', 'Russell', 'Bobby', 'Mason', 'Philip', 'Louis', 'Marcus', 'Travis'
]

female_first_names = [
    'Mary', 'Patricia', 'Jennifer', 'Linda', 'Barbara', 'Elizabeth', 'Susan', 'Jessica', 'Sarah', 'Karen',
    'Lisa', 'Nancy', 'Betty', 'Margaret', 'Sandra', 'Ashley', 'Kimberly', 'Emily', 'Donna', 'Michelle',
    'Carol', 'Amanda', 'Dorothy', 'Melissa', 'Deborah', 'Stephanie', 'Rebecca', 'Sharon', 'Laura', 'Cynthia',
    'Kathleen', 'Amy', 'Angela', 'Shirley', 'Anna', 'Brenda', 'Pamela', 'Emma', 'Nicole', 'Helen',
    'Samantha', 'Katherine', 'Christine', 'Debra', 'Rachel', 'Carolyn', 'Janet', 'Catherine', 'Maria', 'Heather',
    'Diane', 'Ruth', 'Julie', 'Olivia', 'Joyce', 'Virginia', 'Victoria', 'Kelly', 'Lauren', 'Christina',
    'Joan', 'Evelyn', 'Judith', 'Megan', 'Andrea', 'Cheryl', 'Hannah', 'Jacqueline', 'Martha', 'Gloria',
    'Teresa', 'Ann', 'Sara', 'Madison', 'Frances', 'Kathryn', 'Janice', 'Jean', 'Abigail', 'Alice',
    'Brittany', 'Sophia', 'Isabella', 'Charlotte', 'Marie', 'Janet', 'Rose', 'Diana', 'Judy', 'Grace',
    'Danielle', 'Marilyn', 'Beverly', 'Amber', 'Theresa', 'Denise', 'Tammy', 'Michelle', 'Irene', 'Jane'
]

last_names = [
    'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
    'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin',
    'Lee', 'Perez', 'Thompson', 'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson',
    'Walker', 'Young', 'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores',
    'Green', 'Adams', 'Nelson', 'Baker', 'Hall', 'Rivera', 'Campbell', 'Mitchell', 'Carter', 'Roberts',
    'Gomez', 'Phillips', 'Evans', 'Turner', 'Diaz', 'Parker', 'Cruz', 'Edwards', 'Collins', 'Reyes',
    'Stewart', 'Morris', 'Morales', 'Murphy', 'Cook', 'Rogers', 'Gutierrez', 'Ortiz', 'Morgan', 'Cooper',
    'Peterson', 'Bailey', 'Reed', 'Kelly', 'Howard', 'Ramos', 'Kim', 'Cox', 'Ward', 'Richardson',
    'Watson', 'Brooks', 'Chavez', 'Wood', 'James', 'Bennett', 'Gray', 'Mendoza', 'Ruiz', 'Hughes',
    'Price', 'Alvarez', 'Castillo', 'Sanders', 'Patel', 'Myers', 'Long', 'Ross', 'Foster', 'Jimenez'
]

cities = [
    'New York NY', 'Los Angeles CA', 'Chicago IL', 'Houston TX', 'Phoenix AZ', 'Philadelphia PA',
    'San Antonio TX', 'San Diego CA', 'Dallas TX', 'San Jose CA', 'Austin TX', 'Jacksonville FL',
    'Fort Worth TX', 'Columbus OH', 'Charlotte NC', 'San Francisco CA', 'Indianapolis IN', 'Seattle WA',
    'Denver CO', 'Washington DC', 'Boston MA', 'El Paso TX', 'Nashville TN', 'Detroit MI', 'Oklahoma City OK',
    'Portland OR', 'Las Vegas NV', 'Memphis TN', 'Louisville KY', 'Baltimore MD', 'Milwaukee WI',
    'Albuquerque NM', 'Tucson AZ', 'Fresno CA', 'Sacramento CA', 'Kansas City MO', 'Mesa AZ', 'Atlanta GA',
    'Omaha NE', 'Colorado Springs CO', 'Raleigh NC', 'Miami FL', 'Long Beach CA', 'Virginia Beach VA',
    'Oakland CA', 'Minneapolis MN', 'Tulsa OK', 'Tampa FL', 'Arlington TX', 'New Orleans LA'
]

crime_types = [
    'Assault', 'Armed Robbery', 'Burglary', 'Theft', 'Grand Theft Auto', 'Fraud', 'Embezzlement',
    'Drug Trafficking', 'Drug Possession', 'Murder', 'Manslaughter', 'Kidnapping', 'Extortion',
    'Money Laundering', 'Identity Theft', 'Cybercrime', 'Arson', 'Vandalism', 'Battery',
    'Domestic Violence', 'Sexual Assault', 'Stalking', 'Harassment', 'Trespassing', 'Breaking and Entering'
]

statuses = ['Wanted', 'Under Investigation', 'Wanted', 'Wanted', 'Under Investigation']

# Physical descriptors
hair_colors = ['black', 'brown', 'blonde', 'gray', 'red', 'dark brown', 'light brown', 'white', 'salt and pepper']
eye_colors = ['brown', 'blue', 'green', 'hazel', 'gray', 'amber']
builds = ['slim', 'athletic', 'medium', 'heavy', 'muscular', 'stocky', 'lean']
heights_male = ["5'8\"", "5'9\"", "5'10\"", "5'11\"", "6'0\"", "6'1\"", "6'2\"", "6'3\""]
heights_female = ["5'2\"", "5'3\"", "5'4\"", "5'5\"", "5'6\"", "5'7\"", "5'8\"", "5'9\""]

# Features
facial_features = [
    'scar on left cheek', 'scar on right eyebrow', 'broken nose', 'mole on chin', 'dimples',
    'prominent jaw', 'high cheekbones', 'thick eyebrows', 'thin lips', 'full lips',
    'pierced ears', 'pierced nose', 'facial tattoo', 'neck tattoo', 'missing tooth',
    'crooked smile', 'deep-set eyes', 'wide-set eyes', 'prominent forehead', 'receding hairline'
]

accessories = ['glasses', 'sunglasses', 'baseball cap', 'beanie', 'hood', 'bandana']

def generate_description(gender, age, name):
    """Generate realistic physical description"""
    hair = random.choice(hair_colors)
    eyes = random.choice(eye_colors)
    build = random.choice(builds)
    height = random.choice(heights_male if gender == 'Male' else heights_female)
    
    age_desc = 'early' if age < 30 else 'mid' if age < 40 else 'late'
    decade = f"{age // 10}0s"
    
    desc = f"{gender} in {age_desc}-{decade} with {hair} hair, {eyes} eyes, {build} build, approximately {height} tall."
    
    # Add distinguishing features (70% chance)
    if random.random() > 0.3:
        feature = random.choice(facial_features)
        desc += f" {feature.capitalize()}."
    
    # Add accessories (40% chance)
    if random.random() > 0.6:
        accessory = random.choice(accessories)
        desc += f" Often seen wearing {accessory}."
    
    return desc

def generate_sketch_url(gender, index):
    """Generate sketch-style image URLs"""
    # Using DiceBear API for sketch-style avatars
    seed = f"criminal-{gender.lower()}-{index}"
    style = random.choice(['avataaars', 'bottts', 'micah', 'adventurer', 'lorelei', 'notionists'])
    return f"https://api.dicebear.com/7.x/{style}/svg?seed={seed}&backgroundColor=f0f0f0&size=256"

def generate_dataset(num_records=500):
    """Generate criminal records dataset"""
    records = []
    
    for i in range(num_records):
        # Alternate between male and female for balance
        gender = 'Male' if i % 2 == 0 else 'Female'
        
        # Generate name
        first_name = random.choice(male_first_names if gender == 'Male' else female_first_names)
        last_name = random.choice(last_names)
        name = f"{first_name} {last_name}"
        
        # Generate age (18-65)
        age = random.randint(18, 65)
        
        # Generate record ID
        record_id = f"CR{2024}{str(i+1).zfill(4)}"
        
        # Generate dates
        days_ago = random.randint(30, 730)
        date_added = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        last_seen = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
        
        # Generate confidence score (60-98%)
        # Higher indices get lower scores for variety
        base_score = 0.98 - (i * 0.0007)  # Gradually decrease
        confidence = max(0.60, min(0.98, base_score + random.uniform(-0.05, 0.05)))
        
        # Generate description
        description = generate_description(gender, age, name)
        
        # Generate sketch image URL
        sketch_url = generate_sketch_url(gender, i)
        
        record = {
            'record_id': record_id,
            'name': name,
            'age': age,
            'gender': gender,
            'crime_type': random.choice(crime_types),
            'location': random.choice(cities),
            'status': random.choice(statuses),
            'description': description,
            'confidence_score': round(confidence, 2),
            'date_added': date_added,
            'last_seen': last_seen,
            'sketch_url': sketch_url
        }
        
        records.append(record)
    
    return pd.DataFrame(records)

if __name__ == '__main__':
    print("🚀 Generating 500 Criminal Records with Sketch Images...")
    
    # Generate dataset
    df = generate_dataset(500)
    
    # Save to CSV
    csv_path = 'criminal_records_500.csv'
    df.to_csv(csv_path, index=False)
    
    print(f"✅ Generated {len(df)} records")
    print(f"📁 Saved to: {csv_path}")
    
    # Show statistics
    print("\n📊 Dataset Statistics:")
    print(f"   Total Records: {len(df)}")
    print(f"   Male Records: {len(df[df['gender'] == 'Male'])}")
    print(f"   Female Records: {len(df[df['gender'] == 'Female'])}")
    print(f"   Confidence Range: {df['confidence_score'].min():.2f} - {df['confidence_score'].max():.2f}")
    print(f"   Crime Types: {df['crime_type'].nunique()}")
    print(f"   Locations: {df['location'].nunique()}")
    
    # Show sample records
    print("\n📝 Sample Records:")
    for _, row in df.head(5).iterrows():
        print(f"   - {row['record_id']}: {row['name']} ({row['gender']}, {row['age']}) - {row['crime_type']} - {row['confidence_score']:.0%}")
        print(f"     Sketch: {row['sketch_url']}")
    
    print(f"\n✅ Dataset ready! Run load_dataset_500.py to import into MongoDB")
