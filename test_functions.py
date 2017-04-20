from math import floor

def adding_time(start_time,add_time):
  '''
  Example:
    parameters:
      add_time = 30 #seconds
      start_time 09:30:30
    returns: 09:31:00
  '''
  max_minutes = 14
  update_time = start_time.split(':')
  hour = int(update_time[0])
  minute = int(update_time[1]) + int((max_minutes-(max_minutes-floor(add_time/60))))
  second = int(update_time[2]) + int((floor(add_time%60)))
  if second >= 60:
    minute += int(floor(second/60))
    second = second%60

  if minute >= 60:
    hour += int(floor(minute/60))
    minute = minute%60

  if hour >= 24:
    hour = hour%24
  return '%s:%s:%s'%(str(hour).zfill(2),str(minute).zfill(2),str(second).zfill(2))

def check_time(new_time_string, old_time_string):
  '''
  time_string.split(':')
  position 0 in time_string: hours
  position 1 in time_string: minutes
  position 2 in time_string: seconds
  '''
  if new_time_string == 'None' or old_time_string == 'None':
    return 0
  else:
    new_time = [int(value) for value in new_time_string.split(':')]
    old_time = [int(value) for value in old_time_string.split(':')]
    if new_time[0] == 0 and old_time[0] == 23:
      new_time[0] = 24
    hour = new_time[0] - old_time[0]
    minute = new_time[1] - old_time[1]
    second = new_time[2] - old_time[2]
    total_time = (hour*3600) + (minute*60) + second
    if total_time >= 900:
      return 0
    else:
      return 900 - total_time