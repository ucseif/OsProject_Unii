import pandas as pd
import numpy as np

def generate_processes(input_file, output_file):
    try:
        # قراءة ملف الإدخال الذي يحتوي على معاملات التوزيعات
        with open(input_file, 'r') as f:  # فتح ملف الإدخال للقراءة
            lines = f.readlines()  # قراءة جميع السطور في الملف وتخزينها في قائمة

        # استخراج عدد العمليات من السطر الأول
        n = int(lines[0].strip())  # تحويل السطر الأول إلى عدد صحيح (عدد العمليات)

        # استخراج المتوسط والانحراف المعياري لوقت الوصول من السطر الثاني
        arrival_mean, arrival_std = map(float, lines[1].strip().split())  # تقسيم السطر إلى قيمتين عدديتين

        # استخراج المتوسط والانحراف المعياري لوقت التنفيذ من السطر الثالث
        burst_mean, burst_std = map(float, lines[2].strip().split())  # تقسيم السطر إلى قيمتين عدديتين

        # استخراج قيمة Lambda لتوزيع الأولوية من السطر الرابع
        lambda_priority = float(lines[3].strip())  # تحويل السطر إلى عدد عشري

        # توليد بيانات العمليات باستخدام التوزيعات المحددة
        arrival_times = np.random.normal(arrival_mean, arrival_std, n)  # توليد أوقات الوصول باستخدام توزيع طبيعي
        burst_times = np.random.normal(burst_mean, burst_std, n)  # توليد أوقات التنفيذ باستخدام توزيع طبيعي
        priorities = np.random.poisson(lambda_priority, n)  # توليد الأولويات باستخدام توزيع بواسون

        # إنشاء جدول بيانات (DataFrame) لحفظ العمليات
        data = {
            'Process ID': range(1, n + 1),  # أرقام العمليات من 1 إلى n (عدد صحيح)
            'Arrival Time': arrival_times,  # أوقات الوصول المُولدة
            'Burst Time': burst_times,  # أوقات التنفيذ المُولدة
            'Priority': priorities  # الأولويات المُولدة
        }
        df = pd.DataFrame(data)  # إنشاء جدول بيانات باستخدام Pandas

        # إضافة خطوط الفصل لتحسين التنسيق
        separator = "-" * 50  # إنشاء سلسلة من شرطات (-) لاستخدامها كفاصل بين الأقسام

        # كتابة البيانات إلى ملف الإخراج
        with open(output_file, 'w') as f:  # فتح ملف الإخراج للكتابة
            f.write("# Output File for Process Generator Module\n")  # كتابة تعليق يوضح نوع الملف
            f.write(f"# Number of Processes: {n}\n\n")  # كتابة عدد العمليات

            # كتابة الرأس (Header) والفاصل الأول
            f.write(separator + "\n")  # كتابة خط فاصل
            f.write("Process ID | Arrival Time | Burst Time | Priority\n")  # كتابة عناوين الأعمدة
            f.write(separator + "\n")  # كتابة خط فاصل آخر

            # كتابة بيانات الجدول لكل عملية
            for index, row in df.iterrows():  # التكرار على كل صف في الجدول
                # كتابة كل عمود مع تنسيق المسافات
                f.write(
                    f"{int(row['Process ID']):7}    | {row['Arrival Time']:9.2f}    | {row['Burst Time']:7.2f}    | {int(row['Priority']):8}\n"
                )

            # كتابة الفاصل الأخير
            f.write(separator + "\n")  # كتابة خط فاصل في نهاية الجدول

        print("Output file has been created successfully!\n")  # طباعة رسالة تأكيد بأن الملف تم إنشاؤه بنجاح
        display_output(output_file)

    except Exception as e:
        print("Error:", e)  # طباعة أي خطأ يحدث أثناء تنفيذ الكود

def display_output(output_file):
    """
    هذه الدالة تقوم بقراءة محتوى ملف الإخراج وطباعته على الشاشة.
    """
    try:
        with open(output_file, 'r') as f:  # فتح ملف الإخراج للقراءة
           # print("\n--- Displaying Output File Content ---\n")
            print(f.read())  # طباعة محتوى الملف بالكامل
    except Exception as e:
        print("Error while displaying output:", e)  # طباعة أي خطأ يحدث أثناء قراءة الملف

# تشغيل الدالة باستخدام ملفات الإدخال والإخراج
generate_processes("input.txt", "output.txt")