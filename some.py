import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def read_excel_file(file_path, sheet_name=0):
    """Read Excel file and return a pandas DataFrame"""
    try:
        # Skip initial rows if necessary and set header explicitly
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=4, dtype=str, engine="xlrd")
        print(f"\n✅ Columns found: {df.columns.tolist()}\n")
        return df
    except Exception as e:
        raise Exception(f"❌ Error reading Excel file: {e}")

def clean_data(df):
    """Clean and preprocess the data"""
    if df.empty:
        raise ValueError("❌ DataFrame is empty after loading.")
    
    # Remove empty rows
    df = df.dropna(how='all')
    
    # Set proper column names based on your data structure
    df.columns = [
        'Region', 'Agriculture, forestry & fishing', 'Production', 'Construction', 'Motor trades',
        'Wholesale', 'Retail', 'Transport & Storage', 'Accommodation & food services',
        'Information & communication', 'Finance & insurance', 'Property',
        'Professional, scientific & technical', 'Business administration & support services',
        'Public administration & defence', 'Education', 'Health',
        'Arts, entertainment, recreation & other services', 'Total'
    ]
    
    # Handle NaN or float values in 'Region' column
    df['Region'] = df['Region'].fillna('Unknown')  # Replace NaN with a placeholder
    df['Region Code'] = df['Region'].apply(lambda x: str(x).split(' : ')[0] if ' : ' in str(x) else str(x))
    df['Region Name'] = df['Region'].apply(lambda x: str(x).split(' : ')[1] if ' : ' in str(x) else str(x))
    df = df.drop('Region', axis=1)
    
    # Convert numeric columns to integers
    numeric_cols = df.columns[:-2]  # All except Region Code and Name
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    
    # Move Region Code and Name to the front
    cols = ['Region Code', 'Region Name'] + [col for col in df.columns if col not in ['Region Code', 'Region Name']]
    df = df[cols]
    
    print(f"🔍 Detected {len(df.columns)} columns in dataset.")
    return df

def analyze_data(df):
    """Perform analysis on the data"""
    df = df.set_index('Region Code')
    
    print("\n📊 === BASIC STATISTICS ===")
    print(f"📍 Total regions: {len(df)}")
    print(f"📈 Total enterprises across UK: {df['Total'].sum():,}")
    
    # Regional analysis
    print("\n=== TOP 10 REGIONS BY TOTAL ENTERPRISES ===")
    top_regions = df[['Region Name', 'Total']].sort_values(by='Total', ascending=False).head(10)
    print(top_regions.to_string(index=False))
    
    # Industry analysis
    industry_cols = [col for col in df.columns if col not in ['Region Name', 'Total']]
    industry_totals = df[industry_cols].sum().sort_values(ascending=False)
    
    print("\n=== TOP 10 INDUSTRIES BY ENTERPRISE COUNT ===")
    print(industry_totals.head(10).to_string())
    
    # Visualization
    plt.figure(figsize=(12, 6))
    industry_totals.head(10).plot(kind='bar')
    plt.title('Top 10 Industries by Enterprise Count in the UK')
    plt.xlabel('Industry')
    plt.ylabel('Number of Enterprises')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
    
    return df

# Example usage
file_path = "C:\\TUL\\week4-python-p1\\data\\sheet1.xls"
df = read_excel_file(file_path)
df_clean = clean_data(df)
analyzed_df = analyze_data(df_clean)