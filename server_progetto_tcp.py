import threading
import socket
import mysql.connector
import facilities as fa

comunicazioni = ["", ""]
PASSWORD = "CIAO"       # PASSWORD PER ACCEDERE AL MENU DI SCELTA

# MAIN SERVER
def gestisci_comunicazione(conn):       # FUNZIONE PER FARE INTERAGIRE L'UTENTE CON IL MENU DI SCELTA
    conn.send("Benvenuto, inserisci password: ".encode())
    data = conn.recv(1024).decode()
    i = 0

    while data != PASSWORD and i < 2:   #L'UTENTE PUO SBAGLIARE SOLO 2 VOLTE LA PASSWORD
    
        i += 1
        conn.send(f"Password ERRATA, reinserisci password: tentativi rimasti {2 - i} ".encode())
        data = conn.recv(1024).decode()

    if (data != PASSWORD):  # QUI LA PASSWORD INSERITA è SBAGLIATA
        conn.send(f"Password ERRATA troppe volte, arrivederci".encode())
        conn.close()
        return

    while True:     # CHIEDO LA SCELTA DESIDERATA DALL'UTENTE
        conn.send("Benvenuto, inserisci l'operazione CRUD che vuoi fare: I=insert, U=update,R=read,D=delete".encode())
        data = conn.recv(1024).decode()
        print("L'operazione voluta dal client è stata :", data)


        if (data == "R"):   # QUI è IL CASO DELLA LETTURA DAL DATABASE
            conn.send("su che tabella vuoi leggere: dipendenti_david_savin, zone_di_lavoro_david_savin".encode()) 
            tabella = conn.recv(1024).decode()
            read(conn, tabella)     # CHIAMO LA FUNZIONE PER LEGGERE I DATI DAL DATABASE




        elif (data == "D"): # QUI è IL CASO DELLA CANCELLAZIONE DEI DATI
            conn.send("su che tabella vuoi eliminare: dipendenti_david_savin, zone_di_lavoro_david_savin".encode())
            tabella = conn.recv(1024).decode()
        
            if tabella == "dipendenti_david_savin":
                conn.send("Inserisci l'ID del dipendente da eliminare: ".encode())
                id = conn.recv(1024).decode()
                db_delete(conn, tabella, id)    # RICHIAMO LA FUNZIONE PER ELIMINARE UN DIPENDENTE
            
            if tabella == "zone_di_lavoro_david_savin":
                conn.send("Inserisci l'ID della zona da eliminare: ".encode())
                id = conn.recv(1024).decode()
                db_delete(conn, tabella, id)






        elif (data == "U"): # QUI è IL CASO DI AGGIORNAMENTO DEI DATI DELLA MIA TABELLA
            conn.send("su che tabella vuoi  modificare: dipendenti_david_savin, zone_di_lavoro_david_savin".encode())
            tabella = conn.recv(1024).decode()
            if tabella == "dipendenti_david_savin":
                conn.send("Inserisci il valore del campo che desideri modificare della tabella dipendenti_david_savin (nome, indirizzo, telefono, agente, ruolo, stipendio): ".encode())
                campo = conn.recv(1024).decode()
                conn.send("Inserisci l'ID del dipendente: ".encode())   # AGGIORNAMENTO TRAMITE L'ID
                id_dipendente = conn.recv(1024).decode()
                conn.send("Inserisci il nuovo valore da assegnare al campo: ".encode())
                nuovo_valore_campo = conn.recv(1024).decode()
                db_update(conn, tabella, campo, id_dipendente, 0, nuovo_valore_campo)  #RICHIAMO FUNZIONE DI AGGIORNAMENTO DEI DATI
                
            elif tabella == "zone_di_lavoro_david_savin":   
                conn.send("Inserisci il valore del campo che desideri modificare della tabella zone_di_lavoro_savin_david (nome_zona, numero_clienti, id_dipendente, numero_pc): ".encode())
                campo = conn.recv(1024).decode()
                conn.send("Inserisci l'ID della zona: ".encode())   # AGGIORNAMENTO TRAMITE L'ID
                id_zona = conn.recv(1024).decode()
                conn.send("Inserisci il nuovo valore da assegnare al campo: ".encode())
                nuovo_valore_campo = conn.recv(1024).decode()
                db_update(conn, tabella, campo, 0, id_zona, nuovo_valore_campo)  #RICHIAMO FUNZIONE DI AGGIORNAMENTO DEI DATI





        elif (data == "I"):     # FUNZIONE PER INSERIMENTO DATI ALL'INTERNO DI UNA TABELLA 
            conn.send("su che tabella vuoi inserire: dipendenti_david_savin, zone_di_lavoro_david_savin".encode())
            tabella = conn.recv(1024).decode()
            if tabella == "dipendenti_david_savin":
                conn.send("Inserisci il nome: ".encode())
                nome = conn.recv(1024).decode()
                conn.send("Inserisci la via: ".encode())
                Via = conn.recv(1024).decode()
                conn.send("Inserisci il telefono: ".encode())
                telefono = conn.recv(1024).decode()
                conn.send("Inserisci l'agente : ".encode())
                agente = conn.recv(1024).decode()
                conn.send("Inserisci ruolo: ".encode())
                ruolo = conn.recv(1024).decode()
                conn.send("Inserisci lo stipendio: ".encode())
                stipendio = conn.recv(1024).decode() 
                db_create(conn, tabella, nome, Via, telefono, agente, ruolo, stipendio, 0, 0, 0, 0)    # RICHIAMO FUNZIONE DI CREAZIONE TABELLA

            elif tabella == "zone_di_lavoro_david_savin":
                conn.send("Inserisci il nome_zona: ".encode())
                nome_zona = conn.recv(1024).decode()
                conn.send("Inserisci numero clienti : ".encode())
                numero_clienti = conn.recv(1024).decode()
                conn.send("Inserisci ID_dipendente: ".encode())
                id_dipendente = conn.recv(1024).decode()
                conn.send("Inserisci il numero del pc: ".encode())
                numero_pc = conn.recv(1024).decode() 
                db_create(conn, tabella,0,0,0,0,0,0, nome_zona, numero_clienti, id_dipendente, numero_pc)    # RICHIAMO FUNZIONE DI CREAZIONE TABELLA
                 
                              
