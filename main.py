import pandas as pd

# Load the process data generated from Process Generator
try:
    # Read the output.txt file, skip headers and ignore comment lines
    df = pd.read_csv('output.txt', sep='|', skiprows=4, comment='-', engine='python')

    # Clean column names from extra spaces
    df.columns = df.columns.str.strip()

    # Convert columns to appropriate data types
    df['Process ID'] = df['Process ID'].astype(int)
    df['Arrival Time'] = df['Arrival Time'].astype(float)
    df['Burst Time'] = df['Burst Time'].astype(float)
    df['Priority'] = df['Priority'].astype(int)

    # Convert the DataFrame to a list of dictionaries
    processes = df.to_dict('records')

    # Store the process list in a global variable
    global_processes = processes

except Exception as e:
    # Print error message if reading fails
    print("Error while reading the file:", e)