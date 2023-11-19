import threading
import socket
import mysql.connector
import facilities as fa




def db_set(data):
    conn = mysql.connector.connect(
        host="10.10.0.10",
        user="david_savin",
        password="savin1234",
        database="5ATepsit",
        port=3306,
    )
#modificare le anagrafiche dei dipendenti o delle zone


comunicazioni = ["", ""]
PASSWORD = "CIAO"



def gestisci_comunicazione(conn):
    conn.send("Benvenuto, inserisci password: ".encode())
    data = conn.recv(1024).decode()
    i = 0

    while data != PASSWORD and i < 2:
        i += 1
        conn.send(f"Password ERRATA, reinserisci password: tentativi rimasti {2 - i} ".encode())
        data = conn.recv(1024).decode()

    if (data != PASSWORD):
        conn.send(f"Password ERRATA troppe volte, arrivederci".encode())
        conn.close()
        return

    while True:

        conn.send("Benvenuto, cosa vuoi fare: I=insert, U=update,R=read,D=delete".encode())
        data = conn.recv(1024).decode()
        print("L'operazione voluta dal client è stata :", data)

        if (data == "R"):
            conn.send("su che tabella vuoi cercare: clienti_david_savin, zone_di_lavoro_david_savin".encode())
            tabella = conn.recv(1024).decode()
            read(conn, tabella)

        elif (data == "D"):
            conn.send("su che tabella vuoi eliminare: clienti_david_savin, zone_di_lavoro_david_savin".encode())
            dato = conn.recv(1024).decode()
            dati_query = db_delete(dato)
            print("dati_query :", dati_query)


        elif (data == "U"):
            conn.send("su che tabella vuoi eseguire modificare: clienti_david_savin, zone_di_lavoro_david_savin".encode())
            tabella = conn.recv(1024).decode()
            conn.send("Inserisci il valore del campo NUM_Clienti: ".encode())
            campo = conn.recv(1024).decode()
            conn.send("Inserisci l'ID del dipendente: ".encode())
            id_dipendente = conn.recv(1024).decode()
            dato = db_update(conn, tabella, campo, id_dipendente)

        #connessione, tabella, nome, Via, telefono, agente, ruolo, stipendi
        elif (data == "I"):
            conn.send("su che tabella vuoi inserire: clienti_david_savin, zone_di_lavoro_david_savin".encode())
            tabella = conn.recv(1024).decode()
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
            
            dato.db_create(conn, tabella, nome, Via, telefono, agente, ruolo, stipendio)
            



def db_get(parametri):
    conn = mysql.connector.connect(
        host="10.10.0.10",
        user="david_savin",
        password="savin1234",
        database="5ATepsit",
        port=3306,
        # voi qui mettete la porta 3306!! quella di default per mySQL, io ho dovuto mettere la 3307 perche la mia 3306 era gia occupata dal database SQL sul mio PC!
    )

    cur = conn.cursor()
    cur.execute(parametri)
    conn.commit()
    # si chiama una funzione di libreria passando i parametri di ricerca dell'utente. esempio controlla_caratteri(nome)
    clausole = ""
    # for key,value in parametri.items():
    #    clausole += f"and {key} = '{value}' "

    query = f"SELECT * FROM dipendenti_david_savin where 1=1 {clausole}"
    print(query)
    cur.execute(query)
    dati = cur.fetchall()
    print(dati)
    return dati




def read(connessione, tabella):
    conn = mysql.connector.connect(
        host="10.10.0.10",
        user="",
        password="",
        database="5ATepsit",
        port=3306,
    )
    
    cur = conn.cursor()
    
    # inserisci gestione filtri di ricerca
    #dati_query = fa.list_to_bytes(db_get(query))
    query = f"SELECT * FROM {tabella}"
    
    dati = cur.execute(query)

    dati_da_inviare = fa.string_to_bytes(dati)
    connessione.send(dati_da_inviare.encode())

    #dati_formattati = dati_query.fa.list_to_bytes(data)
    #print(dati_formattati.decode())




def db_update(connessione, tabella, campo, id_dipendente):
    """
    cconn = mysql.connector.connect(
        host="10.10.0.10",
        user="david_savin",
        password="savin1234",
        database="5ATepsit",
        port=3306,
    )"""
    
    conn = mysql.connector.connect(
        host="10.10.0.10",
        user="david_savin",
        password="savin1234",
        database="5ATepsit",
        port=3306,
    )
    query = f"UPDATE clienti_david_savin SET numero_clienti = \'{campo}\' WHERE id_dipendente = \'{id_dipendente}\'"
    print(query)
    cur = conn.cursor()
    # inserisci gestione filtri di ricerca
    dati = cur.execute(query)
    #dati_formattati = dati
    #connessione.send(dati_formattati.encode())


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#   Verrà sbiancato anche l’id di quel dipendente
def db_delete(data):
    conn = mysql.connector.connect(
        host="10.0.0.10",
        user="david_savin",
        password="savin",
        database="5atepsit",
        port=3306,
        # voi qui mettete la porta 3306!! quella di default per mySQL, io ho dovuto mettere la 3307 perche la mia 3306 era gia occupata dal database SQL sul mio PC!
    )

    cur = conn.cursor()

    # si chiama una funzione di libreria passando i parametri di ricerca dell'utente. esempio controlla_caratteri(nome)
    query = f"DELETE FROM clienti_david_savin where id= '{data}' "
    cur.execute(query)
    conn.commit()

    return "eliminato"

# tramite l’ID
def db_create(connessione, tabella, nome, Via, telefono, agente, ruolo, stipendio):
    conn = mysql.connector.connect(
        host="10.0.0.10",
        user="david_savin",
        password="savin",
        database="5atepsit",
        port=3306,
        # voi qui mettete la porta 3306!! quella di default per mySQL, io ho dovuto mettere la 3307 perche la mia 3306 era gia occupata dal database SQL sul mio PC!
    )
    cur = conn.cursor()
    query = f"INSERT into tabella VALUES (2500, '{nome}', '{Via}', '{telefono}', '{agente}', '{ruolo}', {stipendio})"
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