#****************************************************************************************************************************************************************************************************************            
#   READ            
# APPOSTO
def read(connessione, tabella):
    """
    SCUOLA
       conn = mysql.connector.connect(
        host="10.10.0.10",
        user="david_savin",
        password="savin1234",
        database="5ATepsit",
        port=3306,
    )
    
    """
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        #password="savin1234",
        database="5atepsit",
        port=3306,
    )
    
    cur = conn.cursor()         # CUR MI SERVE PER POTER ESEGUIRE LA MIA QUERY
    query = f"SELECT * FROM {tabella}"
    print(query)
    cur.execute(query)
    dati = cur.fetchall()
    print(dati)
    print(type(dati))
    connessione.send("lista".encode())

    dati_da_inviare = fa.list_to_bytes(dati)
    connessione.send(dati_da_inviare)

    
#********************************************************************************************************************************************************************************


def db_update(connessione, tabella, campo, id_dipendente, id_zona, nuovo_valore_campo):
    """
      conn = mysql.connector.connect(
        host="10.10.0.10",
        user="david_savin",
        password="savin1234",
        database="5ATepsit",
        port=3306,
    )
    
    """
  
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        #password="savin1234",
        database="5atepsit",
        port=3306,
    )
    
    cur = conn.cursor()     # CUR SERVE PER ESEGUIRE LE QUERY
    valori = []
    if tabella == "dipendenti_david_savin":
        query = f"UPDATE {tabella} SET {campo} = %s WHERE id = %s"# invece che passare i valori nella stringa della query, li passo con una tupla (lista), è il databse che sostituisce %s nella query con i valori passati nella tupla.
        if campo=="agente":
            valori.append(int(nuovo_valore_campo))
        else:
            valori.append(nuovo_valore_campo)
        valori.append(int(id_dipendente))
        print(query)
          
        
    elif tabella == "zone_di_lavoro_david_savin":
        query = f"UPDATE {tabella} SET {campo} = %s WHERE id_zona = %s"
        if campo == "numero_pc":
            valori.append(int(nuovo_valore_campo)) 
            
        else:
            valori.append(nuovo_valore_campo) 
        valori.append(int(id_zona))
        print(query)
    print(valori)
    cur.execute(query, tuple(valori))   # esecuzione query
    conn.commit()
    cur.close()
    #conn.close()

#***********************************************************************************************************************************************************************


#   Verrà sbiancato anche l’id di quel dipendente
def db_delete(connessione, tabella, id):
    """
     conn = mysql.connector.connect(
        host="10.10.0.10",
        user="david_savin",
        password="savin1234",
        database="5ATepsit",
        port=3306,
    )
    """
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        #password="savin1234",
        database="5atepsit",
        port=3306,
    )
    
    cur = conn.cursor()
    
    if tabella == "dipendenti_david_savin":
       query = f"DELETE FROM {tabella} WHERE id = {id}" 
       cur.execute(query)
        
    elif tabella == "zone_di_lavoro_david_savin":
        query = f"DELETE FROM {tabella} WHERE id_zona = {id}"
        cur.execute(query)

    print(query)
    conn.commit()
    
    


#****************************************************************************************************************************************************************************
# CREATE
# APPOSTO
def db_create(connessione, tabella, nome, Via, telefono, agente, ruolo, stipendio, nome_zone, numero_clienti, id_dipendente, numero_pc):
    """
       conn = mysql.connector.connect(
        host="10.10.0.10",
        user="david_savin",
        password="savin1234",
        database="5ATepsit",
        port=3306,
    )
    """
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        #password="savin1234",
        database="5atepsit",
        port=3306,
    )
    
    
    query = ""
    cur = conn.cursor()
    if tabella == "dipendenti_david_savin":
        query = f"INSERT into {tabella} (nome, indirizzo, telefono, agente, ruolo, stipendio) VALUES ('{nome}', '{Via}', '{telefono}', {agente}, '{ruolo}', {stipendio})"
    elif tabella == "zone_di_lavoro_david_savin":
        query = f"INSERT into {tabella} (nome_zona, numero_clienti, id_dipendente, numero_pc) VALUES ('{nome_zone}', '{numero_clienti}', '{id_dipendente}', {numero_pc})"
    cur.execute(query)
    conn.commit()



if __name__ == '__main__':


    print("server in ascolto: ")
    lock = threading.Lock()
    HOST = ''
    PORT = 50011
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(10)
    thread = []
    lista_connessioni = []
    i = 0


    while True:
        lista_connessioni.append(s.accept())
        print('Connected by', lista_connessioni[i][1])
        thread.append(threading.Thread(target=gestisci_comunicazione, args=(lista_connessioni[i][0],)))
        thread[i].start()
        i += 1