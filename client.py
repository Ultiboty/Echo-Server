import socket, threading
from socket import *
from scapy.all import *
from tkinter import *
import tkinter.font as font


def shut_down(sock, win):
    sock.close()
    win.destroy()


def get_server_info():
    a = sniff(filter='udp and dst 255.255.255.255 and len>=53 and len<= 63', count=1)
    return a[0].payload.load.decode('utf-8')


def connect_to_server():
    try:
        addr = get_server_info()
        addr = (addr[0:len(addr) - 5], int(addr[len(addr) - 5:len(addr) + 1]))
        client_sock = socket.socket(AF_INET, SOCK_STREAM)
        client_sock.connect(addr)
    except:
        connect_to_server()
    return client_sock


def send_data(sock, entry, text):
    data = entry.get()
    if not data:
        return
    sock.send(data.encode('utf-8'))
    entry.delete(0, END)  # clear the entry
    txt_insert(text, data)


def receive_data(sock, txt, win):
    tag_name = 0
    while True:
        data = sock.recv(1024).decode('utf-8')
        if not data or data == 'exiting the session' or data == 'SERVER SHUTTING DOWN':
            break
        txt_insert(txt, data)
        # this is for highlighting the server messages in different color
        num_lines = txt.get('1.0', END).count('\n') - 1
        txt.tag_add(str(tag_name), str(num_lines) + '.0', str(num_lines) + '.end')
        txt.tag_configure(str(tag_name), foreground='green')
        tag_name += 1
    shut_down(sock, win)


def txt_insert(txt, message):
    txt.configure(state='normal')
    txt.insert(END, f"{message}\n")
    txt.configure(state='disabled')


def main_logic(win, waiting):
    # connect to the server
    client_sock = connect_to_server()
    # after we connected, destroy the waiting widget
    waiting.destroy()
    win['background'] = 'black'

    # make the writing box
    entry = Entry(win, width=50, font='Arial 16')
    entry.pack(side=BOTTOM, padx=5, pady=10, fill=X)

    # make the command list
    commands = Text(win, wrap=WORD, state='disabled', bg='#313c5e', width=45, font='Arial 11')
    commands.pack(side=RIGHT, pady=10, padx=10, fill=Y)
    txt_insert(commands, 'time: gives server time\n\nmission: gives a random mission for life improvement\n\npeople: gives the amount of people in server\n\nrun time: gives how much time the server has been running for')
    num_lines = commands.get('1.0', END).count('\n') - 1
    commands.tag_add('tag', '1.0', str(num_lines) + '.end')
    commands.tag_configure('tag', foreground='red')

    # make the scrollbar widget
    scrollbar = Scrollbar(win)
    scrollbar.pack(side=RIGHT, fill=Y, pady=10)

    # make the text widget
    text = Text(win, wrap=WORD, state='disabled', bg='#313c5e', font='Arial 11')
    text.pack(side=LEFT, pady=10, fill=BOTH, expand=True)
    text.configure(yscrollcommand=scrollbar.set)
    scrollbar.config(command=text.yview)

    entry.bind('<Return>', lambda x: send_data(client_sock, entry, text))  # bind enter to send data

    # start the receive message thread
    receive_thread = threading.Thread(target=receive_data, args=(client_sock, text, win), daemon=True)
    receive_thread.start()


def waiting_screen(win):
    # clear the screen
    for widgets in win.winfo_children():
        widgets.destroy()

    # waiting for connection screen
    waiting = Label(win, text='Waiting for connection...', bg='#313c5e', font=font.Font(size=20))
    waiting.pack(side=TOP, expand=True)
    logic_thread = threading.Thread(target=main_logic, args=(win, waiting,), daemon=True)
    logic_thread.start()


def start_screen():
    """this bit is in order to stabilize the window at the center of the screen"""

    win = Tk()  # Creating instance of Tk class
    window_height = 500
    window_width = 900

    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    x_cordinate = int((screen_width / 2) - (window_width / 2))
    y_cordinate = int((screen_height / 2) - (window_height / 2))

    win.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

    win.minsize(500, 275)

    """this bit will create the start window"""

    win['background'] = '#313c5e'
    my_font = font.Font(size=20)

    message = Label(win, text='Welcome to echo server!', bg='#313c5e', font=my_font)
    message.pack(side=TOP, expand=False)

    start_button = Button(win, text='Start session', font=my_font, command=lambda: waiting_screen(win))
    start_button.pack(side=TOP, expand=True)

    win.mainloop()


if __name__ == '__main__':
    start_screen()

