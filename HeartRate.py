import serial
import time

# Set up serial connection with Arduino
ser = serial.Serial('COM6', 115200, timeout=1)

# Record heart rate data for 30 seconds
duration = 30
start_time = time.time()
data = []
while (time.time() - start_time) < duration:
    # Read data from serial port
    line = ser.readline().decode().strip()
    try:
        value = float(line)
        data.append(value)
    except ValueError:
        pass

# Close serial connection
ser.close()

# Take the last 10 values and calculate their average
last_ten = data[-10:]
average = sum(last_ten) / len(last_ten)

# Print the average value
#print("Heart rate:", average)

# Compare the average value with the given conditions
if average < 40:
    print("Low heart rate", average)
elif average > 100:
    print("High heart rate", average)
else:
    print("Normal heart rate", average)