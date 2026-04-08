import sqlite3
from datetime import date, datetime

DB_NAME = "Sadjak_Denise_fitnessstudio.db"

def create_tables(conn):
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS Trainer (
            TrainerID   INTEGER PRIMARY KEY AUTOINCREMENT,
            Vorname     VARCHAR(50)  NOT NULL,
            Nachname    VARCHAR(50)  NOT NULL,
            Spezialgebiet VARCHAR(100)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS Kurs (
            KursID          INTEGER PRIMARY KEY AUTOINCREMENT,
            Bezeichnung     VARCHAR(100) NOT NULL,
            Wochentag       VARCHAR(15)  NOT NULL,
            Uhrzeit         TIME         NOT NULL,
            MaxTeilnehmer   INT          NOT NULL,
            TrainerID       INT          NOT NULL,
            FOREIGN KEY (TrainerID) REFERENCES Trainer(TrainerID)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS Mitglied (
            MitgliedID      INTEGER PRIMARY KEY AUTOINCREMENT,
            Vorname         VARCHAR(50)  NOT NULL,
            Nachname        VARCHAR(50)  NOT NULL,
            Email           VARCHAR(100) NOT NULL UNIQUE,
            Beitrittsdatum  DATE         NOT NULL
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS Anmeldung (
            MitgliedID      INT      NOT NULL,
            KursID          INT      NOT NULL,
            Anmeldedatum    DATETIME NOT NULL,
            PRIMARY KEY (MitgliedID, KursID),
            FOREIGN KEY (MitgliedID) REFERENCES Mitglied(MitgliedID),
            FOREIGN KEY (KursID)     REFERENCES Kurs(KursID)
        )
    """)

    conn.commit()
    print("Tabellen erfolgreich erstellt.")


def insert_data(conn):
    c = conn.cursor()

    # --- Trainer (mind. 3) ---
    trainer = [
        ("Anna",  "Berger",  "Yoga & Meditation"),
        ("Lukas", "Huber",   "Spinning & Ausdauer"),
        ("Maria", "Schneider","Zumba & Tanz"),
        ("Felix", "Wagner",  "Pilates & Reha"),
    ]
    c.executemany(
        "INSERT INTO Trainer (Vorname, Nachname, Spezialgebiet) VALUES (?, ?, ?)",
        trainer
    )

    # --- Kurse (mind. 5) ---
    kurse = [
        ("Yoga Basics",     "Montag",     "08:00", 15, 1),
        ("Spinning",        "Dienstag",   "17:30", 20, 2),
        ("Zumba Fun",       "Mittwoch",   "19:00", 25, 3),
        ("Pilates",         "Donnerstag", "10:00", 12, 4),
        ("Yoga Fortgeschrittene", "Freitag", "09:00", 10, 1),
        ("Spinning Intensiv",    "Samstag", "08:30", 18, 2),
    ]
    c.executemany(
        "INSERT INTO Kurs (Bezeichnung, Wochentag, Uhrzeit, MaxTeilnehmer, TrainerID) VALUES (?, ?, ?, ?, ?)",
        kurse
    )

    # --- Mitglieder (mind. 6) ---
    mitglieder = [
        ("Sophie",  "Müller",  "sophie.mueller@mail.at",  "2023-01-15"),
        ("Thomas",  "Bauer",   "thomas.bauer@mail.at",    "2023-03-22"),
        ("Laura",   "Klein",   "laura.klein@mail.at",     "2023-05-10"),
        ("Stefan",  "Wolf",    "stefan.wolf@mail.at",     "2024-01-05"),
        ("Julia",   "Fuchs",   "julia.fuchs@mail.at",     "2024-02-28"),
        ("Markus",  "Braun",   "markus.braun@mail.at",    "2024-06-01"),
        ("Nina",    "Schwarz", "nina.schwarz@mail.at",    "2024-09-12"),
    ]
    c.executemany(
        "INSERT INTO Mitglied (Vorname, Nachname, Email, Beitrittsdatum) VALUES (?, ?, ?, ?)",
        mitglieder
    )

    # --- Anmeldungen (mind. 8) ---
    anmeldungen = [
        (1, 1, "2024-11-01 10:00:00"),
        (1, 3, "2024-11-02 11:30:00"),
        (2, 2, "2024-11-03 09:15:00"),
        (3, 1, "2024-11-04 14:00:00"),
        (3, 4, "2024-11-04 14:05:00"),
        (4, 2, "2024-11-05 08:00:00"),
        (4, 6, "2024-11-05 08:10:00"),
        (5, 3, "2024-11-06 16:45:00"),
        (6, 5, "2024-11-07 10:20:00"),
        (7, 1, "2024-11-08 09:00:00"),
        (7, 4, "2024-11-08 09:05:00"),
    ]
    c.executemany(
        "INSERT INTO Anmeldung (MitgliedID, KursID, Anmeldedatum) VALUES (?, ?, ?)",
        anmeldungen
    )

    conn.commit()
    print("Beispieldaten erfolgreich eingefügt.")


def show_data(conn):
    c = conn.cursor()

    print("\n--- Trainer ---")
    for row in c.execute("SELECT * FROM Trainer"):
        print(row)

    print("\n--- Kurse (mit Trainername) ---")
    for row in c.execute("""
        SELECT k.KursID, k.Bezeichnung, k.Wochentag, k.Uhrzeit, k.MaxTeilnehmer,
               t.Vorname || ' ' || t.Nachname AS Trainer
        FROM Kurs k
        JOIN Trainer t ON k.TrainerID = t.TrainerID
    """):
        print(row)

    print("\n--- Mitglieder ---")
    for row in c.execute("SELECT * FROM Mitglied"):
        print(row)

    print("\n--- Anmeldungen ---")
    for row in c.execute("""
        SELECT m.Vorname || ' ' || m.Nachname AS Mitglied,
               k.Bezeichnung AS Kurs,
               a.Anmeldedatum
        FROM Anmeldung a
        JOIN Mitglied m ON a.MitgliedID = m.MitgliedID
        JOIN Kurs     k ON a.KursID     = k.KursID
        ORDER BY a.Anmeldedatum
    """):
        print(row)


def main():
    conn = sqlite3.connect(DB_NAME)
    create_tables(conn)
    insert_data(conn)
    show_data(conn)
    conn.close()
    print(f"\nDatenbank '{DB_NAME}' wurde erfolgreich erstellt.")

if __name__ == "__main__":
    main()
