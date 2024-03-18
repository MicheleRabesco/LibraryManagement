import jaydebeapi

from flask import Flask, request

app = Flask(__name__)

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


@app.route('/inserisci_libro', methods=['POST'])
def inserisci_libro():
    query_inserisci_libro = ("INSERT INTO libro (titolo) "
                             "VALUES (?)")
    query_scrittura = "INSERT INTO scrittura (codice_libro, codice_autore) VALUES (?, ?)"

    try:
        data = request.json
        if isinstance(data, list):
            data = data[0]
        titolo = data.get('titolo')
        codice_autore = data.get('codice_autore')
        cursor.execute(query_inserisci_libro, (titolo,))
        conn.commit()

        cursor.execute("SELECT codice_libro FROM libro WHERE titolo = ?", (titolo,))
        codice_libro = cursor.fetchone()[0]

        cursor.execute(query_scrittura, (codice_libro, codice_autore))
        conn.commit()
        return "Libro inserito correttamente", 200
    except Exception as e:
        return f"Errore durante l'inserimento del libro: {e}", 500


def main():
    inserisci_libro()


if __name__ == '__main__':
    app.run(debug=True)
