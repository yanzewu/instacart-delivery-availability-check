from helium import *
from time import sleep
import json
import requests
from win10toast import ToastNotifier
import datetime

# -- data -- #
credentials = json.loads(''.join(open("credentials.json").readlines()))
INSTACART_EMAIL = credentials["INSTACART_EMAIL"]
INSTACART_PASSWORD = credentials["INSTACART_PASSWORD"]
STORE_LIST = credentials["STORE_LIST"]
INSTACART_BASE_URL = credentials["INSTACART_BASE_URL"]
INSTACART_DELIVERY_URL = credentials["INSTACART_DELIVERY_URL"]
NOTIFICATION_EMAIL = credentials["NOTIFICATION_EMAIL"]

wait_time = 60 # in seconds

# -- login logic -- #
start_chrome(INSTACART_BASE_URL)#, headless=True)
click(Link("Log In"))
write(INSTACART_EMAIL, into="Email address")
write(INSTACART_PASSWORD, into="Password")
click(Button("Log In"))
wait_until(Link("See delivery times").exists)


# -- check store logic -- #
def check_delivery_times_for_store(store_name):
    go_to(INSTACART_DELIVERY_URL.format(store_name))
    sleep(7)
    if Text("No delivery times available").exists():
        return False, "No Delivery times available. Try again later?"
    else:
        return (
            True,
            "Delivery times found for {}! Please check soon :)".format(store_name),
        )


# -- send email -- #
def send_simple_message(message):
    print("[%s] Available!" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    t = ToastNotifier()
    t.show_toast("Instacart", "Available!", duration=10, threaded=True)
    return



# -- check all stores in list and notify -- #
def main():
    for store in STORE_LIST:
        availability, message = check_delivery_times_for_store(store)
        if availability:
            send_simple_message(message)
        else:
            print("[%s] Checked" % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


if __name__ == "__main__":
    t = ToastNotifier()
    t.show_toast("Instacart", "Initialized", duration=10, threaded=True)
    while True:
        main()
        sleep(wait_time - 7)
