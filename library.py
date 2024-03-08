import jaydebeapi, re
from datetime import datetime

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
    def __init__(self, codice_utente=None, nome=None, cognome=None,
                 data_nascita=None, data_iscrizione=None):
        self.codice_utente = codice_utente
        self.nome = nome
        self.cognome = cognome
        self.data_nascita = data_nascita
        self.data_iscrizione = data_iscrizione


class Prestito:
    def __init__(self, codice_utente=None, codice_catalogazione=None,
                 data_prestito=None, data_restituzione=None, durata_prestito=None):
        self.codice_utente = codice_utente
        self.codice_catalogazione = codice_catalogazione
        self.data_prestito = data_prestito
        self.data_restituzione = data_restituzione
        self.durata_prestito = durata_prestito


class Genere:
    def __init__(self, codice_genere=None, nome_genere=None):
        self.codice_genere = codice_genere
        self.nome_genere = nome_genere


class Appartenenza:
    def __init__(self, codice_genere=None, codice_autore=None):
        self.codice_genere = codice_genere
        self.codice_autore = codice_autore


class Scrittura:
    def __init__(self, codice_libro, codice_autore):
        self.codice_libro = codice_libro
        self.codice_autore = codice_autore


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

        query_associa_libro_autore = ("INSERT INTO scrittura (codice_libro, codice_autore) VALUES (?, ?)")
        print("Associa ora il libro all'autore.\n Inserisci il nome e il cognome, uno alla volta.\n")
        nome = input("Nome: ")
        cognome = input("Cognome: ")
        query_codice_autore = ("SELECT codice_autore FROM autore WHERE nome = ? AND cognome = ?")

        cursor.execute(query_codice_autore, (nome, cognome))
        codice_autore = cursor.fetchone()[0]

        cursor.execute(query_associa_libro_autore, (codice_libro, codice_autore,))
        conn.commit()
        print("Valore Inserito")
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
        data_nascita = input("Data di nascita nel formato dd/mm/yyyy:\n")
        data_iscrizione = input("Data di iscrizione nel formato dd/mm/yyyy:\n")

        cursor.execute(query_inserisci_utente, (nome, cognome, data_nascita, data_iscrizione))
        conn.commit()
        print("Utente registrato")



    except (Exception, jaydebeapi.Error) as error:
        print("Errore durante l'inserimento del record:", error)


def inserisci_prestito():
    try:

        # SELECT dell'utente con codice_utente, SELECT della copia con cod_cat

        query_inserimento_prestito = ("INSERT INTO prestito (codice_utente, codice_catalogazione, data_prestito, "
                                      ") VALUES (?, ?, ?)")
        codice_utente = input("Inserisci il codice dell'utente che deve noleggiare una copia:\n")
        codice_utente = int(codice_utente)
        query_codice_utente = ("SELECT codice_utente FROM utente WHERE codice_utente = ?")
        cursor.execute(query_codice_utente, (codice_utente,))
        cursor.fetchone()

        codice_catalogazione = input("Inserisci il codice di catalogazione della copia di riferimento:\n")
        codice_catalogazione = int(codice_catalogazione)
        query_codice_copia = ("SELECT isbn FROM copia WHERE codice_catalogazione = ?")
        cursor.execute(query_codice_copia, (codice_catalogazione,))
        cursor.fetchone()

        data_prestito = input("Inserisci la data dell'inizio del prestito nel formato dd-mm-yyyy:\n")

        # TO-DO
        #
        # lo stato della copia viene aggiornato
        query_data_restituzione = ("SELECT data_restituzione FROM prestito WHERE codice_catalogazione = ?")
        cursor.execute(query_data_restituzione, (codice_catalogazione,))
        data_restituzione = query_data_restituzione

        update_stato_copia(codice_catalogazione, data_restituzione)
        cursor.execute(query_inserimento_prestito, (codice_utente, codice_catalogazione, data_prestito,))
        conn.commit()
        print("Prestito creato")
    except (Exception, jaydebeapi.Error) as error:
        print("Errore durante l'inserimento del record:", error)


def update_stato_copia(codice_catalogazione, data_restituzione):
    try:
        query_stato_disponibile = ("UPDATE copia SET stato = Disponibile WHERE codice_catalogazione = ?")
        query_stato_non_disponibile = ("UPDATE copia SET stato = Non Disponibile WHERE codice_catalogazione = ?")
        query_update_durata_prestito = ("UPDATE copia SET durata_prestito = ? WHERE codice_catalogazione = ?")
        query_inizio_prestito = ("SELECT data_prestito FROM prestito WHERE codice_catalogazione = ? ")
        data_inizio = cursor.execute(query_inizio_prestito)

        # TO-DO
        # viene modificato lo stato di una copia in seguito all'inizio o la fine di un noleggio
        # questo metodo verrà poi chiamato nel metodo inserisci_prestito

        # calcolare la durata del prestito: estrapolare le date, sottrarle (py) e inserire il valore in durata (sql) in giorni

        regex_fine = re.search(r'\d{2}-\d{2}-\d{4}', data_restituzione)
        data_restituzione = datetime.strptime(regex_fine.group(), '%d-%m-%y').date()

        regex_inizio = re.search(r'\d{2}-\d{2}-\d{4}', data_inizio)
        data_inizio = datetime.strptime(regex_inizio.group(), '%d-%m-%y').date()

        durata_prestito = (data_restituzione - data_inizio).days

        if data_restituzione == '':
            cursor.execute(query_stato_non_disponibile, (codice_catalogazione, data_restituzione))
        elif data_restituzione:
            cursor.execute(query_stato_disponibile, (codice_catalogazione, data_restituzione))
            cursor.execute(query_update_durata_prestito, (durata_prestito, codice_catalogazione))


        conn.commit()
        print("Copia aggiornata")
    except (Exception, jaydebeapi.Error) as error:
        print("Errore durante l'inserimento del record:", error)


def inserisci_genere():
    try:
        query_inserisci_genere = ("INSERT INTO genere (codice_genere, nome_genere) VALUES (?, ?)")
        nome_genere = input("Inserisci il nome del genere:")
        cursor.execute(query_inserisci_genere, (nome_genere))
        codice_genere = cursor.fetchone()[0]  # se dovesse servire

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
                       "inserire un genere\n"
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
        elif prompt == '0':
            exit(0)
        else:
            print("Non valido")


if __name__ == "__main__":
    main()
