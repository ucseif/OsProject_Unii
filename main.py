import pandas as pd

# قراءة الملف الإخراج من Process Generator
try:
    # تجاهل السطور الأولى (التعليقات والفواصل)
    df = pd.read_csv('output.txt', sep='|', skiprows=4, comment='-', engine='python')

    # إزالة المسافات الزائدة من أسماء الأعمدة
    df.columns = df.columns.str.strip()

    # التحقق من الأعمدة
    #print("Columns in DataFrame:", df.columns)

    # تحويل الأعمدة إلى أنواعها الصحيحة
    df['Process ID'] = df['Process ID'].astype(int)
    df['Arrival Time'] = df['Arrival Time'].astype(float)
    df['Burst Time'] = df['Burst Time'].astype(float)
    df['Priority'] = df['Priority'].astype(int)

    # تحويل البيانات إلى قائمة من القوائم
    processes = df.to_dict('records')

    # حفظ العمليات في متغير عالمي
    global_processes = processes

except Exception as e:
    print("Error while reading the file:", e)