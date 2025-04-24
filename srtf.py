import main  # استيراد العمليات من الملف الرئيسي


def srtf_algorithm(processes):
    """
    Shortest Remaining Time First (SRTF) - Preemptive Scheduling
    الجدولة باستخدام أقصر وقت تنفيذ متبقٍ، مع إمكانية الإزاحة (Preemptive)
    """
    n = len(processes)
    if n == 0:
        print("لا توجد عمليات متاحة.")
        return []

    # تجهيز العمليات مع الحقول المطلوبة
    for p in processes:
        p['remaining_time'] = p['Burst Time']
        p['is_completed'] = False

    current_time = 0
    completed = 0
    results = []
    start_times = {}

    while completed < n:
        # العمليات المتاحة حاليًا
        available = [p for p in processes if p['Arrival Time'] <= current_time and not p['is_completed']]

        # تصفية العمليات التي ما زال لديها وقت متبقي فقط
        available = [p for p in available if p['remaining_time'] > 0]

        if not available:
            current_time += 1  # المعالج في حالة خمول، نزيد الوقت
            continue

        # اختيار العملية ذات أقل وقت متبقي
        current_process = min(available, key=lambda p: p['remaining_time'])

        pid = current_process['Process ID']

        # تسجيل وقت البدء لأول مرة فقط
        if pid not in start_times:
            start_times[pid] = current_time

        # تنفيذ وحدة زمنية واحدة
        current_process['remaining_time'] -= 1
        current_time += 1

        # عند الانتهاء من العملية
        if current_process['remaining_time'] == 0:
            completed += 1
            completion_time = current_time
            turnaround_time = completion_time - current_process['Arrival Time']
            waiting_time = turnaround_time - current_process['Burst Time']

            # إضافة النتائج
            results.append({
                'id': pid,
                'arrival_time': current_process['Arrival Time'],
                'burst_time': current_process['Burst Time'],
                'start_time': start_times[pid],
                'completion_time': completion_time,
                'turnaround_time': turnaround_time,
                'waiting_time': waiting_time,
                'priority': current_process.get('Priority')
            })

            current_process['is_completed'] = True

    # ترتيب النتائج حسب وقت الإكمال
    return sorted(results, key=lambda p: p['completion_time'])


def calculate_average_metrics(results):
    """حساب المتوسطات لوقت الانتظار ووقت الدوران"""
    n = len(results)
    if n == 0:
        return {'avg_turnaround_time': 0, 'avg_waiting_time': 0}

    total_tat = sum(p['turnaround_time'] for p in results)
    total_wt = sum(p['waiting_time'] for p in results)

    return {
        'avg_turnaround_time': total_tat / n,
        'avg_waiting_time': total_wt / n
    }


def display_results(results, metrics):
    """عرض النتائج بشكل منسق"""
    print("\nAlgorithm: SRTF (Shortest Remaining Time First)")
    print("-" * 120)
    print(
        "Process ID | Arrival Time | Burst Time | Start Time | Completion Time | Turnaround Time | Waiting Time | Priority")
    print("-" * 120)

    for p in results:
        print(f"{p['id']:10} | {p['arrival_time']:12.2f} | {p['burst_time']:10.2f} | "
              f"{p['start_time']:10.2f} | {p['completion_time']:15.2f} | "
              f"{p['turnaround_time']:15.2f} | {p['waiting_time']:12.2f} | {str(p['priority']):8}")

    print("-" * 120)
    print(f"\nAverage Turnaround Time: {metrics['avg_turnaround_time']:.2f}")
    print(f"Average Waiting Time: {metrics['avg_waiting_time']:.2f}")


if __name__ == "__main__":
    processes = main.global_processes

    if processes:
        results = srtf_algorithm(processes)
        metrics = calculate_average_metrics(results)
        display_results(results, metrics)

        # حفظ النتائج في ملف لرسومات الجرافيك
        with open("d:\\filesOfPyCharm\\OsProject_Unii\\metrics.txt", "a") as f:
            f.write(f"SRTF,{metrics['avg_waiting_time']},{metrics['avg_turnaround_time']}\n")
    else:
        print("⚠️ لا توجد عمليات صالحة للجدولة.")