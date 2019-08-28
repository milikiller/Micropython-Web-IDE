import machine
import utime
import network
import ubinascii
import time

def do_connect():

    AP_Name = "ESP32-AP"
    AP_Pass = "123456789"

    secWifi={
      'chata-dolce1':'',
      'LonkKnotHomeAut':'cMTWeMosD1',
      'Spackovi':'123456789'
    }

    authmode={
      0:'Open',
      1:'WEP',
      2:'WPA-PSK',
      3:'WPA2-PSK',
      4:'WPA/WPA2-PSK'
    }

    hidden={
      0:'false',
      1:'true'
    }

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.disconnect()
    nets = wlan.scan()
    for net in nets:
        print('Network: SSID:',net[0],', MAC:',ubinascii.hexlify(net[1]),', Channel:',net[2],', RSSI:',net[3],', Auth Mode:',authmode[net[4]],', Hidden:',hidden[net[5]])
        if net[0].decode() in secWifi:
            print('Network found!')
            wlan.connect(net[0].decode(),secWifi[net[0].decode()])
            deadline = utime.ticks_add(utime.ticks_ms(), 10000)
            while (utime.ticks_diff(deadline, utime.ticks_ms()) > 0) and not wlan.isconnected():
                machine.idle()
            if wlan.isconnected():
                print('Network config:', wlan.ifconfig())
                break
            else:
                print('WLAN connection failed!')
        else:
            print('Network not in list')

    if not wlan.isconnected():
        print('Starting AP')
        ap = network.WLAN(network.AP_IF)
        ap.active(True)
        if (len(AP_Pass) > 0):
            ap.config(essid=AP_Name, authmode=network.AUTH_WPA_WPA2_PSK, password=AP_Pass)
        else:
            ap.config(essid=AP_Name)
        print('AP Started')

do_connect()
time.sleep_ms(500)