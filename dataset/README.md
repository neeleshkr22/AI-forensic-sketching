# 📊 Criminal Records Dataset

## Overview
This dataset contains **24 synthetic criminal records** for testing the AI Criminal Sketch Matching System.

## Dataset Statistics
- **Total Records:** 24
- **Male Records:** 12
- **Female Records:** 12
- **Confidence Score Range:** 0.61 - 0.95
- **Crime Types:** Assault, Fraud, Robbery, Theft, Drug Trafficking, Burglary, Murder, Kidnapping, Arson, Embezzlement, and more

## File Structure
```
dataset/
├── criminal_records.csv       # Main dataset file
├── load_dataset.py           # Python script to load data into MongoDB
└── README.md                 # This file
```

## Dataset Schema

| Column | Type | Description |
|--------|------|-------------|
| record_id | String | Unique criminal record ID (e.g., CR2024001) |
| name | String | Full name of the person |
| age | Integer | Age of the person |
| gender | String | Gender (Male/Female) |
| crime_type | String | Type of crime committed |
| location | String | Location/jurisdiction |
| status | String | Current status (Wanted/Under Investigation) |
| description | String | Detailed physical description |
| confidence_score | Float | Confidence score (0.0-1.0) |
| date_added | String | Date record was added (YYYY-MM-DD) |
| last_seen | String | Last seen date (YYYY-MM-DD) |

## Sample Records

### Male Records
1. **John Anderson** (95%) - Assault, Los Angeles
2. **Michael Chen** (89%) - Fraud, San Francisco
3. **David Martinez** (84%) - Drug Trafficking, Chicago
4. **Robert Taylor** (79%) - Burglary, Houston
5. **James Wilson** (73%) - Armed Robbery, Phoenix
6. **Carlos Hernandez** (68%) - Theft, Miami

### Female Records
1. **Sarah Williams** (93%) - Robbery, New York
2. **Emily Rodriguez** (87%) - Theft, Miami
3. **Lisa Thompson** (82%) - Fraud, Boston
4. **Amanda Foster** (76%) - Embezzlement, Seattle
5. **Jessica Martinez** (71%) - Identity Theft, Denver
6. **Rachel Kim** (65%) - Assault, Portland

## Loading Dataset into MongoDB

### Prerequisites
- MongoDB running on localhost:27017
- Python environment with pandas installed

### Steps
1. Navigate to dataset directory:
   ```bash
   cd "c:\Users\mrana\OneDrive\Desktop\Major project final\dataset"
   ```

2. Install pandas if not already installed:
   ```bash
   pip install pandas
   ```

3. Run the loader script:
   ```bash
   python load_dataset.py
   ```

### Expected Output
```
🚀 Starting Criminal Records Dataset Loader...
📂 Reading dataset from: criminal_records.csv
✅ Loaded 24 records from CSV
🗑️  Clearing existing records...
✅ Successfully inserted 24 records into MongoDB

📊 Dataset Statistics:
   Total Records: 24
   Male Records: 12
   Female Records: 12
   Confidence Range: 0.61 - 0.95

📝 Sample Records:
   - John Anderson (Male, 35) - Assault - 95.00%
   - Michael Chen (Male, 42) - Fraud - 89.00%
   - David Martinez (Male, 38) - Drug Trafficking - 84.00%

✅ Dataset loaded successfully!
```

## Data Distribution

### By Gender
- Male: 12 records (50%)
- Female: 12 records (50%)

### By Confidence Score
- High (≥0.90): 3 records
- Medium-High (0.80-0.89): 6 records
- Medium (0.70-0.79): 6 records
- Low (<0.70): 9 records

### By Crime Type
- Violent Crimes: 8 records (Assault, Murder, Armed Robbery, Kidnapping)
- Property Crimes: 6 records (Theft, Burglary, Robbery, Arson)
- Financial Crimes: 6 records (Fraud, Embezzlement, Money Laundering)
- Drug-Related: 4 records (Drug Trafficking, Drug Possession)

## Use Cases

### 1. Gender-Based Filtering
Test the system's ability to filter results by gender:
- Male sketch → Should return only 12 male records
- Female sketch → Should return only 12 female records

### 2. Threshold Testing
Test the intelligent threshold system:
- Threshold ≥90%: 3 records (John 95%, Sarah 93%, Marcus 91%)
- Threshold ≥80%: 9 records
- Threshold ≥70%: 15 records
- Threshold ≥60%: 24 records (all)

### 3. Search Accuracy
Test search accuracy with different confidence scores:
- High confidence matches (>90%): Most accurate identifications
- Medium confidence (70-89%): Good suspects for investigation
- Low confidence (<70%): Potential leads requiring further verification

## Data Generation

This is a **synthetic dataset** created for educational and demonstration purposes. The records are fictional and do not represent real individuals.

### Data Sources
- Names: Randomly generated common names
- Locations: Major US cities
- Descriptions: Generic physical descriptions
- Confidence Scores: Distributed across realistic range (0.61-0.95)
- Photo URLs: Placeholder images from randomuser.me API

## Notes

⚠️ **Important:** This dataset is for testing and demonstration purposes only. It contains fictional criminal records and should not be used for any real law enforcement activities.

✅ **Benefits:**
- Balanced gender representation
- Realistic confidence score distribution
- Diverse crime types
- Geographic diversity
- Suitable for testing all system features

## Future Enhancements

Potential improvements to the dataset:
- Add ethnicity field
- Include facial feature vectors
- Add fingerprint data
- Include case history
- Add witness statements
- Include mugshot images
- Add biometric data (height, weight, build)
- Include known associates
- Add vehicle information
- Include known addresses

## License

This dataset is provided for educational purposes as part of the AI Criminal Sketch Matching System project.
