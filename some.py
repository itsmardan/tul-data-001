# These are like toolkits we borrow to help us work with tables, math, and charts
import pandas as pd  # Helps us read and manage tables (like Excel)
import numpy as np  # Helps with math (not used much here)
import matplotlib.pyplot as plt  # Draws charts, like bar graphs

# Function to read an Excel file and turn it into a table
def read_excel_file(file_path, sheet_name=0):
    """Read Excel file and return a pandas DataFrame"""
    try:
        # Read the Excel file, skip 4 rows, treat everything as text, use 'xlrd' for old .xls files
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=4, dtype=str, engine="xlrd")
        print(f"\n✅ Columns found: {df.columns.tolist()}\n")  # Show the column names we found
        return df  # Give the table back
    except Exception as e:
        raise Exception(f"❌ Error reading Excel file: {e}")  # If something goes wrong, tell us

# Function to clean up the table so it’s neat and easy to use
def clean_data(df):
    """Clean and preprocess the data"""
    if df.empty:  # If the table is empty, stop and say so
        raise ValueError("❌ DataFrame is empty after loading.")
    
    df = df.dropna(how='all')  # Throw out rows that are completely empty
    
    # Give the columns clear names based on what’s in the Excel file
    df.columns = [
        'Region', 'Agriculture, forestry & fishing', 'Production', 'Construction', 'Motor trades',
        'Wholesale', 'Retail', 'Transport & Storage', 'Accommodation & food services',
        'Information & communication', 'Finance & insurance', 'Property',
        'Professional, scientific & technical', 'Business administration & support services',
        'Public administration & defence', 'Education', 'Health',
        'Arts, entertainment, recreation & other services', 'Total'
    ]
    
    # Fix the 'Region' column
    df['Region'] = df['Region'].fillna('Unknown')  # If a region is blank, call it "Unknown"
    # Split "E12000001 : North East" into code (E12000001) and name (North East)
    df['Region Code'] = df['Region'].apply(lambda x: str(x).split(' : ')[0] if ' : ' in str(x) else str(x))
    df['Region Name'] = df['Region'].apply(lambda x: str(x).split(' : ')[1] if ' : ' in str(x) else str(x))
    df = df.drop('Region', axis=1)  # Remove the old 'Region' column since we split it
    
    # Turn number columns into actual numbers (not text), fill blanks with 0
    numeric_cols = df.columns[:-2]  # All columns except 'Region Code' and 'Region Name'
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    
    # Move 'Region Code' and 'Region Name' to the front of the table
    cols = ['Region Code', 'Region Name'] + [col for col in df.columns if col not in ['Region Code', 'Region Name']]
    df = df[cols]
    
    print(f"🔍 Detected {len(df.columns)} columns in dataset.")  # Tell us how many columns we have
    return df  # Give the cleaned table back

# Function to analyze the data and show interesting facts
def analyze_data(df):
    """Perform analysis on the data"""
    df = df.set_index('Region Code')  # Use 'Region Code' as the row labels
    
    # Show some basic facts
    print("\n📊 === BASIC STATISTICS ===")
    print(f"📍 Total regions: {len(df)}")  # How many regions are in the table
    print(f"📈 Total enterprises across UK: {df['Total'].sum():,}")  # Add up all businesses
    
    # Show the top 10 regions with the most businesses
    print("\n=== TOP 10 REGIONS BY TOTAL ENTERPRISES ===")
    top_regions = df[['Region Name', 'Total']].sort_values(by='Total', ascending=False).head(10)
    print(top_regions.to_string(index=False))  # Print without the row numbers
    
    # Find out which industries have the most businesses
    industry_cols = [col for col in df.columns if col not in ['Region Name', 'Total']]
    industry_totals = df[industry_cols].sum().sort_values(ascending=False)
    
    print("\n=== TOP 10 INDUSTRIES BY ENTERPRISE COUNT ===")
    print(industry_totals.head(10).to_string())  # Show the top 10 industries
    
    # Draw a bar chart of the top 10 industries
    plt.figure(figsize=(12, 6))  # Make the chart 12 wide and 6 tall
    industry_totals.head(10).plot(kind='bar')  # Make a bar chart with the top 10
    plt.title('Top 10 Industries by Enterprise Count in the UK')  # Add a title
    plt.xlabel('Industry')  # Label the x-axis (bottom)
    plt.ylabel('Number of Enterprises')  # Label the y-axis (side)
    plt.xticks(rotation=45, ha='right')  # Tilt the industry names so they fit
    plt.tight_layout()  # Make sure everything fits nicely
    plt.show()  # Show the chart
    
    return df  # Give the analyzed table back

# Where to find the Excel file and how to run everything
file_path = "C:\\TUL\\week4-python-p1\\data\\sheet1.xls"  # Path to your Excel file
df = read_excel_file(file_path)  # Read the file
df_clean = clean_data(df)  # Clean the table
analyzed_df = analyze_data(df_clean)  # Analyze and show results