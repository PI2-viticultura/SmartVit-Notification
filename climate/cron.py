from crontab import CronTab
import pathlib

cron = CronTab(user='lucas')
python_path = '/usr/bin/python3 ' + str(pathlib.Path().absolute()) + '/climate/main.py'
job = cron.new(command=python_path)
job.minute.on(0)
job.hour.on(0)
job.hour.also.on(12)

cron.write()