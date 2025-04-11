import matplotlib.pyplot as plt

def generate_graphs():
    algorithms = []
    avg_waiting_times = []
    avg_turnaround_times = []

    # Read metrics from the file
    with open("d:\\filesOfPyCharm\\OsProject_Unii\\metrics.txt", "r") as f:
        for line in f:
            algorithm, avg_waiting_time, avg_turnaround_time = line.strip().split(',')
            algorithms.append(algorithm)
            avg_waiting_times.append(float(avg_waiting_time))
            avg_turnaround_times.append(float(avg_turnaround_time))

    # Generate graphs
    plt.figure(figsize=(14, 6))  # Slightly larger figure size

    # Average Waiting Time Comparison
    plt.subplot(1, 2, 1)
    plt.bar(algorithms, avg_waiting_times, color=['#2E7D32', '#00ACC1', '#000000', '#CDDC39'])  # New color scheme FF5733 , 33FF57 , 3357FF , FF33A1
    plt.title('Avg Waiting Time Comparison', fontsize=14, fontweight='bold')  # Bold title
    plt.ylabel('Time Units', fontsize=12)
    plt.xticks(rotation=15)  # Rotate x-axis labels

    # Average Turnaround Time Comparison
    plt.subplot(1, 2, 2)
    plt.bar(algorithms, avg_turnaround_times, color=['#2E7D32', '#00ACC1', '#000000', '#CDDC39'])  # New color scheme
    plt.title('Avg Turnaround Time Comparison', fontsize=14, fontweight='bold')  # Bold title
    plt.ylabel('Time Units', fontsize=12)
    plt.xticks(rotation=15)  # Rotate x-axis labels

    # Save the graph as an image
    plt.tight_layout()
    plt.savefig("d:\\filesOfPyCharm\\OsProject_Unii\\scheduling_comparison.png")
    plt.show()

def generate_graphs():
    algorithms = []
    avg_waiting_times = []
    avg_turnaround_times = []

    # Read metrics from the file
    with open("d:\\filesOfPyCharm\\OsProject_Unii\\metrics.txt", "r") as f:
        for line in f:
            algorithm, avg_waiting_time, avg_turnaround_time = line.strip().split(',')
            algorithms.append(algorithm)
            avg_waiting_times.append(float(avg_waiting_time))
            avg_turnaround_times.append(float(avg_turnaround_time))

    # Generate graphs
    plt.figure(figsize=(14, 6))  # Slightly larger figure size

    # Average Waiting Time Comparison
    plt.subplot(1, 2, 1)
    plt.bar(algorithms, avg_waiting_times, color=['#2E7D32', '#00ACC1', '#000000', '#CDDC39'])  # New color scheme
    plt.title('Avg Waiting Time Comparison', fontsize=14, fontweight='bold',)  # Bold title
    plt.ylabel('Time Units', fontsize=12)
    plt.xticks(rotation=15)  # Rotate x-axis labels

    # Average Turnaround Time Comparison
    plt.subplot(1, 2, 2)
    plt.bar(algorithms, avg_turnaround_times, color=['#2E7D32', '#00ACC1', '#000000', '#CDDC39'])  # New color scheme
    plt.title('Avg Turnaround Time Comparison', fontsize=14, fontweight='bold')  # Bold title
    plt.ylabel('Time Units', fontsize=12)
    plt.xticks(rotation=15)  # Rotate x-axis labels

    # Save the graph as an image
    plt.tight_layout()
    plt.savefig("d:\\filesOfPyCharm\\OsProject_Unii\\scheduling_comparison.png")
    plt.show()

if __name__ == "__main__":
    generate_graphs()