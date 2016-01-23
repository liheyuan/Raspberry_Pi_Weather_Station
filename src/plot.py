#-*- coding:utf-8 -*-
import traceback
import codecs
import json
import sys
import time
import datetime
import os
import matplotlib.pyplot as plt
from config import *

# get time tuple
DATE_STR = datetime.datetime.now().strftime('%Y%m%d')
today_obj = datetime.date.today()
DAY_BEGIN = int(today_obj.strftime("%s"))
tomorrow_obj = today_obj + datetime.timedelta(1)
DAY_END = int(tomorrow_obj.strftime("%s"))

# Open file
FILE = os.path.join(DATA_DIR, DATE_STR)
try:
    os.mkdir(PNG_DIR)
except:
    pass
PNG_FILE = os.path.join(PNG_DIR, "%s.png"%DATE_STR)

if not os.path.exists(FILE):
    print FILE, "not exists"
    sys.exit(-1)

temp_list = []
humi_list = []
for line in codecs.open(FILE).readlines():
    try:
        obj = json.loads(line.strip())
        temp = obj.get("temperature", None)
        humi = obj.get("humidity", None)
        ts = obj.get("timestamp", None)
        #print temp, humi, ts
        if not ts or not temp or not humi:
            continue
        temp_list.append((ts, temp))
        humi_list.append((ts, humi))
        # min & max
    except:
        #print traceback.print_exc()
        pass

# calculate y min & max
def my_max(arr):
    max_key = 0
    max_val = 0
    for e in arr:
        if e[1] > max_val:
            (max_key, max_val) = e
    return (max_key, max_val)

def my_min(arr):
    min_key = 0
    min_val = 999999
    for e in arr:
        if e[1] < min_val:
            (min_key, min_val) = e
    return (min_key, min_val)

(max_temp_x, max_temp) = my_max(temp_list)
(max_humi_x, max_humi) = my_max(humi_list)
(min_temp_x, min_temp) = my_min(temp_list)
(min_humi_x, min_humi) = my_min(humi_list)

# calculate annotation min & max
anno_list = []
#anno_list.append((min_humi_x, min_humi, False))
#anno_list.append((max_humi_x, max_humi, True))
anno_list.append((min_temp_x, min_temp, False))
anno_list.append((max_temp_x, max_temp, True))
if len(temp_list) >= 1:
    last_x, last_y = temp_list[-1]
    anno_list.append((last_x, last_y, True))

# calculate x min & max
min_x = DAY_BEGIN
max_x = DAY_END

# calculate x ticks
ticks_list = []
tmp_ts = DAY_BEGIN
for i in xrange(0, 25, 3):
    ticks_list.append(((tmp_ts + 3600 * i), "%s:00"%(i)))
    
# set x & y axis limit
axes = plt.gca()
axes.set_xlim([min_x, max_x])
axes.set_ylim([min(min_temp, min_humi, 0), max(max_temp, max_humi) * 1.4])
# set x ticks
plt.xticks([e[0] for e in ticks_list], [e[1] for e in ticks_list])
# set data
plt.title(u"Temperature & Humidity change during %s" % DATE_STR)
plt.plot([e[0] for e in temp_list], [e[1] for e in temp_list], "m", label="Temperature Cent.")
plt.plot([e[0] for e in humi_list], [e[1] for e in humi_list], "c", label=u"Humidity %")
plt.legend()
# set annotation
for e in anno_list:
    (x, y, isMax) = e
    if isMax:
        x_delta = 0
        y_delta = 4.5
    else:
        y_delta = 0
        x_delta = -5
    plt.annotate('%s' % y, xy = (x, y), xytext=(x + x_delta, y + y_delta), arrowprops=dict(facecolor='black', shrink=0.15))
#plt.show()
plt.savefig(PNG_FILE)
