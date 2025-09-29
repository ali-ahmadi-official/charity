import os
import sys
import django
from datetime import datetime

sys.path.append('/home/charitytest/charity')


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'charity.settings')
django.setup()

from referees.models import Recipient

def run():
    print(f"[{datetime.now()}] شروع به‌روزرسانی گیرنده‌ها...")
    for r in Recipient.objects.all():
        try:
            r.save()
        except Exception as e:
            print(f"خطا در ذخیره گیرنده با شناسه {r.id}: {e}")
    print(f"[{datetime.now()}] پایان به‌روزرسانی.")

if __name__ == "__main__":
    run()