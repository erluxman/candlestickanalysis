import json
import os
import csv

def read_stock_data(file_path):
    """Read stock data from a JSON file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    return data

def calculate_percentage_changes(stock_data):
    """Calculate percentage changes from opening price to high and low."""
    result = []
    
    for entry in stock_data:
        opening = entry.get('open')
        high = entry.get('high')
        low = entry.get('low')
        
        if opening and high and low:
            try:
                opening = float(opening)
                high = float(high)
                low = float(low)
                
                pct_change_high = ((high - opening) / opening) * 100
                pct_change_low = ((low - opening) / opening) * 100
                
                result.append({
                    **entry,
                    'pct_change_high': pct_change_high,
                    'pct_change_low': pct_change_low
                })
            except (ValueError, TypeError):
                continue
    
    return result

def count_threshold_instances(stock_data_with_changes, high_threshold, low_threshold):
    """Count instances where percentage changes exceed thresholds."""
    high_count = sum(1 for entry in stock_data_with_changes if entry.get('pct_change_high', 0) >= high_threshold)
    low_count = sum(1 for entry in stock_data_with_changes if entry.get('pct_change_low', 0) <= -abs(low_threshold))
    
    return high_count, low_count

def analyze_stock_movement(file_path, high_threshold, low_threshold):
    """Analyze stock movement from a JSON file."""
    stock_data = read_stock_data(file_path)
    stock_data_with_changes = calculate_percentage_changes(stock_data)
    high_count, low_count = count_threshold_instances(stock_data_with_changes, high_threshold, low_threshold)
    
    return stock_data_with_changes, high_count, low_count

def test_sideways_profit():
    # Read all files from the specified directory
    data_dir = '/Users/risky/project/personal/mba/thesis_v2/data/sideways_test'
    # Get all files from data directory
    files = os.listdir(data_dir)

    # Filter for CSV files with the specific prefix
    csv_files = [f for f in files if f.startswith('nepsealpha_export_price_') and f.endswith('.csv')]

    for csv_file in csv_files:
        try:
            # Create the full file path
            csv_path = os.path.join(data_dir, csv_file)
            
            # Extract new file name - remove prefix, split by '_', take first part
            file_name_without_prefix = csv_file.replace('nepsealpha_export_price_', '')
            new_name = file_name_without_prefix.split('_')[0] + '.json'
            json_path = os.path.join(data_dir, new_name)
            
            # Read CSV and convert to JSON
            data = []
            with open(csv_path, 'r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    data.append(dict(row))
            
            # Write JSON file
            print(f"writing json file for {new_name}")
            with open(json_path, 'w') as file:
                json.dump(data, file, indent=4)
            
            print(f"Converted {csv_file} to {new_name}")
        except Exception as e:
            print(f"Error processing {csv_file}: {str(e)}")
#    analyze_stock_movement('data/stock_data.json', 1, 1)


