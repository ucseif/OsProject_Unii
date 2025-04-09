import main  # استيراد العمليات من الملف الرئيسي

def round_robin(processes, time_quantum=4):
    queue = processes[:]
    current_time = 0
    results = []
    remaining_times = {p['Process ID']: p['Burst Time'] for p in processes}
    start_times = {}  # لتخزين وقت بدء التنفيذ لكل عملية
    quantum_used = {}  # لتخزين قيمة Quantum المستخدمة لكل عملية

    while queue:
        p = queue.pop(0)
        if current_time < p['Arrival Time']:
            current_time = p['Arrival Time']

        # تسجيل وقت بدء التنفيذ إذا لم يكن مسجلًا بالفعل
        if p['Process ID'] not in start_times:
            start_times[p['Process ID']] = current_time

        # تحديد الوقت الذي سيتم تنفيذه (أقل قيمة بين Quantum والوقت المتبقي)
        execution_time = min(time_quantum, remaining_times[p['Process ID']])
        remaining_times[p['Process ID']] -= execution_time
        current_time += execution_time

        # تخزين قيمة Quantum المستخدمة لهذه العملية
        if p['Process ID'] not in quantum_used:
            quantum_used[p['Process ID']] = execution_time
        else:
            quantum_used[p['Process ID']] += execution_time

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
                'priority': p.get('Priority', None),  # الأولوية (إن وجدت)
                'quantum_used': quantum_used[p['Process ID']]  # قيمة Quantum المستخدمة
            })
        else:
            queue.append(p)

    return results


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


def display_results(algorithm_name, results, metrics):
    print(f"\nAlgorithm: {algorithm_name}")
    print(
        "Process ID | Quantum | Arrival Time | Burst Time | Start Time | Completion Time | Turnaround Time | Waiting Time | Priority"
    )
    print("-" * 150)
    for result in results:
        print(
            f"{result['id']:8}   | {result['quantum_used']:5}   | {result['arrival_time']:10.2f}   | {result['burst_time']:8.2f}   | {result['start_time']:8.2f}   | {result['completion_time']:13.2f}   | {result['turnaround_time']:13.2f}   | {result['waiting_time']:10.2f}   | {result['priority']:7}"
        )
    print("\nAverage Turnaround Time: {:.2f}".format(metrics['avg_turnaround_time']))
    print("Average Waiting Time: {:.2f}".format(metrics['avg_waiting_time']))


if __name__ == "__main__":
    results = round_robin(main.global_processes)
    metrics = calculate_metrics(results)
    display_results("Round Robin", results, metrics)