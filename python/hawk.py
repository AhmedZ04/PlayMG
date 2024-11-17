import threading
import serial
import filter
import time
import pyfirmata

# Configure serial port
SERIAL_PORT = 'COM4'  # Replace with your Arduino's port
BAUD_RATE = 9600      # Match the Arduino's serial rate

# Initialize serial connection
'''
try:
    board = pyfirmata.ArduinoMega(SERIAL_PORT)
    print(f"Connected to {SERIAL_PORT}")
except Exception as e:
    print(f"Error: {e}")
    exit()
'''
def PortProcess(data, start_time):
    try:
            process = filter.Filter()
            process.filter(data, start_time)
    except KeyboardInterrupt:
        print(f"Stopping data collection and plotting results for sensors")

        process.plot()

def read_serial_data():
    try:
        board = pyfirmata.ArduinoMega(SERIAL_PORT)
        print(board)
        it = pyfirmata.util.Iterator(board)
        it.start()
        board.get_pin('a:0:i') # Piece of actual fucking shit how you have to call this even though its never referenceed AT FUCKING ALL in this
        board.get_pin('a:1:i') # Stupid fatiggerots

        start_time = time.time()
        while True:
            
            
            A0 = board.analog[0].read()
            if A0 != None:
                 A0 = A0*1000
                 
            A1 = board.analog[1].read()
            A2 = board.analog[2].read()
            A3 = board.analog[3].read()
            A4 = board.analog[4].read()
            
            
            process0 = threading.Thread(target=PortProcess, args=(A0, start_time))
            process1 = threading.Thread(target=PortProcess, args=(A1, start_time))
            process2 = threading.Thread(target=PortProcess, args=(A2, start_time))
            process3 = threading.Thread(target=PortProcess, args=(A3, start_time))
            process4 = threading.Thread(target=PortProcess, args=(A4, start_time))


            process0.start()
            #process1.start()
            #process2.start()
            #process3.start()
            #process4.start()

    except Exception as e:
        print(e)
          # Ignore invalid lines
    





if __name__ == "__main__":
    read_serial_data()