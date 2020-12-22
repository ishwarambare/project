from blog.models import User
from django.core.mail import send_mail
import datetime


def my_cron_job():
    user = User.objects.all()
    print(user)
    print('hello ishwar')


def my_new_cron_job():
    print('hello ishwar')
    f = open('/home/ishwar/Desktop/file123.txt', 'a')
    f.write('ishwar')
    f.close()


def send_birthday_wish():
    date = datetime.date.today()
    for i in User.objects.all():
        if date == i.birth_date:
            send_mail("birthday wish", f"Happy birthday {i.username}", "ambareishu@gmail.com", [i.email])
