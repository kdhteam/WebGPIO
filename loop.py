from gpiozero import LED
from time import sleep

pump = LED(17)

while True:
    try:
        fh = open('auto_on', 'r')
        pump.on()
        sleep(60)
        pump.off()
        sleep(30)
    # Store configuration file values
    except FileNotFoundError:
            # Keep preset values
        sleep(30)
