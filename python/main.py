#V1.2.0
import sys
import glob
import serial
import tkinter as tk
import threading

root = tk.Tk()
root.title("Serial Port Data Print - AtrivaTECH")
root.configure(background='#ebebeb')

# Set icon if it exists
try:
    root.iconbitmap("logo.ico")
except tk.TclError:
    pass  # Icon file not found, continue without it

def display_about():
    about_window = tk.Toplevel(root)
    about_window.title("About")
    about_text = "Serial Port Data Print\n\nAtrivaTECH\natrivatech.com \n\nVersion 1.2.0\n\nConnect to a serial port and print data received via Serial.\n\nCertified Open-Source. \n\n© 2024-2025 AtrivaTECH (A Unit of Atrivatech P. Ltd.). All rights reserved. \n\n A product for Engineers, Hobbyists and Professionals. \n Distributed for free use and non Commercial purposes.\n \nThis software purely runs locally and does not send data to any server.\nFor more information, visit atrivatech.com"
    about_label = tk.Label(about_window, text=about_text, padx=20, pady=20)
    about_label.pack()

def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def connect_serial():
    global ser
    selected_port = port_var.get()
    baud_rate = baud_var.get()
    if selected_port and baud_rate:
        try:
            ser = serial.Serial(selected_port, baud_rate, timeout=1)
            status_label.config(text=f"Connected to {selected_port} at {baud_rate} baud rate", fg="green")
            printdata()
        except serial.SerialException:
            status_label.config(text="Failed to connect", fg="red")
    else:
        status_label.config(text="Please select port and baud rate", fg="red")

def disconnect_serial():
    global ser
    if ser:
        ser.close()
        status_label.config(text="Serial port disconnected", fg="blue")

def clear_screen():
    text.delete('1.0', tk.END)

def dataread():
    global ser
    if ser:
        line = ser.readline()
        if line:
            return line.decode().strip()
    return ""

def printdata():
    data = dataread()
    if data:
        text.insert(tk.END, data + '\n')
        text.see(tk.END)  # Scroll to the bottom
    root.after(refresh_rate_var.get(), printdata)

def scan_ports():
    status_label.config(text="Scanning for COM ports...", fg="orange")
    root.update()
    ports = serial_ports()
    port_var.set(ports[0] if ports else "")
    port_menu['menu'].delete(0, 'end')
    for port in ports:
        port_menu['menu'].add_command(label=port, command=tk._setit(port_var, port))
    status_label.config(text="Scan complete", fg="green")

def scan_ports_thread():
    scanning_thread = threading.Thread(target=scan_ports)
    scanning_thread.start()


port_label = tk.Label(root, text="COM Port:")
port_label.grid(row=0, column=0)
port_var = tk.StringVar(root)
port_menu = tk.OptionMenu(root, port_var, "")
port_menu.grid(row=0, column=2)

scan_ports_button = tk.Button(root, text="Scan Ports", command=scan_ports_thread)
scan_ports_button.grid(row=6, column=2)

baud_label = tk.Label(root, text="Baud Rate:")
baud_label.grid(row=1, column=0)
baud_var = tk.IntVar(root)
baud_entry = tk.Entry(root, textvariable=baud_var)
baud_entry.grid(row=1, column=2)

refresh_rate_label = tk.Label(root, text="Refresh Rate (ms):")
refresh_rate_label.grid(row=2, column=0)
refresh_rate_var = tk.IntVar(root)
refresh_rate_entry = tk.Entry(root, textvariable=refresh_rate_var)
refresh_rate_entry.grid(row=2, column=2)

connect_button = tk.Button(root, text="Connect", command=lambda: connect_serial())
connect_button.grid(row=3, column=0)
disconnect_button = tk.Button(root, text="Disconnect", command=lambda: disconnect_serial())
disconnect_button.grid(row=3, column=2)

clear_button = tk.Button(root, text="Clear Screen", command=lambda: clear_screen())
clear_button.grid(row=6, column=0)

status_label = tk.Label(root, text="")
status_label.grid(row=4, columnspan=3)

about_button = tk.Button(root, text="ℹ", font=("Arial", 12), command=display_about, bg="white", fg="black", relief="flat")
about_button.grid(row=6, column=1)

text = tk.Text(root)
text.grid(row=5, columnspan=3)

scan_ports_thread() 

root.mainloop()
