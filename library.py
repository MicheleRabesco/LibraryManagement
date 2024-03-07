import jaydebeapi

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
                 data_nascita, data_morte=None):
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
    def __init__(self, codice_libro=None, codice_autore=None):
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
        numero_copie = input(int("Numero di copie: "))  #il numero di copie inserito qui non risulta nella tabella copie
        cursor.execute(query_inserisci_libro, (         #controllare ora che la foreign key è stata aggiunta
            titolo.strip(), int(numero_copie.strip())))
        codice_libro = cursor.fetchone()[0]

        print("Associa ora il libro all'autore.\n Inserisci il nome e il cognome, uno alla volta.\n")
        nome = input("Nome: ")
        cognome = input("Cognome: ")

        query_codice_autore = ("SELECT codice_autore FROM autore WHERE nome = ? AND cognome = ?")
        cursor.execute(query_codice_autore, (nome.strip(), cognome.strip()))
        codice_autore = cursor.fetchone()[0]

        query_associa_libro_autore = ("INSERT INTO scrittura (codice_libro, codice_autore) VALUES (?, ?)")
        cursor.execute(query_associa_libro_autore, (codice_libro, codice_autore))
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
        cursor.execute(query_inserisci_copia, (
            stato.strip(), isbn.strip(), codice_libro))
        query_aggiornamento_copie = "UPDATE libro SET numero_copie = numero_copie +1 WHERE codice_libro = ?"
        cursor.execute(query_aggiornamento_copie, (codice_libro,))
        conn.commit()
        print("Valore Inserito")
    except (Exception, jaydebeapi.Error) as error:
        print("Errore durante l'inserimento del record:", error)


# codice_utente=None, codice_catalogazione=None,
#                  data_prestito=None, data_restituzione=None, durata_prestito=None

def inserisci_prestito():
    try:

        # SELECT dell'utente con nome e cognome, SELECT della copia con ISBN, calcolo durata prestito

        query_inserimento_prestito = ("INSERT INTO prestito (codice_utente, codice_catalogazione, data_prestito, "
                                      "data_restituzione, durata_prestito) VALUES (?, ?, ?, ?, ?)")
    except (Exception, jaydebeapi.Error) as error:
        print("Errore durante l'inserimento del record:", error)


def inserisci_genere():
    try:
        query_inserisci_genere = ("INSERT INTO genere (codice_genere, nome_genere) VALUES (?, ?)")
        nome_genere = input("Inserisci il nome del genere:")
        cursor.execute(query_inserisci_genere, (nome_genere))
        codice_genere = cursor.fetchone()[0] #se dovesse servire

    except (Exception, jaydebeapi.Error) as error:
        print("Errore durante l'inserimento del record:", error)


def definisci_appartenenza_genere():
    try:
        #i campi sono codice_genere e codice_autore, all'utente vengono chiesti nome del genere e dell'autore nome, cognome e in caso di duplicato anche


    except (Exception, jaydebeapi.Error) as error:
        print("Errore durante l'inserimento del record:", error)

def main():
    while True:
        prompt = input("Che azione vuoi eseguire?\nDigita 1 per inserire un autore, 2 un libro, 3 una copia, "
                       "0 per uscire\n")

        if prompt == '1':
            inserisci_autore()
        elif prompt == '2':
            inserisci_libro()
        elif prompt == '3':
            inserisci_copia()
        elif prompt == '0':
            exit(0)
        else:
            print("Non valido")


if __name__ == "__main__":
    main()
