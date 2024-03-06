class Libro:
    def __init__(self, codice_libro=None, titolo=None, n_copie=None):
        self.codice_libro = codice_libro
        self.titolo = titolo
        self.n_copie = n_copie


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
