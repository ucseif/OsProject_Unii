import main
from pathlib import Path

def round_robin(processes, time_quantum=4):
    queue = processes[:]
    current_time = 0
    results = []
    remaining_times = {p['Process ID']: p['Burst Time'] for p in processes}
    start_times = {}

    process_sequence = []
    while queue:
        p = queue.pop(0)

        # Ensure the current time is after the process's arrival time
        if current_time < p['Arrival Time']:
            current_time = p['Arrival Time']

        # Record the start time of the process if it's the first time it's being executed
        if p['Process ID'] not in start_times:
            start_times[p['Process ID']] = current_time

        # Execute the process for a maximum of 'time_quantum' units of time
        execution_time = min(time_quantum, remaining_times[p['Process ID']])
        remaining_times[p['Process ID']] -= execution_time
        current_time += execution_time

        # Track the sequence of process execution
        process_sequence.append(p['Process ID'])

        # If the process is completed (remaining time is 0), calculate the metrics
        if remaining_times[p['Process ID']] == 0:
            completion_time = current_time
            turnaround_time = completion_time - p['Arrival Time']
            waiting_time = turnaround_time - p['Burst Time']
            results.append({
                'id': p['Process ID'],
                'arrival_time': p['Arrival Time'],
                'burst_time': p['Burst Time'],
                'start_time': start_times[p['Process ID']],
                'completion_time': completion_time,
                'turnaround_time': turnaround_time,
                'waiting_time': waiting_time,
                'priority': p.get('Priority', None)
            })
        else:
            # If the process is not completed, add it back to the queue to continue later
            queue.append(p)

    return results, process_sequence

def calculate_metrics(results):
    # Calculate the total turnaround time and waiting time
    total_turnaround_time = sum(r['turnaround_time'] for r in results)
    total_waiting_time = sum(r['waiting_time'] for r in results)
    num_processes = len(results)

    # Calculate and return the average turnaround time and waiting time
    avg_turnaround_time = total_turnaround_time / num_processes
    avg_waiting_time = total_waiting_time / num_processes

    return {
        'avg_turnaround_time': avg_turnaround_time,
        'avg_waiting_time': avg_waiting_time
    }

def display_results(algorithm_name, results, metrics, process_sequence):
    # Display the results in a neat table format
    print(f"\nAlgorithm: {algorithm_name}")
    print("-" * 127)
    print(
        "Process ID | Arrival Time | Burst Time | Start Time | Completion Time | Turnaround Time | Waiting Time | Priority"
    )
    print("-" * 127)
    for result in results:
        print(
            f"{result['id']:8}   | {result['arrival_time']:10.2f}   | {result['burst_time']:8.2f}   | {result['start_time']:8.2f}   | {result['completion_time']:13.2f}   | {result['turnaround_time']:13.2f}   | {result['waiting_time']:10.2f}   | {result['priority']:7}"
        )
    print("-" * 127)
    print("\nAverage Turnaround Time: {:.2f}".format(metrics['avg_turnaround_time']))
    print("Average Waiting Time: {:.2f}".format(metrics['avg_waiting_time']))

    # Display the process sequence
    print("\nProcess Execution Sequence (Order in which processes entered the queue):")
    print(" -> ".join(map(str, process_sequence)))

if __name__ == "__main__":
    results, process_sequence = round_robin(main.global_processes)
    metrics = calculate_metrics(results)
    display_results("Round Robin", results, metrics, process_sequence)

    # Append the metrics to a text file
    metrics_file = Path(__file__).parent / "metrics.txt"
    with open(metrics_file, "a") as f:
        f.write(f"Round Robin,{metrics['avg_waiting_time']},{metrics['avg_turnaround_time']}\n")
