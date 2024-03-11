import jaydebeapi, re, traceback
from datetime import datetime, date

try:

    conn = jaydebeapi.connect(
        "org.postgresql.Driver",
        "jdbc:postgresql://localhost:5432/LibraryManagement",
        {"user": "postgres", "password": "postgres"},
        "C:/Program Files/PostgreSQL/16/postgresql-42.7.2.jar",
    )
    conn.jconn.setAutoCommit(False)
    cursor = conn.cursor()
    print("Connessione effettuata")
except Exception as e:
    print("Errore durante la connessione al database:", e)


class Libro:
    def __init__(self, codice_libro, titolo, numero_copie):
        self.codice_libro = codice_libro
        self.titolo = titolo
        self.numero_copie = numero_copie


class Autore:
    def __init__(self, codice_autore, nome, cognome,
                 data_nascita, data_morte):
        self.codice_autore = codice_autore
        self.nome = nome
        self.cognome = cognome
        self.data_nascita = data_nascita
        self.data_morte = data_morte


class Copia:
    def __init__(self, codice_catalogazione, stato, isbn, codice_libro):
        self.codice_catalogazione = codice_catalogazione
        self.stato = stato
        self.isbn = isbn
        self.codice_libro = codice_libro


class Utente:
    def __init__(self, codice_utente, nome=None, cognome=None,
                 data_nascita=None, data_iscrizione=None):
        self.codice_utente = codice_utente
        self.nome = nome
        self.cognome = cognome
        self.data_nascita = data_nascita
        self.data_iscrizione = data_iscrizione


class Prestito:
    def __init__(self, codice_prestito, codice_utente, codice_catalogazione,
                 data_prestito, data_restituzione=None, durata_prestito=None):
        self.codice_utente = codice_utente
        self.codice_catalogazione = codice_catalogazione
        self.data_prestito = data_prestito
        self.data_restituzione = data_restituzione
        self.durata_prestito = durata_prestito
        self.codice_prestito = codice_prestito


class Genere:
    def __init__(self, codice_genere, nome_genere):
        self.codice_genere = codice_genere
        self.nome_genere = nome_genere


class Appartenenza:
    def __init__(self, codice_genere=None, codice_autore=None):
        self.codice_genere = codice_genere
        self.codice_autore = codice_autore


class Scrittura:
    def __init__(self, codice_autore, codice_libro):
        self.codice_autore = codice_autore
        self.codice_libro = codice_libro


class Edizione:
    def __init__(self, isbn=None, anno_stampa=None, edizione=None):
        self.isbn = isbn
        self.anno_stampa = anno_stampa
        self.edizione = edizione


def inserisci_autore():
    try:
        query_inserisci_autore = ("INSERT INTO autore (nome, cognome, data_nascita, data_morte)"
                                  "VALUES (?, ?, ?, ?)")
        print("Inserisci i dati dell'autore: le date devono essere in formato dd/mm/yyyy\n")
        nome_autore = input("Nome: ")
        cognome_autore = input("Cognome: ")
        data_nascita_autore = input("Data di nascita: ")
        data_morte_autore = input("Data di morte: ")
        cursor.execute(query_inserisci_autore, (
            nome_autore.strip(), cognome_autore.strip(), data_nascita_autore.strip(),
            data_morte_autore.strip()))
        conn.commit()
        print("Valore Inserito")
    except (Exception, jaydebeapi.Error) as error:
        print("Errore durante l'inserimento del record:", error)

    ricerca_codice_query = "SELECT codice_autore FROM autore"
    codice_autore = cursor.execute(ricerca_codice_query)
    return codice_autore


def inserisci_libro():
    try:
        query_inserisci_libro = ("INSERT INTO libro (titolo, numero_copie) "
                                 "VALUES (?, ?) RETURNING codice_libro")
        print("Inserisci i dati del libro: titolo, numero di copie\n")
        titolo = input("Titolo: ")
        numero_copie = input("Numero di copie: ")
        cursor.execute(query_inserisci_libro, (
            titolo.strip(), int(numero_copie.strip())))
        codice_libro = cursor.fetchone()[0]

        query_associa_libro_autore = "INSERT INTO scrittura (codice_autore, codice_libro) VALUES (?, ?)"
        query_mostra_autori = "SELECT * FROM autore ORDER BY codice_autore ASC"
        cursor.execute(query_mostra_autori)
        print("Associa ora il libro all'autore.\n")
        print("Ecco la lista degli autori inseriti:")
        lista_autori = cursor.fetchone()
        while lista_autori is not None:
            print(lista_autori)
            lista_autori = cursor.fetchone()

        codice_autore = input(
            "L'autore è presente nella lista? Se sì scrivi il codice a lui associato\naltrimenti scrivi 0 per "
            "inserire un nuovo autore\n")
        query_codice_autore = "SELECT * FROM autore"
        cursor.execute(query_codice_autore)
        codice_autore = int(codice_autore)
        if codice_autore != 0:
            cursor.execute(query_associa_libro_autore, (codice_autore, codice_libro,))
        else:
            print("Autore non esistente.\n")
            inserisci_autore()
            cursor.execute("SELECT LASTVAL()")
            codice_autore = cursor.fetchone()[0]
            cursor.execute(query_associa_libro_autore, (codice_autore, codice_libro))

        conn.commit()
        print("Libro inserito, autore associato, tabella scrittura aggiornata")
    except (Exception, jaydebeapi.Error) as error:
        print("Errore durante l'inserimento del record:", error)
    return codice_libro


