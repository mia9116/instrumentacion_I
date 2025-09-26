import threading
import time

class KeyboardThread(threading.Thread):

    def __init__(self, input_cbk = None, name='keyboard-input-thread'):
        self.input_cbk = input_cbk
        super(KeyboardThread, self).__init__(name=name)
        self.start()

    def run(self):
        while True:
            self.input_cbk(input()) #waits to get input + Return

def input_teclado(inp):
    #evaluate the keyboard input
    global start
    global state
    global States
    match inp:
        case "start":
            start = True
            print("Inicia la maquina")
        case "stop":
            start = False
            print("Termina la maquina")
start = False
            
class States:
    Idle = 0
    Start = 1

#start the Keyboard thread
kthread = KeyboardThread(input_teclado)

state = States.Idle
start = False

while True:
    match state:
        case States.Idle:
            if start == True:
                state = States.Start
                print("Estado actual: Start")
        case States.Start:
            if start == False:
                state = States.Idle
                print("Estado actual: Idle")