import time, datetime
import pigpio

waterFlow = 0
#flowGpio = 13
flowGpio = [13,19,26]
pi = pigpio.pi()
flowCallback=[0,0,0]
for i in range(3):
    pi.set_mode(flowGpio[i], pigpio.INPUT)
    pi.set_pull_up_down(flowGpio[i], pigpio.PUD_DOWN)
    flowCallback[i] = pi.callback(flowGpio[i], pigpio.FALLING_EDGE)
    #print(flowCallback)

old_count0 = 0
old_count1 = 0
old_count2 = 0


#triggerTime = datetime.datetime.today() - datetime.timedelta(weeks=1)  # Initialize it to more than a day ago

while True:
   time.sleep(4)
   count0 = flowCallback[0].tally()
   count1 = flowCallback[1].tally()
   count2 = flowCallback[2].tally()

   waterFlow0 = count0 - old_count0
   waterFlow1 = count1 - old_count1
   waterFlow2 = count2 - old_count2

   print("counted {},{},{} pulses".format(waterFlow0,waterFlow1,waterFlow2))
   #yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
   #print("Waterflow over limit: " + str(waterFlow))
   old_count0 = count0
   old_count1 = count1
   old_count2 = count2
   
   # Only send at most one message per day so check if the last trigger was more than 24hours ago
   #if ( (waterFlow > triggerMin) & (triggerTime < yesterday) ):
   #    triggerTime = datetime.datetime.today()
   #    print("Waterflow over limit: " + str(waterFlow))
   #old_count = count

pi.stop()