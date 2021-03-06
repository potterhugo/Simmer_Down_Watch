try:
    import time
    import random
    
    # The pin configuration and set up is based on the tutorials/examples at
    # https://github.com/adafruit/Adafruit_Python_CharLCD (for the LCD screen) and
    # https://github.com/adafruit/Adafruit_Python_MCP3008 (for the analogue-digital converter)
	
    import RPi.GPIO as GPIO
    # Set up LCD character display
    import Adafruit_CharLCD as LCD

    # LCD screen pin configuration:
    lcd_en        = 24
    lcd_d4        = 23
    lcd_d5        = 17
    lcd_d6        = 27
    lcd_d7        = 22
    lcd_rs        = 25  
    lcd_backlight = 4

    # Define LCD column and row size for 16x2 LCD.
    lcd_columns = 16
    lcd_rows    = 2

    # Initialize the LCD using the pins above.
    lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                               lcd_columns, lcd_rows, lcd_backlight)
    FE = ["Fidget spinner","Finger Pull", "Hand massage"]#Fast and Emotinal
    ST = ["Arm massage", "Arm Pretzel", "Palm Push"]#Slaw and tierd 

    # Import MCP3008 library.
    import Adafruit_MCP3008

    # MCP3008 software pin configuration:
    CLK  = 18
    MISO = 4
    MOSI = 21
    CS   = 26
    mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

    # Setup GPIO LED pin
    LED_PIN = 12
    GPIO.setup(LED_PIN, GPIO.OUT)

    HEART_THRESH = 550
    NO_BEATS = 3 # Number of readings to take to calculate average b.p.m.

    # Welcome message
    lcd.clear()
    #########....1234567890123456
    lcd.message("Welcome to the\n"+
	        "SimmerDown Watch")
    time.sleep(5)

    OVER = False
    start_time = time.time()
    beat_times = []
    av_bpm = 70

    bpm_med = 75
    bpm_high = 90


    while True:
        heartrateV = mcp.read_adc(4)
        n = heartrateV // 15 - 20
	#lcd.message (str (heartrateV) + " ")

        printstr='%4d %4d' + '*'*n
        print(printstr % (heartrateV, n))
        if heartrateV > HEART_THRESH:
            if OVER == False:
		time_between = time.time() - start_time
		start_time = time.time()
		
		beat_times.append(time_between)
		if len(beat_times) == NO_BEATS:
                    lcd.clear()
                    av_time_between_beats =  sum(beat_times)/NO_BEATS
		    av_bpm = 60. / av_time_between_beats
                    #lcd.message('%.3f s\n%d b.p.m.' % (av_time_between_beats, av_bpm))
                    lcd.message('%d b.p.m.' % av_bpm)

		    beat_times = []
 	    OVER = True
	else:
            OVER = False
        if av_bpm < bpm_med: 
            lcd.message("\n:)")
           # GPIO.output(LED_PIN, False)
        elif av_bpm < bpm_high:
            lcd.message("\n:|")
           # GPIO.output(LED_PIN, False)
	elif av_bpm < 30 :
	    lcd.message("\n ZZZ"+" Try" + "fidget spinner")
        else:
            lcd.message("  :(" + "\n Try " +  "finger pull" )
            #GPIO.output(LED_PIN, True)
		
        time.sleep(0.05)
except KeyboardInterrupt:
    print('pressed ctrl-C')
    GPIO.cleanup()
finally:
    GPIO.cleanup()
