
import tkinter as tk
import tkinter.ttk
import socket
import sys
import json

TITLE = "OnOff v0.0"
TITLE_ICO = "..."
TITLE_IMAGE = "title_image.gif"
MAIN_WIN_WIDTH = 720
MAIN_WIN_HEIGHT = 1280

#test variable
#var = {'Q1':'off', 'Q2':'off', 'Q3':'off', 'Q4':'off'}
var = {'Q1':'off'}

# hier are setting IP - Adress from Nextion Display
ip = '10.0.0.102'

class MainWindowFrame(object):
    def __init__(self, parent):
        self.parent = parent
        self.tk = tk

        # Taps
        self.note = tkinter.ttk.Notebook(parent.main_win)
        self.tab1 = tkinter.ttk.Frame(self.note)

        self.note.add(self.tab1, text="Nextion")

        self.note.grid(row=0, column=1, padx=0, pady=20, sticky="N")

        self.frame = tk.Frame(parent.main_win)
        self.frame.grid(row=0, column=0)

        self.frame2 = tk.Frame(parent.main_win, relief="ridge", borderwidth = 1)
        self.frame2.grid(row=0, column=1, pady=60, sticky="S" )

        # Titelbild & Icon
        # parent.main_win.iconbitmap(TITLE_ICO) # Für Windows
        #self.image = tk.PhotoImage(file="C:\Herbert\Hintergrund\Burg.png")
        #tk.Label(self.frame, image=self.image).pack()

        # Begrüßungstext
        #tk.Label(self.frame, text="...", font="Arial 20").grid()

        #TAP1 ###################################################################################
        # Denn Übung macht den Meister!
        # tk.Label(self.frame, text="Übung macht den Meister!",
        # font="Arial 10").grid()
        self.Anzeige1 = tk.Label(self.tab1, text="...", width=8, font=('Arial', 8))
        self.Anzeige1.grid(row=0)

        # Button Stempeln Tap1

        self.F1_B_on = tk.Button(self.tab1, text="ON",
                           width=15, command= self.parent.send_data_on_f1) #command=self.parent.do)
        self.F1_B_off = tk.Button(self.tab1, text="OFF",
                                    width=15, command= self.parent.send_data_off_f1)  # command=self.parent.do)
        
        self.F1_B_on.grid(row=1)
        self.F1_B_off.grid(row=2)
       

class Application(object):
    def __init__(self, main_win, title):
        self.main_win = main_win
        main_win.title(title)

        # Schliessung des Hauptfensters übder das 'x'-Symbol in der Titelleiste
        main_win.protocol("WM_DELETE_WINDOW", self.close_app)
        # Erstelle die Geometriedaten für ein zentriertes Hauptfenster
        geometry = self.center_win(main_win, MAIN_WIN_WIDTH, MAIN_WIN_HEIGHT)
        # Zentrier das Hauptfenster
        #self.main_win.geometry("{}x{}+{}+{}".format(*geometry))
        self.main_win.geometry("220x450")
        # Erstelle den Inhalt des Hauptfensters
        self.main_window_frame = MainWindowFrame(self) # ertselle Objekt
        # Variablen für Zeichnen

        # Create a TCP/IP socket
        self.sock = socket.create_connection((ip, 10000))  # 'espressif' oder 'localhost'

    def center_win(self, window, width, height):
        xpos = int((window.winfo_screenwidth() - width) / 2)
        ypos = int((window.winfo_screenheight() - height) / 2)
        return width, height, xpos, ypos

    def close_app(self):
        # Here do something before apps shutdown
        print("Good Bye! ")
        print('closing socket')
        self.sock.close()
        self.main_win.withdraw()
        self.main_win.destroy()

    def send_data_on_f1(self):
        try:
            # Send data
            global var
            var['Q1'] = 'on'
            str_json = json.dumps(var)
            #message = b'R1_on'
            message = bytes(str_json, 'utf-8')
            print('sending {!r}'.format(message))
            self.sock.sendall(message)
            # Anzeige was gestepelt wurde löschen
            self.main_window_frame.Anzeige1.config(text='on')
            amount_received = 0
            amount_expected = len(message)

        finally:
            print('socket open')
            #self.sock.close()


    def send_data_off_f1(self):
        try:
            # Send data
            #global var
            var['Q1'] = 'off'
            str_json = json.dumps(var)
            #message = b'R1_on'
            message = bytes(str_json, 'utf-8')
            print('sending {!r}'.format(message))
            self.sock.sendall(message)
            self.main_window_frame.Anzeige1.config(text='off')
            amount_received = 0
            amount_expected = len(message)

        finally:
            print('socket open')
            #sock.close()


def main():
    main_win = tk.Tk()
    app = Application(main_win, TITLE)
    main_win.mainloop()

main()
