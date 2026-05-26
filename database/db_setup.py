import mysql.connector

def setup_database():
    try:
        mydb=mysql.connector.connect(
            host="localhost",
            user="f1user",
            password="securepass"
        )
        mycursor=mydb.cursor()

        print("Connessione a MariaDB stabilita!")
        mycursor.execute("DROP DATABASE IF EXISTS formula1")
        
        mycursor.execute("CREATE DATABASE IF NOT EXISTS formula1")
        mycursor.execute("USE formula1")
        print("Database formula1 pronto")

        mycursor.execute("""
        CREATE TABLE IF NOT EXISTS circuiti (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                localita VARCHAR(100),
                nazione VARCHAR(50),
                lunghezza_km DECIMAL(5,3),
                numero_curve INT,
                record_sul_giro VARCHAR(20),
                capacita_spettatori INT,
                tipo_circuito ENUM('Cittadino', 'Permanente', 'Ibrido')
            )""")

        mycursor.execute("""
            CREATE TABLE IF NOT EXISTS sponsor (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome_societa VARCHAR(100) NOT NULL,
                settore_merceologico VARCHAR(100),
                valore_contratto_annuo DECIMAL(15,2),
                scadenza_contratto DATE
            )""")

        mycursor.execute("""
            CREATE TABLE IF NOT EXISTS scuderie (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                sede_legale VARCHAR(100),
                team_principal VARCHAR(100),
                costruttore_motore VARCHAR(50),
                anno_fondazione INT,
                titoli_costruttori_vinti INT DEFAULT 0,
                id_sponsor INT,
                FOREIGN KEY (id_sponsor) REFERENCES sponsor(id) ON DELETE SET NULL
            )""")

        mycursor.execute("""
        CREATE TABLE IF NOT EXISTS macchine (
                id INT AUTO_INCREMENT PRIMARY KEY,
                modello_sigla VARCHAR(50) NOT NULL,
                power_unit_modello VARCHAR(100),
                peso_kg DECIMAL(5,2),
                id_scuderia INT,
                FOREIGN KEY (id_scuderia) REFERENCES scuderie(id) ON DELETE CASCADE
            )""")

        mycursor.execute("""
            CREATE TABLE IF NOT EXISTS piloti (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(50) NOT NULL,
                cognome VARCHAR(50) NOT NULL,
                data_nascita DATE,
                nazionalita VARCHAR(50),
                numero_gara INT UNIQUE,
                stipendio_annuo DECIMAL(15,2),
                id_scuderia INT,
                FOREIGN KEY (id_scuderia) REFERENCES scuderie(id) ON DELETE SET NULL
            )""")

        mycursor.execute("""
            CREATE TABLE IF NOT EXISTS gran_premi (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome_evento VARCHAR(100),
                edizione_numero INT,
                data_inizio DATE,
                meteo_previsto VARCHAR(100),
                id_circuito INT,
                FOREIGN KEY (id_circuito) REFERENCES circuiti(id) ON DELETE CASCADE
            )""")

        mycursor.execute("""
            CREATE TABLE IF NOT EXISTS sessioni (
                id INT AUTO_INCREMENT PRIMARY KEY,
                tipo ENUM('FP1', 'FP2', 'FP3', 'Qualifiche', 'Sprint', 'Gara'),
                orario_inizio DATETIME,
                id_gran_premio INT,
                FOREIGN KEY (id_gran_premio) REFERENCES gran_premi(id) ON DELETE CASCADE
            )""")

        mycursor.execute("""
            CREATE TABLE IF NOT EXISTS risultati (
                id INT AUTO_INCREMENT PRIMARY KEY,
                posizione_finale INT,
                punti_assegnati DECIMAL(4,1),
                giro_veloce BOOLEAN DEFAULT FALSE,
                numero_pit_stop INT,
                id_pilota INT,
                id_sessione INT,
                FOREIGN KEY (id_pilota) REFERENCES piloti(id) ON DELETE CASCADE,
                FOREIGN KEY (id_sessione) REFERENCES sessioni(id) ON DELETE CASCADE
            )""")

        mycursor.execute("""
            CREATE TABLE IF NOT EXISTS squalifiche (
                id INT AUTO_INCREMENT PRIMARY KEY,
                tipo_infrazione VARCHAR(255),
                penalita_secondi INT,
                id_risultato INT,
                FOREIGN KEY (id_risultato) REFERENCES risultati(id) ON DELETE CASCADE
            )""")

        # ── DELETE (ordine inverso alle dipendenze FK) ─────────────────────
        mycursor.execute("DELETE FROM squalifiche")
        mycursor.execute("DELETE FROM risultati")
        mycursor.execute("DELETE FROM sessioni")
        mycursor.execute("DELETE FROM gran_premi")
        mycursor.execute("DELETE FROM macchine")
        mycursor.execute("DELETE FROM piloti")
        mycursor.execute("DELETE FROM scuderie")
        mycursor.execute("DELETE FROM sponsor")
        mycursor.execute("DELETE FROM circuiti")

        # ── SPONSOR ────────────────────────────────────────────────────────
        # id 1
        mycursor.execute("INSERT INTO sponsor (nome_societa, settore_merceologico, valore_contratto_annuo, scadenza_contratto) VALUES ('Aramco', 'Energia/Petrolio', 80000000.00, '2030-12-31')")
        # id 2
        mycursor.execute("INSERT INTO sponsor (nome_societa, settore_merceologico, valore_contratto_annuo, scadenza_contratto) VALUES ('Petronas', 'Energia/Petrolio', 50000000.00, '2028-12-31')")
        # id 3
        mycursor.execute("INSERT INTO sponsor (nome_societa, settore_merceologico, valore_contratto_annuo, scadenza_contratto) VALUES ('OKX', 'Criptovalute', 40000000.00, '2027-12-31')")
        # id 4
        mycursor.execute("INSERT INTO sponsor (nome_societa, settore_merceologico, valore_contratto_annuo, scadenza_contratto) VALUES ('Oracle', 'Tecnologia Cloud', 100000000.00, '2030-12-31')")
        # id 5
        mycursor.execute("INSERT INTO sponsor (nome_societa, settore_merceologico, valore_contratto_annuo, scadenza_contratto) VALUES ('BWT', 'Depurazione Acqua', 20000000.00, '2027-12-31')")
        # id 6
        mycursor.execute("INSERT INTO sponsor (nome_societa, settore_merceologico, valore_contratto_annuo, scadenza_contratto) VALUES ('MoneyGram', 'Servizi Finanziari', 25000000.00, '2027-12-31')")
        # id 7
        mycursor.execute("INSERT INTO sponsor (nome_societa, settore_merceologico, valore_contratto_annuo, scadenza_contratto) VALUES ('Visa Cash App RB', 'Servizi Finanziari', 30000000.00, '2028-12-31')")
        # id 8
        mycursor.execute("INSERT INTO sponsor (nome_societa, settore_merceologico, valore_contratto_annuo, scadenza_contratto) VALUES ('Duracell', 'Elettronica/Batterie', 15000000.00, '2027-12-31')")
        # id 9
        mycursor.execute("INSERT INTO sponsor (nome_societa, settore_merceologico, valore_contratto_annuo, scadenza_contratto) VALUES ('Audi AG', 'Automotive', 200000000.00, '2035-12-31')")
        # id 10
        mycursor.execute("INSERT INTO sponsor (nome_societa, settore_merceologico, valore_contratto_annuo, scadenza_contratto) VALUES ('General Motors', 'Automotive', 150000000.00, '2035-12-31')")
        # id 11
        mycursor.execute("INSERT INTO sponsor (nome_societa, settore_merceologico, valore_contratto_annuo, scadenza_contratto) VALUES ('Cognizant', 'Consulenza IT', 40000000.00, '2028-12-31')")

        # ── CIRCUITI (22 gare del calendario 2026) ─────────────────────────
        # id 1
        mycursor.execute("INSERT INTO circuiti (nome, localita, nazione, lunghezza_km, numero_curve, record_sul_giro, capacita_spettatori, tipo_circuito) VALUES ('Albert Park Circuit', 'Melbourne', 'Australia', 5.278, 16, '1:20.235', 120000, 'Ibrido')")
        # id 2
        mycursor.execute("INSERT INTO circuiti (nome, localita, nazione, lunghezza_km, numero_curve, record_sul_giro, capacita_spettatori, tipo_circuito) VALUES ('Shanghai International Circuit', 'Shanghai', 'Cina', 5.451, 16, '1:32.238', 200000, 'Permanente')")
        # id 3
        mycursor.execute("INSERT INTO circuiti (nome, localita, nazione, lunghezza_km, numero_curve, record_sul_giro, capacita_spettatori, tipo_circuito) VALUES ('Suzuka Circuit', 'Suzuka', 'Giappone', 5.807, 18, '1:30.983', 115000, 'Permanente')")
        # id 4
        mycursor.execute("INSERT INTO circuiti (nome, localita, nazione, lunghezza_km, numero_curve, record_sul_giro, capacita_spettatori, tipo_circuito) VALUES ('Miami International Autodrome', 'Miami', 'USA', 5.412, 19, '1:26.841', 90000, 'Ibrido')")
        # id 5
        mycursor.execute("INSERT INTO circuiti (nome, localita, nazione, lunghezza_km, numero_curve, record_sul_giro, capacita_spettatori, tipo_circuito) VALUES ('Circuit Gilles Villeneuve', 'Montreal', 'Canada', 4.361, 14, '1:13.078', 100000, 'Ibrido')")
        # id 6
        mycursor.execute("INSERT INTO circuiti (nome, localita, nazione, lunghezza_km, numero_curve, record_sul_giro, capacita_spettatori, tipo_circuito) VALUES ('Circuit de Monaco', 'Monte Carlo', 'Monaco', 3.337, 19, '1:10.166', 37000, 'Cittadino')")
        # id 7
        mycursor.execute("INSERT INTO circuiti (nome, localita, nazione, lunghezza_km, numero_curve, record_sul_giro, capacita_spettatori, tipo_circuito) VALUES ('Circuit de Barcelona-Catalunya', 'Montmelo', 'Spagna', 4.657, 16, '1:16.330', 140000, 'Permanente')")
        # id 8
        mycursor.execute("INSERT INTO circuiti (nome, localita, nazione, lunghezza_km, numero_curve, record_sul_giro, capacita_spettatori, tipo_circuito) VALUES ('Red Bull Ring', 'Spielberg', 'Austria', 4.318, 10, '1:05.619', 55000, 'Permanente')")
        # id 9
        mycursor.execute("INSERT INTO circuiti (nome, localita, nazione, lunghezza_km, numero_curve, record_sul_giro, capacita_spettatori, tipo_circuito) VALUES ('Silverstone Circuit', 'Silverstone', 'Gran Bretagna', 5.891, 18, '1:26.600', 150000, 'Permanente')")
        # id 10
        mycursor.execute("INSERT INTO circuiti (nome, localita, nazione, lunghezza_km, numero_curve, record_sul_giro, capacita_spettatori, tipo_circuito) VALUES ('Circuit de Spa-Francorchamps', 'Spa', 'Belgio', 7.004, 19, '1:41.252', 90000, 'Permanente')")
        # id 11
        mycursor.execute("INSERT INTO circuiti (nome, localita, nazione, lunghezza_km, numero_curve, record_sul_giro, capacita_spettatori, tipo_circuito) VALUES ('Hungaroring', 'Budapest', 'Ungheria', 4.381, 14, '1:16.627', 80000, 'Permanente')")
        # id 12
        mycursor.execute("INSERT INTO circuiti (nome, localita, nazione, lunghezza_km, numero_curve, record_sul_giro, capacita_spettatori, tipo_circuito) VALUES ('Circuit Zandvoort', 'Zandvoort', 'Paesi Bassi', 4.259, 14, '1:11.097', 105000, 'Permanente')")
        # id 13
        mycursor.execute("INSERT INTO circuiti (nome, localita, nazione, lunghezza_km, numero_curve, record_sul_giro, capacita_spettatori, tipo_circuito) VALUES ('Autodromo Nazionale Monza', 'Monza', 'Italia', 5.793, 11, '1:21.046', 113000, 'Permanente')")
        # id 14
        mycursor.execute("INSERT INTO circuiti (nome, localita, nazione, lunghezza_km, numero_curve, record_sul_giro, capacita_spettatori, tipo_circuito) VALUES ('Circuito de Madrid', 'Madrid', 'Spagna', 5.470, 20, '1:22.000', 110000, 'Cittadino')")
        # id 15
        mycursor.execute("INSERT INTO circuiti (nome, localita, nazione, lunghezza_km, numero_curve, record_sul_giro, capacita_spettatori, tipo_circuito) VALUES ('Baku City Circuit', 'Baku', 'Azerbaigian', 6.003, 20, '1:41.218', 30000, 'Cittadino')")
        # id 16
        mycursor.execute("INSERT INTO circuiti (nome, localita, nazione, lunghezza_km, numero_curve, record_sul_giro, capacita_spettatori, tipo_circuito) VALUES ('Marina Bay Street Circuit', 'Singapore', 'Singapore', 4.940, 19, '1:29.525', 85000, 'Cittadino')")
        # id 17
        mycursor.execute("INSERT INTO circuiti (nome, localita, nazione, lunghezza_km, numero_curve, record_sul_giro, capacita_spettatori, tipo_circuito) VALUES ('Circuit of the Americas', 'Austin', 'USA', 5.513, 20, '1:36.169', 120000, 'Permanente')")
        # id 18
        mycursor.execute("INSERT INTO circuiti (nome, localita, nazione, lunghezza_km, numero_curve, record_sul_giro, capacita_spettatori, tipo_circuito) VALUES ('Autodromo Hermanos Rodriguez', 'Citta del Messico', 'Messico', 4.304, 17, '1:17.774', 140000, 'Permanente')")
        # id 19
        mycursor.execute("INSERT INTO circuiti (nome, localita, nazione, lunghezza_km, numero_curve, record_sul_giro, capacita_spettatori, tipo_circuito) VALUES ('Autodromo Jose Carlos Pace', 'San Paolo', 'Brasile', 4.309, 15, '1:10.540', 70000, 'Permanente')")
        # id 20
        mycursor.execute("INSERT INTO circuiti (nome, localita, nazione, lunghezza_km, numero_curve, record_sul_giro, capacita_spettatori, tipo_circuito) VALUES ('Las Vegas Strip Circuit', 'Las Vegas', 'USA', 6.201, 17, '1:31.000', 170000, 'Cittadino')")
        # id 21
        mycursor.execute("INSERT INTO circuiti (nome, localita, nazione, lunghezza_km, numero_curve, record_sul_giro, capacita_spettatori, tipo_circuito) VALUES ('Lusail International Circuit', 'Lusail', 'Qatar', 5.419, 16, '1:24.319', 40000, 'Permanente')")
        # id 22
        mycursor.execute("INSERT INTO circuiti (nome, localita, nazione, lunghezza_km, numero_curve, record_sul_giro, capacita_spettatori, tipo_circuito) VALUES ('Yas Marina Circuit', 'Abu Dhabi', 'Emirati Arabi', 5.281, 16, '1:26.103', 55000, 'Permanente')")

        # ── SCUDERIE (11 team 2026) ────────────────────────────────────────
        # id 1 - sponsor Aramco (id 1)
        mycursor.execute("INSERT INTO scuderie (nome, sede_legale, team_principal, costruttore_motore, anno_fondazione, titoli_costruttori_vinti, id_sponsor) VALUES ('Ferrari', 'Maranello, Italia', 'Fred Vasseur', 'Ferrari', 1929, 16, 1)")
        # id 2 - sponsor Petronas (id 2)
        mycursor.execute("INSERT INTO scuderie (nome, sede_legale, team_principal, costruttore_motore, anno_fondazione, titoli_costruttori_vinti, id_sponsor) VALUES ('Mercedes-AMG Petronas', 'Brackley, Gran Bretagna', 'Toto Wolff', 'Mercedes', 1954, 8, 2)")
        # id 3 - sponsor OKX (id 3)
        mycursor.execute("INSERT INTO scuderie (nome, sede_legale, team_principal, costruttore_motore, anno_fondazione, titoli_costruttori_vinti, id_sponsor) VALUES ('McLaren', 'Woking, Gran Bretagna', 'Andrea Stella', 'Mercedes', 1963, 8, 3)")
        # id 4 - sponsor Oracle (id 4)
        mycursor.execute("INSERT INTO scuderie (nome, sede_legale, team_principal, costruttore_motore, anno_fondazione, titoli_costruttori_vinti, id_sponsor) VALUES ('Red Bull Racing', 'Milton Keynes, Gran Bretagna', 'Laurent Mekies', 'Ford RBPT', 2005, 6, 4)")
        # id 5 - sponsor BWT (id 5)
        mycursor.execute("INSERT INTO scuderie (nome, sede_legale, team_principal, costruttore_motore, anno_fondazione, titoli_costruttori_vinti, id_sponsor) VALUES ('Alpine', 'Enstone, Gran Bretagna', 'Flavio Briatore', 'Mercedes', 1981, 2, 5)")
        # id 6 - sponsor MoneyGram (id 6)
        mycursor.execute("INSERT INTO scuderie (nome, sede_legale, team_principal, costruttore_motore, anno_fondazione, titoli_costruttori_vinti, id_sponsor) VALUES ('Haas F1 Team', 'Kannapolis, USA', 'Ayao Komatsu', 'Ferrari', 2016, 0, 6)")
        # id 7 - sponsor Visa Cash App RB (id 7)
        mycursor.execute("INSERT INTO scuderie (nome, sede_legale, team_principal, costruttore_motore, anno_fondazione, titoli_costruttori_vinti, id_sponsor) VALUES ('Racing Bulls', 'Faenza, Italia', 'Alan Permane', 'Ford RBPT', 1985, 0, 7)")
        # id 8 - sponsor Duracell (id 8)
        mycursor.execute("INSERT INTO scuderie (nome, sede_legale, team_principal, costruttore_motore, anno_fondazione, titoli_costruttori_vinti, id_sponsor) VALUES ('Williams Racing', 'Grove, Gran Bretagna', 'James Vowles', 'Mercedes', 1977, 7, 8)")
        # id 9 - sponsor Audi AG (id 9)
        mycursor.execute("INSERT INTO scuderie (nome, sede_legale, team_principal, costruttore_motore, anno_fondazione, titoli_costruttori_vinti, id_sponsor) VALUES ('Audi', 'Hinwil, Svizzera', 'Mattia Binotto', 'Audi', 1993, 0, 9)")
        # id 10 - sponsor General Motors (id 10)
        mycursor.execute("INSERT INTO scuderie (nome, sede_legale, team_principal, costruttore_motore, anno_fondazione, titoli_costruttori_vinti, id_sponsor) VALUES ('Cadillac', 'Concord, USA', 'Graeme Lowdon', 'Ferrari', 2026, 0, 10)")
        # id 11 - sponsor Cognizant (id 11)
        mycursor.execute("INSERT INTO scuderie (nome, sede_legale, team_principal, costruttore_motore, anno_fondazione, titoli_costruttori_vinti, id_sponsor) VALUES ('Aston Martin Aramco', 'Silverstone, Gran Bretagna', 'Mike Krack', 'Honda', 2018, 0, 11)")

        # ── MACCHINE (una per scuderia) ────────────────────────────────────
        mycursor.execute("INSERT INTO macchine (modello_sigla, power_unit_modello, peso_kg, id_scuderia) VALUES ('SF-26', 'Ferrari 066/13', 798.00, 1)")
        mycursor.execute("INSERT INTO macchine (modello_sigla, power_unit_modello, peso_kg, id_scuderia) VALUES ('W17', 'Mercedes-AMG F1 M16', 798.00, 2)")
        mycursor.execute("INSERT INTO macchine (modello_sigla, power_unit_modello, peso_kg, id_scuderia) VALUES ('MCL43', 'Mercedes-AMG F1 M16', 798.00, 3)")
        mycursor.execute("INSERT INTO macchine (modello_sigla, power_unit_modello, peso_kg, id_scuderia) VALUES ('RB22', 'Ford RBPT003', 798.00, 4)")
        mycursor.execute("INSERT INTO macchine (modello_sigla, power_unit_modello, peso_kg, id_scuderia) VALUES ('A526', 'Mercedes-AMG F1 M16', 798.00, 5)")
        mycursor.execute("INSERT INTO macchine (modello_sigla, power_unit_modello, peso_kg, id_scuderia) VALUES ('VF-26', 'Ferrari 066/13', 798.00, 6)")
        mycursor.execute("INSERT INTO macchine (modello_sigla, power_unit_modello, peso_kg, id_scuderia) VALUES ('VCARB 02', 'Ford RBPT003', 798.00, 7)")
        mycursor.execute("INSERT INTO macchine (modello_sigla, power_unit_modello, peso_kg, id_scuderia) VALUES ('FW47', 'Mercedes-AMG F1 M16', 798.00, 8)")
        mycursor.execute("INSERT INTO macchine (modello_sigla, power_unit_modello, peso_kg, id_scuderia) VALUES ('C44e', 'Audi PU001', 798.00, 9)")
        mycursor.execute("INSERT INTO macchine (modello_sigla, power_unit_modello, peso_kg, id_scuderia) VALUES ('CF1', 'Ferrari 066/13', 798.00, 10)")
        mycursor.execute("INSERT INTO macchine (modello_sigla, power_unit_modello, peso_kg, id_scuderia) VALUES ('AMR26', 'Honda RA626H', 798.00, 11)")

        # ── PILOTI (22 piloti griglia 2026) ───────────────────────────────
        # Mercedes (id_scuderia=2)
        mycursor.execute("INSERT INTO piloti (nome, cognome, data_nascita, nazionalita, numero_gara, stipendio_annuo, id_scuderia) VALUES ('George', 'Russell', '1998-02-15', 'Britannica', 63, 20000000.00, 2)")
        mycursor.execute("INSERT INTO piloti (nome, cognome, data_nascita, nazionalita, numero_gara, stipendio_annuo, id_scuderia) VALUES ('Kimi', 'Antonelli', '2006-08-25', 'Italiana', 12, 2000000.00, 2)")
        # Ferrari (id_scuderia=1)
        mycursor.execute("INSERT INTO piloti (nome, cognome, data_nascita, nazionalita, numero_gara, stipendio_annuo, id_scuderia) VALUES ('Charles', 'Leclerc', '1997-10-16', 'Monegasca', 16, 25000000.00, 1)")
        mycursor.execute("INSERT INTO piloti (nome, cognome, data_nascita, nazionalita, numero_gara, stipendio_annuo, id_scuderia) VALUES ('Lewis', 'Hamilton', '1985-01-07', 'Britannica', 44, 50000000.00, 1)")
        # McLaren (id_scuderia=3)
        mycursor.execute("INSERT INTO piloti (nome, cognome, data_nascita, nazionalita, numero_gara, stipendio_annuo, id_scuderia) VALUES ('Lando', 'Norris', '1999-11-13', 'Britannica', 4, 35000000.00, 3)")
        mycursor.execute("INSERT INTO piloti (nome, cognome, data_nascita, nazionalita, numero_gara, stipendio_annuo, id_scuderia) VALUES ('Oscar', 'Piastri', '2001-04-06', 'Australiana', 81, 12000000.00, 3)")
        # Red Bull (id_scuderia=4)
        mycursor.execute("INSERT INTO piloti (nome, cognome, data_nascita, nazionalita, numero_gara, stipendio_annuo, id_scuderia) VALUES ('Max', 'Verstappen', '1997-09-30', 'Olandese', 33, 60000000.00, 4)")
        mycursor.execute("INSERT INTO piloti (nome, cognome, data_nascita, nazionalita, numero_gara, stipendio_annuo, id_scuderia) VALUES ('Isack', 'Hadjar', '2004-02-28', 'Francese', 6, 2000000.00, 4)")
        # Alpine (id_scuderia=5)
        mycursor.execute("INSERT INTO piloti (nome, cognome, data_nascita, nazionalita, numero_gara, stipendio_annuo, id_scuderia) VALUES ('Pierre', 'Gasly', '1996-02-07', 'Francese', 10, 8000000.00, 5)")
        mycursor.execute("INSERT INTO piloti (nome, cognome, data_nascita, nazionalita, numero_gara, stipendio_annuo, id_scuderia) VALUES ('Franco', 'Colapinto', '2003-05-27', 'Argentina', 43, 3000000.00, 5)")
        # Haas (id_scuderia=6)
        mycursor.execute("INSERT INTO piloti (nome, cognome, data_nascita, nazionalita, numero_gara, stipendio_annuo, id_scuderia) VALUES ('Esteban', 'Ocon', '1996-09-17', 'Francese', 31, 7000000.00, 6)")
        mycursor.execute("INSERT INTO piloti (nome, cognome, data_nascita, nazionalita, numero_gara, stipendio_annuo, id_scuderia) VALUES ('Oliver', 'Bearman', '2005-05-08', 'Britannica', 87, 2000000.00, 6)")
        # Racing Bulls (id_scuderia=7)
        mycursor.execute("INSERT INTO piloti (nome, cognome, data_nascita, nazionalita, numero_gara, stipendio_annuo, id_scuderia) VALUES ('Liam', 'Lawson', '2002-02-11', 'Neozelandese', 30, 3000000.00, 7)")
        mycursor.execute("INSERT INTO piloti (nome, cognome, data_nascita, nazionalita, numero_gara, stipendio_annuo, id_scuderia) VALUES ('Arvid', 'Lindblad', '2006-01-22', 'Britannica', 40, 1500000.00, 7)")
        # Williams (id_scuderia=8)
        mycursor.execute("INSERT INTO piloti (nome, cognome, data_nascita, nazionalita, numero_gara, stipendio_annuo, id_scuderia) VALUES ('Carlos', 'Sainz', '1994-09-01', 'Spagnola', 55, 15000000.00, 8)")
        mycursor.execute("INSERT INTO piloti (nome, cognome, data_nascita, nazionalita, numero_gara, stipendio_annuo, id_scuderia) VALUES ('Alexander', 'Albon', '1996-03-23', 'Thailandese', 23, 4000000.00, 8)")
        # Audi (id_scuderia=9)
        mycursor.execute("INSERT INTO piloti (nome, cognome, data_nascita, nazionalita, numero_gara, stipendio_annuo, id_scuderia) VALUES ('Nico', 'Hulkenberg', '1987-08-19', 'Tedesca', 27, 5000000.00, 9)")
        mycursor.execute("INSERT INTO piloti (nome, cognome, data_nascita, nazionalita, numero_gara, stipendio_annuo, id_scuderia) VALUES ('Gabriel', 'Bortoleto', '2004-10-14', 'Brasiliana', 5, 2000000.00, 9)")
        # Cadillac (id_scuderia=10)
        mycursor.execute("INSERT INTO piloti (nome, cognome, data_nascita, nazionalita, numero_gara, stipendio_annuo, id_scuderia) VALUES ('Sergio', 'Perez', '1990-01-26', 'Messicana', 11, 7000000.00, 10)")
        mycursor.execute("INSERT INTO piloti (nome, cognome, data_nascita, nazionalita, numero_gara, stipendio_annuo, id_scuderia) VALUES ('Valtteri', 'Bottas', '1989-08-28', 'Finlandese', 77, 5000000.00, 10)")
        # Aston Martin (id_scuderia=11)
        mycursor.execute("INSERT INTO piloti (nome, cognome, data_nascita, nazionalita, numero_gara, stipendio_annuo, id_scuderia) VALUES ('Fernando', 'Alonso', '1981-07-29', 'Spagnola', 14, 20000000.00, 11)")
        mycursor.execute("INSERT INTO piloti (nome, cognome, data_nascita, nazionalita, numero_gara, stipendio_annuo, id_scuderia) VALUES ('Lance', 'Stroll', '1998-10-29', 'Canadese', 18, 5000000.00, 11)")

        # ── GRAN PREMI (22 gare calendario 2026) ──────────────────────────
        mycursor.execute("INSERT INTO gran_premi (nome_evento, edizione_numero, data_inizio, meteo_previsto, id_circuito) VALUES ('Gran Premio d Australia', 44, '2026-03-08', 'Soleggiato, 22C', 1)")
        mycursor.execute("INSERT INTO gran_premi (nome_evento, edizione_numero, data_inizio, meteo_previsto, id_circuito) VALUES ('Gran Premio di Cina', 20, '2026-03-15', 'Nuvoloso, 18C', 2)")
        mycursor.execute("INSERT INTO gran_premi (nome_evento, edizione_numero, data_inizio, meteo_previsto, id_circuito) VALUES ('Gran Premio del Giappone', 36, '2026-03-29', 'Soleggiato, 19C', 3)")
        mycursor.execute("INSERT INTO gran_premi (nome_evento, edizione_numero, data_inizio, meteo_previsto, id_circuito) VALUES ('Gran Premio di Miami', 5, '2026-05-03', 'Soleggiato, 29C', 4)")
        mycursor.execute("INSERT INTO gran_premi (nome_evento, edizione_numero, data_inizio, meteo_previsto, id_circuito) VALUES ('Gran Premio del Canada', 55, '2026-05-24', 'Variabile, 20C', 5)")
        mycursor.execute("INSERT INTO gran_premi (nome_evento, edizione_numero, data_inizio, meteo_previsto, id_circuito) VALUES ('Gran Premio di Monaco', 83, '2026-06-07', 'Soleggiato, 24C', 6)")
        mycursor.execute("INSERT INTO gran_premi (nome_evento, edizione_numero, data_inizio, meteo_previsto, id_circuito) VALUES ('Gran Premio di Spagna', 42, '2026-06-14', 'Soleggiato, 27C', 7)")
        mycursor.execute("INSERT INTO gran_premi (nome_evento, edizione_numero, data_inizio, meteo_previsto, id_circuito) VALUES ('Gran Premio d Austria', 32, '2026-06-28', 'Soleggiato, 25C', 8)")
        mycursor.execute("INSERT INTO gran_premi (nome_evento, edizione_numero, data_inizio, meteo_previsto, id_circuito) VALUES ('Gran Premio di Gran Bretagna', 78, '2026-07-05', 'Nuvoloso, 21C', 9)")
        mycursor.execute("INSERT INTO gran_premi (nome_evento, edizione_numero, data_inizio, meteo_previsto, id_circuito) VALUES ('Gran Premio del Belgio', 72, '2026-07-19', 'Variabile, 18C', 10)")
        mycursor.execute("INSERT INTO gran_premi (nome_evento, edizione_numero, data_inizio, meteo_previsto, id_circuito) VALUES ('Gran Premio d Ungheria', 40, '2026-07-26', 'Soleggiato, 31C', 11)")
        mycursor.execute("INSERT INTO gran_premi (nome_evento, edizione_numero, data_inizio, meteo_previsto, id_circuito) VALUES ('Gran Premio dei Paesi Bassi', 6, '2026-08-23', 'Ventoso, 20C', 12)")
        mycursor.execute("INSERT INTO gran_premi (nome_evento, edizione_numero, data_inizio, meteo_previsto, id_circuito) VALUES ('Gran Premio d Italia', 97, '2026-09-06', 'Soleggiato, 26C', 13)")
        mycursor.execute("INSERT INTO gran_premi (nome_evento, edizione_numero, data_inizio, meteo_previsto, id_circuito) VALUES ('Gran Premio di Madrid', 1, '2026-09-13', 'Soleggiato, 28C', 14)")
        mycursor.execute("INSERT INTO gran_premi (nome_evento, edizione_numero, data_inizio, meteo_previsto, id_circuito) VALUES ('Gran Premio d Azerbaigian', 10, '2026-09-26', 'Soleggiato, 23C', 15)")
        mycursor.execute("INSERT INTO gran_premi (nome_evento, edizione_numero, data_inizio, meteo_previsto, id_circuito) VALUES ('Gran Premio di Singapore', 18, '2026-10-11', 'Umido, 30C', 16)")
        mycursor.execute("INSERT INTO gran_premi (nome_evento, edizione_numero, data_inizio, meteo_previsto, id_circuito) VALUES ('Gran Premio degli USA', 22, '2026-10-25', 'Soleggiato, 24C', 17)")
        mycursor.execute("INSERT INTO gran_premi (nome_evento, edizione_numero, data_inizio, meteo_previsto, id_circuito) VALUES ('Gran Premio del Messico', 52, '2026-11-01', 'Soleggiato, 20C', 18)")
        mycursor.execute("INSERT INTO gran_premi (nome_evento, edizione_numero, data_inizio, meteo_previsto, id_circuito) VALUES ('Gran Premio del Brasile', 54, '2026-11-08', 'Variabile, 25C', 19)")
        mycursor.execute("INSERT INTO gran_premi (nome_evento, edizione_numero, data_inizio, meteo_previsto, id_circuito) VALUES ('Gran Premio di Las Vegas', 4, '2026-11-21', 'Sereno, 15C', 20)")
        mycursor.execute("INSERT INTO gran_premi (nome_evento, edizione_numero, data_inizio, meteo_previsto, id_circuito) VALUES ('Gran Premio del Qatar', 5, '2026-11-29', 'Caldo, 28C', 21)")
        mycursor.execute("INSERT INTO gran_premi (nome_evento, edizione_numero, data_inizio, meteo_previsto, id_circuito) VALUES ('Gran Premio di Abu Dhabi', 16, '2026-12-06', 'Soleggiato, 26C', 22)")

        # ── SESSIONI (prime 4 gare completate + qualifiche + sprint) ──────
        # Gara GP Australia (id_gran_premio=1) -> id sessione=1
        mycursor.execute("INSERT INTO sessioni (tipo, orario_inizio, id_gran_premio) VALUES ('Gara', '2026-03-08 15:00:00', 1)")
        # Gara GP Cina (id_gran_premio=2) -> id sessione=2
        mycursor.execute("INSERT INTO sessioni (tipo, orario_inizio, id_gran_premio) VALUES ('Gara', '2026-03-15 08:00:00', 2)")
        # Gara GP Giappone (id_gran_premio=3) -> id sessione=3
        mycursor.execute("INSERT INTO sessioni (tipo, orario_inizio, id_gran_premio) VALUES ('Gara', '2026-03-29 14:00:00', 3)")
        # Gara GP Miami (id_gran_premio=4) -> id sessione=4
        mycursor.execute("INSERT INTO sessioni (tipo, orario_inizio, id_gran_premio) VALUES ('Gara', '2026-05-03 22:00:00', 4)")
        # Qualifiche GP Australia -> id sessione=5
        mycursor.execute("INSERT INTO sessioni (tipo, orario_inizio, id_gran_premio) VALUES ('Qualifiche', '2026-03-07 15:00:00', 1)")
        # Qualifiche GP Cina -> id sessione=6
        mycursor.execute("INSERT INTO sessioni (tipo, orario_inizio, id_gran_premio) VALUES ('Qualifiche', '2026-03-14 08:00:00', 2)")
        # Qualifiche GP Giappone -> id sessione=7
        mycursor.execute("INSERT INTO sessioni (tipo, orario_inizio, id_gran_premio) VALUES ('Qualifiche', '2026-03-28 14:00:00', 3)")
        # Qualifiche GP Miami -> id sessione=8
        mycursor.execute("INSERT INTO sessioni (tipo, orario_inizio, id_gran_premio) VALUES ('Qualifiche', '2026-05-02 22:00:00', 4)")
        # Sprint GP Cina (weekend sprint) -> id sessione=9
        mycursor.execute("INSERT INTO sessioni (tipo, orario_inizio, id_gran_premio) VALUES ('Sprint', '2026-03-15 04:00:00', 2)")
        # Sprint GP Miami (weekend sprint) -> id sessione=10
        mycursor.execute("INSERT INTO sessioni (tipo, orario_inizio, id_gran_premio) VALUES ('Sprint', '2026-05-03 18:00:00', 4)")

        # ── RISULTATI (top 3 gare completate) ─────────────────────────────
        # Piloti IDs: Russell=1, Antonelli=2, Leclerc=3, Hamilton=4, Norris=5, Piastri=6

        # GP Australia (sessione id=1): Russell 1°, Antonelli 2°, Leclerc 3°
        mycursor.execute("INSERT INTO risultati (posizione_finale, punti_assegnati, giro_veloce, numero_pit_stop, id_pilota, id_sessione) VALUES (1, 25.0, FALSE, 2, 1, 1)")
        mycursor.execute("INSERT INTO risultati (posizione_finale, punti_assegnati, giro_veloce, numero_pit_stop, id_pilota, id_sessione) VALUES (2, 18.0, FALSE, 2, 2, 1)")
        mycursor.execute("INSERT INTO risultati (posizione_finale, punti_assegnati, giro_veloce, numero_pit_stop, id_pilota, id_sessione) VALUES (3, 15.0, TRUE,  2, 3, 1)")
        mycursor.execute("INSERT INTO risultati (posizione_finale, punti_assegnati, giro_veloce, numero_pit_stop, id_pilota, id_sessione) VALUES (4, 12.0, FALSE, 2, 6, 1)")
        mycursor.execute("INSERT INTO risultati (posizione_finale, punti_assegnati, giro_veloce, numero_pit_stop, id_pilota, id_sessione) VALUES (5, 10.0, FALSE, 2, 5, 1)")

        # GP Cina (sessione id=2): Antonelli 1°, Russell 2°, Hamilton 3°
        mycursor.execute("INSERT INTO risultati (posizione_finale, punti_assegnati, giro_veloce, numero_pit_stop, id_pilota, id_sessione) VALUES (1, 25.0, FALSE, 2, 2, 2)")
        mycursor.execute("INSERT INTO risultati (posizione_finale, punti_assegnati, giro_veloce, numero_pit_stop, id_pilota, id_sessione) VALUES (2, 18.0, FALSE, 2, 1, 2)")
        mycursor.execute("INSERT INTO risultati (posizione_finale, punti_assegnati, giro_veloce, numero_pit_stop, id_pilota, id_sessione) VALUES (3, 15.0, TRUE,  2, 4, 2)")
        mycursor.execute("INSERT INTO risultati (posizione_finale, punti_assegnati, giro_veloce, numero_pit_stop, id_pilota, id_sessione) VALUES (4, 12.0, FALSE, 2, 3, 2)")
        mycursor.execute("INSERT INTO risultati (posizione_finale, punti_assegnati, giro_veloce, numero_pit_stop, id_pilota, id_sessione) VALUES (5, 10.0, FALSE, 2, 5, 2)")

        # GP Giappone (sessione id=3): Antonelli 1°, Piastri 2°, Leclerc 3°
        mycursor.execute("INSERT INTO risultati (posizione_finale, punti_assegnati, giro_veloce, numero_pit_stop, id_pilota, id_sessione) VALUES (1, 25.0, FALSE, 2, 2, 3)")
        mycursor.execute("INSERT INTO risultati (posizione_finale, punti_assegnati, giro_veloce, numero_pit_stop, id_pilota, id_sessione) VALUES (2, 18.0, FALSE, 2, 6, 3)")
        mycursor.execute("INSERT INTO risultati (posizione_finale, punti_assegnati, giro_veloce, numero_pit_stop, id_pilota, id_sessione) VALUES (3, 15.0, TRUE,  2, 3, 3)")
        mycursor.execute("INSERT INTO risultati (posizione_finale, punti_assegnati, giro_veloce, numero_pit_stop, id_pilota, id_sessione) VALUES (4, 12.0, FALSE, 2, 5, 3)")
        mycursor.execute("INSERT INTO risultati (posizione_finale, punti_assegnati, giro_veloce, numero_pit_stop, id_pilota, id_sessione) VALUES (5, 10.0, FALSE, 2, 1, 3)")

        # GP Miami (sessione id=4): Antonelli 1°, Norris 2°, Russell 3°
        mycursor.execute("INSERT INTO risultati (posizione_finale, punti_assegnati, giro_veloce, numero_pit_stop, id_pilota, id_sessione) VALUES (1, 25.0, FALSE, 2, 2, 4)")
        mycursor.execute("INSERT INTO risultati (posizione_finale, punti_assegnati, giro_veloce, numero_pit_stop, id_pilota, id_sessione) VALUES (2, 18.0, FALSE, 2, 5, 4)")
        mycursor.execute("INSERT INTO risultati (posizione_finale, punti_assegnati, giro_veloce, numero_pit_stop, id_pilota, id_sessione) VALUES (3, 15.0, TRUE,  2, 1, 4)")
        mycursor.execute("INSERT INTO risultati (posizione_finale, punti_assegnati, giro_veloce, numero_pit_stop, id_pilota, id_sessione) VALUES (4, 12.0, FALSE, 2, 6, 4)")
        mycursor.execute("INSERT INTO risultati (posizione_finale, punti_assegnati, giro_veloce, numero_pit_stop, id_pilota, id_sessione) VALUES (5, 10.0, FALSE, 2, 4, 4)")

        mydb.commit()
        print("Database popolato con i dati reali della stagione F1 2026!")

    except mysql.connector.Error as err:
        print(f"Errore di MariaDB: {err}")

if __name__== '__main__':
    setup_database()