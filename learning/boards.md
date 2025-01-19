## Boards

Circuit python has its own commands for looking up boards:

>circuitpython_setboard -l

Will return all list of supported boards

> circuitpython_setboard -l espressif

Will help us find all supported boards for espressif,
currently we are using `Qualia ESP32-S3 RGB666 40p TFT`. 
From the list returned, we identify `adafruit_qualia_s3_rgb666`.

Another way to identify the board is to look into the `boot_out.txt` file
located in the CIRCUITPY drive, and look at the value of `Board ID:`

> circuitpython_setboard adafruit_qualia_s3_rgb666

Will set our board as the `adafruit_qualia_s3_rgb666` with the command: 
```commandline
circuitpython_setboard adafruit_qualia_s3_rgb666
```

## Terminal IO (tio)

In order to visualize the board communication we will need to install 
`tio` that stands for [Terminal IO](https://formulae.brew.sh/formula/tio).

To check installation/version use:
```commandline
tio --version
```

Check how the board is referenced in terminal (macOS):
```commandline
ls /dev/tty.*
```
Or using `tio` (list is much longer):
```commandline
tio -l
```
Example output from command `ls /dev/tty.*`:
```commandline
/dev/tty.Bluetooth-Incoming-Port /dev/tty.usbmodem47D4DBD9E4431   /dev/tty.wlan-debug
```
Validate the board referenced as `usbmodemXXX`, in this case `/dev/tty.usbmodem47D4DBD9E4431`.

Connect to the board using `tio`:
```commandline
tio /dev/tty.usbmodem47D4DBD9E4431
```
The output should be something similar to:
```commandline
tio 3.8
Press ctrl-t q to quit
Connected to /dev/tty.usbmodem47D4DBD9E4431
Auto-reload is on. Simply save files over USB to run them or enter REPL to disable.

Press any key to enter the REPL. Use CTRL-D to reload.
```

At this point `tio` is running in the terminal window, and any code change will reflect an output on the terminal io. 




