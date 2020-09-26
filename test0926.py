import RPi.GPIO as GPIO
import dht11
import time
import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)
instance = dht11.DHT11(pin=14)

INTERVAL_SEC = 600
RETRY_SEC = 1
RETRY_TIMES = 10


def log_write():
    output_time = time.asctime()
    log_file = open("/var/log/python/moisture.log", "a+", encoding="UTF-8")
    log_file.write(output_time + " : " + str(Temp) +
                   ":" + str(Humid) + " : " + "V" + "\n")
    log_file.close()


def sqlite_insert():
    output_time = datetime.datetime.now()
    output_time = "{0:%Y-%m-%d:%H:%M:%S}".format(output_time)
    Temp = result.temperature
    Humid = result.humidity
    data = (output_time, Temp, Humid)
    #Temp = result.temperature
    #Humid = result.humidity
    users_ref.child(output_time).set({
        'date': output_time,
        'Temp': Temp,
        'Humid': Humid

    })


cred = credentials.Certificate(
    '/home/pi/Documents/moisture-6f216-firebase-adminsdk-7tuzg-71ecc7c30e.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://moisture-6f216.firebaseio.com/',
    'databaseAuthVariableovverride': {
        'uid' 'my-service-worker'
    }
})

users_ref = db.reference('/moisture')


def db_insert():
    output_time = datetime.datetime.now()
    output_time = "{0:%Y-%m-%d:%H:%M:%S:}".format(output_time)
    Temp = result.temperature
    Humid = result.humidity
    data = (output_time, Temp, Humid)
    Temp = result.temperature
    Humid = result.humidity
    users_ref.set({
        'date': output_time,
        'Temp': Temp,
        'Humid': Humid

    })


try:
    w = 0
    while True:
        result = instance.read()
        print("ok1")

        if result.is_valid():
            print("Last valid input: " + str(datetime.datetime.now()))
            print(" - Temperature: %-3.1f C" % result.temperature)
            print(" - Humidity: %-3.1f %%" % result.humidity)
            # log_write()
            if result.humidity > 0:
                sqlite_insert()
                w = 0
                time.sleep(INTERVAL_SEC)
                continue

        print("Invalid result(w=%d)" % w)
        if w <= RETRY_TIMES:
            w += 1
            time.sleep(RETRY_SEC)
        else:  # w > RETRY_TIMES
            print("err")
            w = 0
            time.sleep(INTERVAL_SEC)


except KeyboardInterrupt:
    print("Cleanup")
    GPIO.cleanup()


# データを取得する
print(users_ref.get())
