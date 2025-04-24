
import matplotlib.pyplot as plt
from pathlib import Path

def generate_graphs():
    algorithms = []
    avg_waiting_times = []
    avg_turnaround_times = []

    # Read metrics from the file

    base_path = Path(__file__).parent
    metrics_file = base_path / "metrics.txt"
    output_image = base_path / "scheduling_comparison.png"

    # Read metrics from the file

    with open(metrics_file, "r") as f:
        for line in f:
            algorithm, avg_waiting_time, avg_turnaround_time = line.strip().split(',')
            algorithms.append(algorithm)
            avg_waiting_times.append(float(avg_waiting_time))
            avg_turnaround_times.append(float(avg_turnaround_time))

    # Generate graphs

    plt.figure(figsize=(14, 6))

    # Average Waiting Time Comparison
    plt.subplot(1, 2, 1)
    plt.bar(algorithms, avg_waiting_times, color=['#2E7D32', '#00ACC1', '#000000', '#CDDC39'])
    plt.title('Avg Waiting Time Comparison', fontsize=14, fontweight='bold')
    plt.ylabel('Time Units', fontsize=12)
    plt.xticks(rotation=15)

    # Average Turnaround Time Comparison
    plt.subplot(1, 2, 2)
    plt.bar(algorithms, avg_turnaround_times, color=['#2E7D32', '#00ACC1', '#000000', '#CDDC39'])
    plt.title('Avg Turnaround Time Comparison', fontsize=14, fontweight='bold')
    plt.ylabel('Time Units', fontsize=12)
    plt.xticks(rotation=15)

  # Save the graph as an image
    plt.tight_layout()
    plt.savefig(output_image)
    plt.show()

if __name__ == "__main__":
    generate_graphs()