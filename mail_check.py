#! /usr/bin/python
 
import imaplib, time
#import RPi.GPIO as GPIO
 
GREEN_PIN = 25
RED_PIN = 24
 
class MailChecker:
    def __init__(self, server, port):
    #    GPIO.setmode(GPIO.BCM)
     #   GPIO.setup(GREEN_PIN, GPIO.OUT)
      #  GPIO.setup(RED_PIN, GPIO.OUT)
       # GPIO.setwarnings(False)
 
        try:
            self.m = imaplib.IMAP4_SSL(server, port)
        except:
            self.do_error("Unable to contact server")
 
    def do_error(self, error):
        # maybe flash another error LED
        print(error)
        exit()
 
 
    def log_in(self, user, password):
        try:
            self.m.login(user, password)
        except:
            self.do_error("Unable to log in")
 
    def check_mail(self):
    	type, data = self.m.select('INBOX')
    	print type, data
    	num_msgs = int(data[0])
    	print 'There are %d messages in INBOX' % num_msgs
        try:
            self.m.select('INBOX')
            type, data = self.m.search(None, "UNSEEN")
        except:
            self.do_error("Unable to check messages")
 
        if type == "NO":
            self.do_error("Problem checking messages")
 
        self.report(data)
 
    def start_checking(self):
#        while True:
         self.check_mail()
         #   time.sleep(interval)
 
    def report(self, data):
        message_count = len(data[0].split())
        if message_count > 0:
            print("You've got %i new messages" %
            message_count)
        #    GPIO.output(RED_PIN, GPIO.LOW)
         #   for i in range(1, 100):
          #          GPIO.output(GREEN_PIN, GPIO.LOW)
           #         time.sleep(.2)
            #        GPIO.output(GREEN_PIN, GPIO.HIGH)
             #       time.sleep(.2)
        else:
            print("No new mail right now")
           # GPIO.output(GREEN_PIN, GPIO.LOW)
           # GPIO.output(RED_PIN, GPIO.HIGH)
 
if __name__ == "__main__":
    user = "savusfridge"
    password = "frigider"
    server = "imap.gmail.com"
    port = 993 
    # or whatever port you need to use
 
    checker = MailChecker(server, port)
    checker.log_in(user, password)
    checker.start_checking()
