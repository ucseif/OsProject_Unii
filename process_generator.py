import pandas as pd
import numpy as np

def generate_processes(input_file, output_file):
    try:
        # Read input file containing distribution parameters
        with open(input_file, 'r') as f:
            lines = f.readlines()

        # Extract number of processes
        n = int(lines[0].strip())

        # Extract mean and std deviation for arrival time
        arrival_mean, arrival_std = map(float, lines[1].strip().split())

        # Extract mean and std deviation for burst time
        burst_mean, burst_std = map(float, lines[2].strip().split())

        # Extract lambda value for Poisson priority distribution
        lambda_priority = float(lines[3].strip())

        # Generate process data based on distributions
        arrival_times = np.random.normal(arrival_mean, arrival_std, n)
        burst_times = np.random.normal(burst_mean, burst_std, n)
        priorities = np.random.poisson(lambda_priority, n)

        # Create DataFrame to hold the process info
        data = {
            'Process ID': range(1, n + 1),
            'Arrival Time': arrival_times,
            'Burst Time': burst_times,
            'Priority': priorities
        }
        df = pd.DataFrame(data)

        separator = "-" * 50  # Line separator for formatting

        # Write process data to output file
        with open(output_file, 'w') as f:
            f.write("# Output File for Process Generator Module\n")
            f.write(f"# Number of Processes: {n}\n\n")
            f.write(separator + "\n")
            f.write("Process ID | Arrival Time | Burst Time | Priority\n")
            f.write(separator + "\n")

            for _, row in df.iterrows():
                f.write(
                    f"{int(row['Process ID']):7}    | {row['Arrival Time']:9.2f}    | {row['Burst Time']:7.2f}    | {int(row['Priority']):8}\n"
                )

            f.write(separator + "\n")

        print("Output file has been created successfully!\n")
        display_output(output_file)

    except Exception as e:
        print("Error:", e)

# Display the content of the generated output file
def display_output(output_file):
    try:
        with open(output_file, 'r') as f:
            print(f.read())
    except Exception as e:
        print("Error while displaying output:", e)

# Run process generation using input and output files
generate_processes("input.txt", "output.txt")