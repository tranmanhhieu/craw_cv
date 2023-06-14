import datetime
from dateutil.relativedelta import relativedelta
from linkedin import LinkedinBot
import pymongo
import config
import random
import re
input = "cmc"
list_key = ['telecom','job','company','media','group','networks','media','development','security','project','posts','technology','solution','manager','regulatory']


myclient = pymongo.MongoClient(f'mongodb://{config.USERNAME}:{config.PASSWORD}@localhost:{config.localhost}/')
mydb = myclient["craw_cv"]

bot = LinkedinBot()

# for key in list_key:
# keyword = input + " " + key
list_result = bot.search('viettel')
for result in list_result:
    time = result['time']
    time1 = result['crawled_at']
    list_time = ['m', 'h', 'mo', 'yr']
    if 'mo' in time:
        months = re.findall(r'\d+', time)
        time_delta = relativedelta(months=int(months[0]))
    elif 'm' in time:
        minutes = re.findall(r'\d+', time)
        time_delta = relativedelta(minutes=int(minutes[0]))
    elif 'yr' in time:
        years = re.findall(r'\d+', time)
        time_delta = relativedelta(years=int(years[0]))
    else:
        hours = re.findall(r'\d+', time)
        time_delta = relativedelta(hours=int(hours[0]))

    result['time'] = time1 - time_delta
    mydb['craw_cv'].insert_one(result)
