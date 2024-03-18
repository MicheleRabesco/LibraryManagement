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
    print("Errore durante l'inserimento del libro:", e)


@app.route('/inserisci_libro', methods=['POST'])
def inserisci_libro():
    query_inserisci_libro = "INSERT INTO libro (titolo) VALUES (?)"
    query_scrittura = "INSERT INTO scrittura (codice_libro, codice_autore) VALUES (?, ?)"

    try:
        # Get JSON data from request
        data = request.get_json()
        titolo = data.get('titolo')
        codice_autore = data.get('codice_autore')

        # Insert data into PostgreSQL
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
    app.run(debug=True)


if __name__ == '__main__':
    main()
