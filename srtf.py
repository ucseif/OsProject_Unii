import main  # استيراد العمليات من الملف الرئيسي

def srtf(processes):
    # ترتيب العمليات حسب وقت الوصول
    processes.sort(key=lambda x: x['Arrival Time'])
    queue = []  # صف العمليات الجاهزة
    current_time = 0  # الوقت الحالي
    results = []  # تخزين النتائج
    remaining_times = {p['Process ID']: p['Burst Time'] for p in processes}  # الأوقات المتبقية لكل عملية
    completed = set()  # العمليات التي تم إكمالها
    start_times = {}  # لتخزين وقت بدء التنفيذ لكل عملية

    while len(completed) < len(processes):
        # إضافة العمليات التي وصلت إلى الوقت الحالي إلى الصف
        for p in processes:
            if p['Arrival Time'] <= current_time and p['Process ID'] not in completed and p not in queue:
                queue.append(p)

        # إذا كان الصف فارغًا ولم تُضف أي عمليات جديدة، تحديث الوقت الحالي إلى وقت أقرب عملية
        if not queue:
            next_arrival = min([p['Arrival Time'] for p in processes if p['Process ID'] not in completed])
            current_time = max(current_time, next_arrival)
            continue

        # ترتيب الصف حسب الأوقات المتبقية (Shortest Remaining Time First)
        queue.sort(key=lambda x: remaining_times[x['Process ID']])
        if queue:
            p = queue[0]  # اختيار العملية الأولى في الصف

            # تسجيل وقت بدء التنفيذ إذا لم يكن مسجلًا بالفعل
            if p['Process ID'] not in start_times:
                start_times[p['Process ID']] = current_time

            # تحديث الوقت المتبقي للعملية
            remaining_times[p['Process ID']] -= 1
            current_time += 1

            # إذا انتهت العملية
            if remaining_times[p['Process ID']] == 0:
                completed.add(p['Process ID'])
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
                    'priority': p.get('Priority', None)  # الأولوية (إن وجدت)
                })
                queue.pop(0)  # إزالة العملية من الصف بعد اكتمالها

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
        "Process ID | Arrival Time | Burst Time | Start Time | Completion Time | Turnaround Time | Waiting Time | Priority"
    )
    print("-" * 120)
    for result in results:
        print(
            f"{result['id']:8} | {result['arrival_time']:12.2f} | {result['burst_time']:9.2f} | {result['start_time']:10.2f} | {result['completion_time']:15.2f} | {result['turnaround_time']:15.2f} | {result['waiting_time']:12.2f} | {result['priority']}"
        )
    print("\nAverage Turnaround Time: {:.2f}".format(metrics['avg_turnaround_time']))
    print("Average Waiting Time: {:.2f}".format(metrics['avg_waiting_time']))


if __name__ == "__main__":
    # استدعاء العمليات من الملف الرئيسي
    results = srtf(main.global_processes)
    metrics = calculate_metrics(results)
    display_results("SRTF", results, metrics)