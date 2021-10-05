from sys import exit
from pynput.keyboard import Key, KeyCode, Listener

# exit on ctrl-q
def fun_exit_ctrl_q() :
    exit( print( "Exit on user request (Ctrl+Q)" ) )

# exit on Esc
def fun_exit_esc() :
    exit( print( "Exit on user request (Esc)" ) )

# use frozenset as sets are not hashable - so they can't be used as keys, 
# map functions to keysets
COMBINATIONS = {
    frozenset([Key.shift_l, KeyCode(char='q')]): fun_exit_ctrl_q,
    frozenset([Key.shift_l, KeyCode(char='Q')]): fun_exit_ctrl_q,
    frozenset([Key.esc]): fun_exit_esc
}

# register pressed keys
def on_press(key) :
    current.add(key)
    if (frozenset(current) in COMBINATIONS) :
        COMBINATIONS[frozenset(current)]()

# unregister released keys
def on_release(key) :
    current.remove(key)

# Get currently pressed keys
current = set()

while (1) :
    
    input_val = input("Enter value: ")
    with Listener(on_pres = on_press, on_release = on_release) as listener:
        listener.join