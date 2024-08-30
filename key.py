import threading
from pynput import keyboard
import pynput
import time

my_key=["a","l","t"]#请使用非特殊键
front=2 #起始工具编号
my_len =3  #工具数量
flag=False
i=0
j=0
cv=threading.Condition()

def on_press(key):
    
    global j
    global flag
    try:
        
        if(key==pynput.keyboard.KeyCode.from_char(my_key[j])):
            j+=1
            if(j==len(my_key)):
                flag=True
                j=0
        else:
            j=0
            flag=False
        if(flag):
            flag=False
            global i
            with cv:
                i += 1
                i = i % my_len       
                cv.notify()  
    except AttributeError:
        pass
def t1():
    with keyboard.Listener(
        on_press=on_press
        ) as listener:
        listener.join()
def press_key(ctr,i):
    for num in range(len(my_key)):
        ctr.press(pynput.keyboard.Key.backspace)
        ctr.release(pynput.keyboard.Key.backspace)
    global front
    str_i=str(i+front)  
    
    # time.sleep(0.1)   # 增加延迟
    ctr.press(pynput.keyboard.Key.alt_l)
    # time.sleep(0.05)  # 增加延迟
    ctr.press(str_i)
    # time.sleep(0.05)  # 增加延迟
    ctr.release(str_i)
    # time.sleep(0.05)  # 增加延迟
    ctr.release(pynput.keyboard.Key.alt_l)
    # time.sleep(0.2)   # 增加延迟
def main_loop():
    ctr = keyboard.Controller()
    # time.sleep(1)
    while True:
        with cv:
            cv.wait()  
        press_key(ctr,i)

if __name__ == '__main__':
    thread = threading.Thread(target=t1)
    thread.daemon = True  
    thread.start()
    
    with cv:
        cv.notify()  
    main_loop()
    