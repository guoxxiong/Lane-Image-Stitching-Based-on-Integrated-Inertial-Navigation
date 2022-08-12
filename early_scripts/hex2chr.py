from datetime import datetime, timedelta

now_time = datetime.now()
utc_time = now_time - timedelta(hours=8)
print(now_time, utc_time)

