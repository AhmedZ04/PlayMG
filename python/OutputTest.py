import pyfirmata
import time

board = pyfirmata.ArduinoMega('COM4', baudrate=9600)
it = pyfirmata.util.Iterator(board)
it.start()


board.get_pin('a:0:i')
board.get_pin('a:1:i')
board.get_pin('a:2:i')
board.get_pin('a:3:i')
board.get_pin('a:4:i')
board.get_pin('a:5:i')



while True:
    start = time.time()

    print(board.analog[0].read())
    print(board.analog[1].read())
    print(board.analog[2].read())
    print(board.analog[3].read())
    print(board.analog[4].read())

    print(f"processing time: {time.time() - start}")
    time.sleep(0.1)
    