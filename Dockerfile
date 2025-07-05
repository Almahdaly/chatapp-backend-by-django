# استخدم صورة بايثون
FROM python:3.11-slim

# إعداد مجلد العمل داخل الحاوية
WORKDIR /app

# نسخ ملفات المشروع
COPY . .

# تثبيت المتطلبات
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# تجميع الملفات الثابتة
RUN python manage.py collectstatic --noinput

# فتح البورت
EXPOSE 8000

# أمر التشغيل الافتراضي
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
