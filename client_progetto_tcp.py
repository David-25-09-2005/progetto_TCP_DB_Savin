import socket
import facilities


HOST = 'localhost'    # Il nodo remoto, qui metti il tuo indirizzo IP per provare connessione server e client dalla tua macchina alla tua macchina
PORT = 50011     # La stessa porta usata dal server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    
    data = s.recv(1024)
    
    if data.decode()=="lista":
        dati = s.recv(1024)
        dati = facilities.bytes_to_list(dati)
        for elem in dati:
            print(elem)
        
    else:
        print('Received: ', data.decode())
        testo = input("\ninserisci: ").encode()
        s.send(testo)

s.close()
