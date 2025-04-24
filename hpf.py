import main
from pathlib import Path


# Sort processes by priority (highest first), then by arrival time
def hpf(processes):
    processes.sort(key=lambda x: (-x['Priority'], x['Arrival Time']))
    current_time = 0
    results = []

    for p in processes:
        if current_time < p['Arrival Time']:
            current_time = p['Arrival Time']
        start_time = current_time
        completion_time = current_time + p['Burst Time']
        turnaround_time = completion_time - p['Arrival Time']
        waiting_time = turnaround_time - p['Burst Time']
        results.append({
            'id': p['Process ID'],
            'arrival_time': p['Arrival Time'],
            'burst_time': p['Burst Time'],
            'start_time': start_time,
            'completion_time': completion_time,
            'turnaround_time': turnaround_time,
            'waiting_time': waiting_time,
            'priority': p['Priority']
        })
        current_time = completion_time

    return results

# Calculate average turnaround and waiting time

def calculate_metrics(results):
    total_turnaround_time = sum(r['turnaround_time'] for r in results)
    total_waiting_time = sum(r['waiting_time'] for r in results)
    num_processes = len(results)

    avg_turnaround_time = total_turnaround_time / num_processes
    avg_waiting_time = total_waiting_time / num_processes

    return {
        'avg_turnaround_time': avg_turnaround_time,
        'avg_waiting_time': avg_waiting_time
    }

# Display the results in a clean formatted table

def display_results(algorithm_name, results, metrics):
    print(f"\nAlgorithm: {algorithm_name}")
    print("-" * 120)
    print(
        "Process ID | Arrival Time | Burst Time | Start Time | Completion Time | Turnaround Time | Waiting Time | Priority"
    )
    print("-" * 120)
    for result in results:
        print(
            f"{result['id']:8}   | {result['arrival_time']:10.2f}   | {result['burst_time']:8.2f}   | {result['start_time']:8.2f}   | {result['completion_time']:13.2f}   | {result['turnaround_time']:13.2f}   | {result['waiting_time']:10.2f}   | {result['priority']:7}"
        )
    print("-" * 120)
    print("\nAverage Turnaround Time: {:.2f}".format(metrics['avg_turnaround_time']))
    print("Average Waiting Time: {:.2f}".format(metrics['avg_waiting_time']))

# Main execution: run HPF algorithm and save the metrics to a file

if __name__ == "__main__":
    results = hpf(main.global_processes)
    metrics = calculate_metrics(results)
    display_results("HPF", results, metrics)

    metrics_file = Path(__file__).parent / "metrics.txt"

    # Append metrics to the file
    with open(metrics_file, "a") as f:
        f.write(f"HPF,{metrics['avg_waiting_time']},{metrics['avg_turnaround_time']}\n")