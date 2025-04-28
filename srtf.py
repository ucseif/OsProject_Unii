import pandas as pd
import heapq

# Function to implement SRTF Scheduling Algorithm
def srtf(processes):
    processes.sort(key=lambda x: x['Arrival Time'])  # Sort by Arrival Time initially

    n = len(processes)
    time = 0
    completed = 0

    remaining_bt = {p['Process ID']: p['Burst Time'] for p in processes}
    arrival_dict = {p['Process ID']: p['Arrival Time'] for p in processes}
    burst_dict = {p['Process ID']: p['Burst Time'] for p in processes}

    start_time = {}
    completion_time = {}
    turnaround_time = {}
    waiting_time = {}
    ready_queue = []
    visited = set()

    results = []

    while completed < n:
        # Add processes to ready queue based on arrival time
        for p in processes:
            pid = p['Process ID']
            if p['Arrival Time'] <= time and pid not in visited and remaining_bt[pid] > 0:
                heapq.heappush(ready_queue, (remaining_bt[pid], p['Arrival Time'], pid, p))
                visited.add(pid)

        if ready_queue:
            rt, at, pid, p = heapq.heappop(ready_queue)

            if pid not in start_time:
                start_time[pid] = time

            remaining_bt[pid] -= 1
            time += 1

            if remaining_bt[pid] > 0:
                heapq.heappush(ready_queue, (remaining_bt[pid], at, pid, p))
            else:
                completed += 1
                completion_time[pid] = time
                tat = time - arrival_dict[pid]
                wt = tat - burst_dict[pid]

                turnaround_time[pid] = tat
                waiting_time[pid] = wt

                results.append({
                    'id': pid,
                    'arrival_time': arrival_dict[pid],
                    'burst_time': burst_dict[pid],
                    'start_time': start_time[pid],
                    'completion_time': completion_time[pid],
                    'turnaround_time': tat,
                    'waiting_time': wt,
                    'priority': p.get('Priority', None)
                })
        else:
            time += 1

    return results

# Function to calculate metrics
def calculate_metrics(results):
    total_tat = sum(r['turnaround_time'] for r in results)
    total_wt = sum(r['waiting_time'] for r in results)
    n = len(results)
    return {
        'avg_turnaround_time': total_tat / n,
        'avg_waiting_time': total_wt / n
    }

# Function to display the results
def display_results(algorithm_name, results, metrics):
    print(f"\nAlgorithm: {algorithm_name}")
    print("-" * 120)
    print("Process ID | Arrival Time | Burst Time | Start Time | Completion Time | Turnaround Time | Waiting Time | Priority")
    print("-" * 120)
    for result in results:
        print(
            f"{result['id']:8}   | {result['arrival_time']:10.2f}   | {result['burst_time']:8.2f}   | {result['start_time']:8.2f}   | {result['completion_time']:13.2f}   | {result['turnaround_time']:13.2f}   | {result['waiting_time']:10.2f}   | {result['priority']:7}")
    print("-" * 120)
    print("\nAverage Turnaround Time: {:.2f}".format(metrics['avg_turnaround_time']))
    print("Average Waiting Time: {:.2f}".format(metrics['avg_waiting_time']))

# Main block to load data and run SRTF
if __name__ == "__main__":
    try:
        df = pd.read_csv('output.txt', sep='|', skiprows=4, comment='-', engine='python')
        df.columns = df.columns.str.strip()
        df['Process ID'] = df['Process ID'].astype(int)
        df['Arrival Time'] = df['Arrival Time'].astype(float)
        df['Burst Time'] = df['Burst Time'].astype(float)
        df['Priority'] = df['Priority'].astype(int)

        processes = df.to_dict('records')

        results = srtf(processes)
        metrics = calculate_metrics(results)
        display_results("SRTF", results, metrics)

        # Save the metrics to file for graphing
        with open("metrics.txt", "a") as f:
            f.write(f"SRTF,{metrics['avg_waiting_time']},{metrics['avg_turnaround_time']}\n")

    except Exception as e:
        print("❌ Error:", e)