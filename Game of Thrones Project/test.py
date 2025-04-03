import pickle
import pandas as pd
import os
import sys

def fix_pickle_file():
    # Path to your current pickle file
    pickle_file = 'data.pkl'
    
    try:
        # Try a different approach to load the pickle
        with open(pickle_file, 'rb') as f:
            # Skip the protocol and other header information
            # This is a risky approach but sometimes works for version mismatches
            try:
                data = pd.read_pickle(pickle_file)
                print("Successfully loaded data using pd.read_pickle!")
                
                # Save in a more version-compatible format
                data.to_csv('data.csv', index=False)
                print("Data saved to data.csv")
                
                # If you still need a pickle file, save it with current pandas version
                data.to_pickle('data_new.pkl')
                print("Data resaved to data_new.pkl with current pandas version")
                
                return data
            except Exception as e:
                print(f"pd.read_pickle failed: {e}")
                
        print("Direct loading approaches failed, trying reconstruction...")
        
    except Exception as e:
        print(f"Error during file operations: {e}")
    
    print("\nRecommendations:")
    print("1. Try installing the pandas version used to create the pickle file")
    print("2. Ask the creator of the data.pkl file to share the data in CSV format")
    print("3. If you have access to the original data, recreate the DataFrame")
    
    return None

# Run the function
if __name__ == "__main__":
    print(f"Python version: {sys.version}")
    print(f"Pandas version: {pd.__version__}")
    result = fix_pickle_file()
    
    if result is not None:
        print("\nData preview:")
        print(result.head())
        
        # You can then modify your app.py to load from CSV instead
        print("\nTo modify your app.py, change the loading code to:")
        print("df = pd.read_csv('data.csv')")
        print("df = df.head(25)")