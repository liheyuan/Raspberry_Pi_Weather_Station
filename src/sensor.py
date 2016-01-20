import sys
import os
import Adafruit_DHT
import time
import datetime
import json
from config import *

sensor_args = { '11': Adafruit_DHT.DHT11,
        '22': Adafruit_DHT.DHT22,
        '2302': Adafruit_DHT.AM2302 }

sensor = sensor_args.get(SENSOR, None)

if not sensor:
        print 'Invalid sensor type'
        sys.exit(1)

humidity, temperature = Adafruit_DHT.read_retry(sensor, GPIO)

if humidity is not None and temperature is not None:
        # get ts
        ts = int(time.time())
        date = datetime.datetime.now().strftime('%Y%m%d')
        # make data json
        data = {"temperature": temperature, "humidity": humidity, "timestamp": ts}
        # Save data
        try:
                os.mkdir(DATA_DIR)
        except:
                pass
        file = os.path.join(DATA_DIR, date)
        open(file, "a+").write(json.dumps(data)+"\n")
        print 'Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity)
else:
        print 'Failed to get reading. Try again!'
        sys.exit(1)
