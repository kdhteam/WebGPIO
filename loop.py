from gpiozero import LED
from time import sleep

pump = LED(17)
on_time = 2
off_time = 2
while True:
    try:
        fh = open('auto_on', 'r')
        pump.on()
        sleep(on_time * 60)
        pump.off()
        sleep(off_time * 60)
    # Store configuration file values
    except FileNotFoundError:
            # Keep preset values
        sleep(10)