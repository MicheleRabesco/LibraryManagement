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
    def __init__(self, codice_libro=None, titolo=None, numero_copie=None):
        self.codice_libro = codice_libro
        self.titolo = titolo
        self.numero_copie = numero_copie


class Autore:
    def __init__(self, codice_autore=None, nome=None, cognome=None,
                 data_nascita=None, data_morte=None):
        self.codice_autore = codice_autore
        self.nome = nome
        self.cognome = cognome
        self.data_nascita = data_nascita
        self.data_morte = data_morte


class Copia:
    def __init__(self, codice_catalogazione=None, stato=None, isbn=None, codice_libro=None):
        self.codice_catalogazione = codice_catalogazione
        self.stato = stato
        self.isbn = isbn
        self.codice_libro = codice_libro


class Utente:
    def __init__(self, matricola=None, nome=None, cognome=None,
                 data_nascita=None, data_iscrizione=None):
        self.matricola = matricola
        self.nome = nome
        self.cognome = cognome
        self.data_nascita = data_nascita
        self.data_iscrizione = data_iscrizione


class Prestito:
    def __init__(self, matricola=None, codice_catalogazione=None,
                 data_prestito=None, data_restituzione=None, durata_prestito=None):
        self.matricola = matricola
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


def insert_book():
    try:
        add_book_query = ("INSERT INTO libro(codice_libro, titolo, numero_copie)"
                          "VALUES (?,?,?)")
        values_to_add = ("06", "1984", 2)
        cursor.execute(add_book_query, values_to_add)
        conn.commit()
        print("Valore Inserito")
    except (Exception, jaydebeapi.Error) as error:
        print("Errore durante l'inserimento del record:", error)


insert_book()


def update_book():
    try:
        add_book_query = ("INSERT INTO libro(codice_libro, titolo, numero_copie)"
                          "VALUES (?,?,?)")
        values_to_add = ("06", "1984", 2)
        cursor.execute(add_book_query, values_to_add)
        conn.commit()
        print("Valore Inserito")
    except (Exception, jaydebeapi.Error) as error:
        print("Errore durante l'inserimento del record:", error)


update_book()
