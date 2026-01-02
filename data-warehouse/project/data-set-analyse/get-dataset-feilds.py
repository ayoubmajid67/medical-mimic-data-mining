import os
import csv
from itertools import islice

# Configuration
# Path to the directory containing MIMIC-III CSV files
# Using absolute path as per the user's workspace structure
MIMIC_DIR = '..\dataset'

# Output files in the same directory as this script
FIELDS_OUTPUT_FILE = os.path.join(os.path.dirname(__file__), 'dataset_fields.txt')
SAMPLES_OUTPUT_FILE = os.path.join(os.path.dirname(__file__), 'dataset_samples.txt')

def get_csv_analysis(directory, sample_size=5):
    """
    Reads all CSV files in the directory and returns a dictionary of filename -> {'headers': [], 'samples': []}.
    """
    dataset_analysis = {}
    
    if not os.path.exists(directory):
        print(f"Error: Directory not found: {directory}")
        return dataset_analysis

    files = [f for f in os.listdir(directory) if f.lower().endswith('.csv')]
    files.sort() # Process files in alphabetical order

    for filename in files:
        filepath = os.path.join(directory, filename)
        try:
            with open(filepath, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                try:
                    headers = next(reader)
                    # Read sample_size rows
                    samples = list(islice(reader, sample_size))
                    dataset_analysis[filename] = {
                        'headers': headers,
                        'samples': samples
                    }
                except StopIteration:
                    print(f"Warning: {filename} is empty.")
                    dataset_analysis[filename] = {'headers': [], 'samples': []}
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            
    return dataset_analysis

def save_fields_to_file(analysis_data, output_path):
    """
    Saves the fields information to a text file.
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            for filename, data in analysis_data.items():
                headers = data['headers']
                f.write(f"File: {filename}\n")
                f.write("-" * (len(filename) + 6) + "\n")
                
                # Write fields in a clear, ordered list
                for idx, header in enumerate(headers, 1):
                    f.write(f"{idx}. {header}\n")
                
                f.write("\n" + "="*40 + "\n\n")
        
        print(f"Successfully saved field info to: {output_path}")
    except Exception as e:
        print(f"Error writing to fields output file: {e}")

def save_samples_to_file(analysis_data, output_path):
    """
    Saves the sample rows information to a text file.
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            for filename, data in analysis_data.items():
                headers = data['headers']
                samples = data['samples']
                
                f.write(f"File: {filename}\n")
                f.write("-" * (len(filename) + 6) + "\n")
                
                if not samples:
                    f.write("(No data rows found)\n")
                else:
                    # Write headers first
                    f.write(f"Headers: {', '.join(headers)}\n\n")
                    f.write("Samples (First 5 rows):\n")
                    for i, row in enumerate(samples, 1):
                        f.write(f"Row {i}: {row}\n")
                
                f.write("\n" + "="*40 + "\n\n")
        
        print(f"Successfully saved samples info to: {output_path}")
    except Exception as e:
        print(f"Error writing to samples output file: {e}")

def main():
    print("Starting analysis of MIMIC-III dataset fields and samples...")
    print(f"Source Directory: {MIMIC_DIR}")
    
    analysis_data = get_csv_analysis(MIMIC_DIR)
    
    if analysis_data:
        save_fields_to_file(analysis_data, FIELDS_OUTPUT_FILE)
        save_samples_to_file(analysis_data, SAMPLES_OUTPUT_FILE)
        print("Done.")
    else:
        print("No fields found or errors encountered.")

if __name__ == "__main__":
    main()
