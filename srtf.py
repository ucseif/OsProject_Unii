import main  # استيراد العمليات من الملف الرئيسي

def srtf_algorithm(processes):
    """تنفيذ خوارزمية SRTF"""
    if not processes:
        print("لا توجد عمليات للجدولة!")
        return []
    
    print(f"بدء جدولة {len(processes)} عملية")
    
    # نسخة من العمليات للعمل عليها
    processes = [p.copy() for p in processes]
    
    # إضافة حقل للوقت المتبقي
    for p in processes:
        p['remaining_time'] = p['Burst Time']
    
    current_time = 0
    completed = []
    
    # استمر حتى اكتمال جميع العمليات
    while len(completed) < len(processes):
        # العمليات المتاحة في الوقت الحالي
        available = [p for p in processes if p['Arrival Time'] <= current_time and p['remaining_time'] > 0]
        
        if not available:
            # إذا لم تكن هناك عمليات متاحة، انتقل إلى وقت وصول العملية التالية
            next_arrivals = [p['Arrival Time'] for p in processes if p['remaining_time'] > 0]
            if next_arrivals:
                current_time = min(next_arrivals)
                print(f"لا توجد عمليات متاحة، الانتقال إلى الوقت {current_time}")
            else:
                print("جميع العمليات اكتملت أو لا توجد عمليات متبقية")
                break
            continue
        
        # اختيار العملية ذات أقل وقت متبقي
        current_process = min(available, key=lambda p: p['remaining_time'])
        print(f"تنفيذ العملية {current_process['Process ID']} في الوقت {current_time}, الوقت المتبقي: {current_process['remaining_time']}")
        
        # تحديد وقت البدء إذا كانت هذه أول مرة تنفذ فيها العملية
        if 'start_time' not in current_process:
            current_process['start_time'] = current_time
        
        # تنفيذ العملية لوحدة زمنية واحدة
        current_time += 1
        current_process['remaining_time'] -= 1
        
        # التحقق من اكتمال العملية
        if current_process['remaining_time'] == 0:
            completion_time = current_time
            turnaround_time = completion_time - current_process['Arrival Time']
            waiting_time = turnaround_time - current_process['Burst Time']
            
            completed.append({
                'id': current_process['Process ID'],
                'arrival_time': current_process['Arrival Time'],
                'burst_time': current_process['Burst Time'],
                'start_time': current_process['start_time'],
                'completion_time': completion_time,
                'turnaround_time': turnaround_time,
                'waiting_time': waiting_time,
                'priority': current_process.get('Priority')
            })
            print(f"اكتملت العملية {current_process['Process ID']} في الوقت {completion_time}")
    
    print(f"عدد العمليات المكتملة: {len(completed)}")
    
    # ترتيب النتائج حسب وقت الإكمال
    return sorted(completed, key=lambda p: p['completion_time'])

def calculate_average_metrics(results):
    """حساب متوسط وقت الانتظار ووقت الدوران"""
    if not results:
        return {'avg_turnaround_time': 0, 'avg_waiting_time': 0}
        
    avg_turnaround = sum(p['turnaround_time'] for p in results) / len(results)
    avg_waiting = sum(p['waiting_time'] for p in results) / len(results)
    
    return {
        'avg_turnaround_time': avg_turnaround,
        'avg_waiting_time': avg_waiting
    }

def display_results(results, metrics):
    """عرض النتائج بتنسيق مناسب"""
    if not results:
        print("لا توجد نتائج للعرض!")
        return
        
    print("\nAlgorithm: SRTF (Shortest Remaining Time First)")
    print("-" * 120)
    print("Process ID | Arrival Time | Burst Time | Start Time | Completion Time | Turnaround Time | Waiting Time | Priority")
    print("-" * 120)
    
    for p in results:
        print(f"{p['id']:10} | {p['arrival_time']:11.2f} | {p['burst_time']:9.2f} | "
              f"{p['start_time']:10.2f} | {p['completion_time']:15.2f} | "
              f"{p['turnaround_time']:15.2f} | {p['waiting_time']:11.2f} | {p['priority']:8}")
    
    print("-" * 120)
    print(f"\nAverage Turnaround Time: {metrics['avg_turnaround_time']:.2f}")
    print(f"Average Waiting Time: {metrics['avg_waiting_time']:.2f}")

if __name__ == "__main__":
    # استخدام العمليات من main.global_processes
    processes = main.global_processes
    
    if processes:
        # تنفيذ خوارزمية SRTF
        results = srtf_algorithm(processes)
        
        # حساب المقاييس
        metrics = calculate_average_metrics(results)
        
        # عرض النتائج
        display_results(results, metrics)
    else:
        print("لم يتم العثور على عمليات صالحة في الملف")