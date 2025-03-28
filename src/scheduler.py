from flask_apscheduler import APScheduler

scheduler = APScheduler()


@scheduler.task('interval', seconds=60)
def get_mail_job():
    print('Планировщик работает')