def inserisci_copia():
    try:
        query_codice_libro = "SELECT codice_libro FROM libro WHERE titolo = ?"
        titolo_libro = input("Inserisci il titolo del libro di cui vuoi aggiungere una copia:\n")
        cursor.execute(query_codice_libro, (titolo_libro,))
        codice_libro = cursor.fetchone()[0]

        # ogni copia è differente
        query_inserisci_copia = ("INSERT INTO copia (stato, isbn, codice_libro) "
                                 "VALUES (?, ?, ?)")
        print("Inserisci i dati della copia\n")
        stato = input("Stato: ")
        isbn = input("ISBN: ")
        cursor.execute(query_inserisci_copia, (stato.strip(), isbn.strip(), codice_libro))
        query_aggiornamento_copie = "UPDATE libro SET numero_copie = numero_copie +1 WHERE codice_libro = ?"
        cursor.execute(query_aggiornamento_copie, (codice_libro,))
        conn.commit()
        print("Valore Inserito")
    except (Exception, jaydebeapi.Error) as error:
        print("Errore durante l'inserimento del record:", error)


def inserisci_utente():
    try:
        query_inserisci_utente = ("INSERT INTO utente (nome, cognome, data_nascita, data_iscrizione) VALUES (?, ?, ?, "
                                  "?)")
        print("Inserisci i dati anagrafici dell'utente\n")
        nome = input("Nome:\n")
        cognome = input("Cognome:\n")
        data_nascita = input("Data di nascita nel formato dd-mm-yyyy:\n")
        data_iscrizione = input("Data di iscrizione nel formato dd-mm-yyyy:\n")

        cursor.execute(query_inserisci_utente, (nome, cognome, data_nascita, data_iscrizione))
        conn.commit()
        print("Utente registrato")

    except (Exception, jaydebeapi.Error) as error:
        print("Errore durante l'inserimento del record:", error)


def inserisci_prestito():
    try:
        val = None
        query_inserimento_prestito = ("INSERT INTO prestito (codice_utente, codice_catalogazione, data_prestito, "
                                      "data_restituzione, durata_prestito) VALUES (?, ?, ?, NULL, NULL)")

        # viene chiesto il codice dell'utente

        codice_utente = input("Inserisci il codice dell'utente che deve noleggiare una copia:\n")
        codice_utente = int(codice_utente)
        query_codice_utente = "SELECT codice_utente FROM utente WHERE codice_utente = ?"
        cursor.execute(query_codice_utente, (codice_utente,))
        res = cursor.fetchone()
        if res is None:
            print("Utente non trovato.")
            return

        # viene chiesto il codice di catalogazione della copia

        codice_catalogazione = input("Inserisci il codice di catalogazione della copia di riferimento:\n")
        codice_catalogazione = int(codice_catalogazione)
        query_codice_copia = "SELECT codice_catalogazione FROM copia WHERE codice_catalogazione = ?"
        cursor.execute(query_codice_copia, (codice_catalogazione,))
        res = cursor.fetchone()
        if res is None:
            print("Copia non trovata.")
            return

        # viene chiesta la data di inizio del prestito

        data_prestito = input("Inserisci la data dell'inizio del prestito nel formato dd-mm-yyyy:\n")

        cursor.execute(query_inserimento_prestito, (codice_utente, codice_catalogazione, data_prestito,))

        print("Prestito creato.")

        update_stato_copia(int(codice_catalogazione))
        conn.commit()
        print("Prestito inserito.")
    except (Exception, jaydebeapi.Error) as error:
        print("Errore durante l'inserimento del record:", error)


