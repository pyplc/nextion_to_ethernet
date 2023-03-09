from usocket import socket
from machine import Pin, SPI
from nextion import nextion
import network
import time
import ujson

#Nextion Object
display = nextion(0, 1, 9600)

#W5x00 chip init
def w5x00_init():
    spi=SPI(0,2_000_000, mosi=Pin(19),miso=Pin(16),sck=Pin(18))
    nic = network.WIZNET5K(spi,Pin(17),Pin(20)) #spi,cs,reset pin
    nic.active(True)
    
    #None DHCP
    nic.ifconfig(('10.0.0.102','255.255.255.0','10.0.0.138','0.0.0.0'))
    
    #DHCP
    #nic.ifconfig('dhcp')
    
    print('IP address :', nic.ifconfig())
    while not nic.isconnected():
        time.sleep(1)
        print(nic.regs())
    
def server_loop(): 
    s = socket()
    s.bind(('0.0.0.0', 10000)) #Source IP Address from PC or 0.0.0.0 means all adress acept incomming
    s.listen(100)#bytes for buffer
    
    print("TEST server")
    while True:
        conn, addr = s.accept() # programm bleibt stehen bis etwas empfangen wird
        print('conn', conn)
        print("Connect to:", conn, "address:", addr) 
        print("Loopback server Open!")
        while True:
            try:
                data = conn.recv(2048)
                #led.value(1)
            except:
                conn.close()
                print('Close Connection')
                #led.value(0)
                break         
            print(data.decode('utf-8'))
            
            # Nextion Display
            fromDisplay = display.read()
            print('from Nextion: ', fromDisplay)
            
            #text in Display schreiben
            #text = str(data.decode('utf-8'))
            var = ujson.loads(data.decode('utf-8'))
            display.write_text('t0.txt', var['Q1'])
            
            #if data != 'NULL':
                #conn.send(data)
            try:
                conn.send(data)
            except:
                conn.close()
                print('Abort Connection')
                #led.value(0)
                break

def client_loop():
    s = socket()
    s.connect(('10.0.0.8', 5000)) #Destination IP Address
    
    print("Loopback client Connect!")
    while True:
        data = s.recv(2048)
        print(data.decode('utf-8'))
        if data != 'NULL' :
            s.send(data)
        
def main():
    w5x00_init()
    
###TCP SERVER###
    server_loop()

###TCP CLIENT###
    #client_loop()

if __name__ == "__main__":
    main()