def update_stato_copia(codice_catalogazione):
    try:
        # Seleziona la data di inizio e di restituzione del prestito per la copia specificata
        query_prestito = "SELECT data_prestito, data_restituzione FROM prestito WHERE codice_catalogazione = ?"
        cursor.execute(query_prestito, (codice_catalogazione,))
        prestito = cursor.fetchone()

        if prestito:
            data_inizio, data_restituzione = prestito

            # Calcola la durata del prestito
            if data_inizio and data_restituzione:
                data_inizio = datetime.strptime(data_inizio, "%d-%m-%Y").date()
                data_restituzione = datetime.strptime(data_restituzione, "%d-%m-%Y").date()
                durata_prestito = (data_restituzione - data_inizio).days

                # Aggiorna lo stato della copia in base alla presenza della data di restituzione
                if data_restituzione:
                    query_stato_disponibile = "UPDATE copia SET stato = 'Disponibile' WHERE codice_catalogazione = ?"
                    cursor.execute(query_stato_disponibile, (codice_catalogazione,))
                else:
                    query_stato_non_disponibile = "UPDATE copia SET stato = 'Non Disponibile' WHERE codice_catalogazione = ?"
                    cursor.execute(query_stato_non_disponibile, (codice_catalogazione,))

                # Aggiorna la durata del prestito nella tabella prestito
                query_update_durata_prestito = "UPDATE prestito SET durata_prestito = ? WHERE codice_catalogazione = ?"
                cursor.execute(query_update_durata_prestito, (durata_prestito, codice_catalogazione))

                conn.commit()
                print("Stato della copia aggiornato con successo.")
            else:
                # Se esiste un prestito valido (con data di inizio), imposta lo stato della copia a "Non Disponibile"
                query_stato_non_disponibile = "UPDATE copia SET stato = 'Non Disponibile' WHERE codice_catalogazione = ?"
                cursor.execute(query_stato_non_disponibile, (codice_catalogazione,))
                conn.commit()
                print("Stato della copia aggiornato con successo.")
        else:
            print("Nessun prestito trovato per la copia specificata.")
    except (Exception, jaydebeapi.Error) as error:
        print("Errore durante l'aggiornamento dello stato della copia:", error)



# def restituisci_copia(): necessario codice_prestito, si aggiunge data restituzione, si aggiorna stato della copia ( torna disponibile)
def restituisci_copia():
    try:
        codice_prestito = input("Inserisci il codice prestito da restituire")
        codice_prestito = int(codice_prestito)
        query_seleziona_prestito = "SELECT * FROM prestito WHERE codice_prestito = ?"
        cursor.execute(query_seleziona_prestito, (codice_prestito,))
        prestito = cursor.fetchone()

        if prestito:
            data_restituzione = datetime.now().strftime("%d-%m-%Y")
            query_aggiorna_data_restituzione = "UPDATE prestito SET data_restituzione = ? WHERE codice_prestito = ?"
            cursor.execute(query_aggiorna_data_restituzione, (data_restituzione, codice_prestito))
            codice_catalogazione = prestito[1]

            update_stato_copia(codice_catalogazione)
            print("Copia restituita con successo.")
            conn.commit()
        else:
            print("Il codice prestito specificato non esiste.")
    except (Exception, jaydebeapi.Error) as error:
        print("Errore durante l'operazione di restituzione della copia:", error)


def inserisci_genere():
    try:
        query_inserisci_genere = "INSERT INTO genere (nome_genere) VALUES (?)"
        nome_genere = input("Inserisci il nome del genere: ")
        cursor.execute(query_inserisci_genere, [nome_genere])
        conn.commit()
        print("Genere inserito")
    except (Exception, jaydebeapi.Error) as error:
        print("Errore durante l'inserimento del record:", error)


"""

def definisci_appartenenza_genere():
    try:



    except (Exception, jaydebeapi.Error) as error:
        print("Errore durante l'inserimento del record:", error)
"""


def main():
    while True:
        prompt = input("Che azione vuoi eseguire?\nDigita:\n1. per inserire un autore\n2. per inserire un libro\n3. "
                       "per inserire una copia\n4. per inserire un utente\n5. per inserire un prestito\n6. per "
                       "inserire un genere\n7. per restituire una copia\n"
                       "0 per uscire\n")

        if prompt == '1':
            inserisci_autore()
        elif prompt == '2':
            inserisci_libro()
        elif prompt == '3':
            inserisci_copia()
        elif prompt == '4':
            inserisci_utente()
        elif prompt == '5':
            inserisci_prestito()
        elif prompt == '6':
            inserisci_genere()
        elif prompt == '7':
            restituisci_copia()
        elif prompt == '0':
            exit(0)
        else:
            print("Non valido")


if __name__ == "__main__":
    main()
