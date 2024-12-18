-- Tabel voor games
CREATE TABLE games (
    gamenr INTEGER PRIMARY KEY AUTOINCREMENT,   -- Uniek nummer voor de game
    gamename VARCHAR(100) NOT NULL UNIQUE       -- Naam van de game (moet uniek zijn)
);

-- Tabel voor bibliotheken die gebruikers aan games koppelen
CREATE TABLE library (
    librarynr INTEGER PRIMARY KEY AUTOINCREMENT, -- Uniek ID voor de bibliotheek
    accountnr INT NOT NULL,                      -- Verwijzing naar de gebruiker
    gamenr INT NOT NULL,                         -- Verwijzing naar de game
    hours INT DEFAULT 0,                         -- Aantal uur gespeeld (default = 0)
    FOREIGN KEY (accountnr) REFERENCES accounts(accountnr) ON DELETE CASCADE,
    FOREIGN KEY (gamenr) REFERENCES games(gamenr) ON DELETE CASCADE,
    UNIQUE(accountnr, gamenr)                    -- Zorgt ervoor dat dezelfde gebruiker niet meerdere keren dezelfde game heeft
);

-- Tabel voor vriendenrelaties tussen gebruikers
CREATE TABLE friends (
    friendnr INTEGER PRIMARY KEY AUTOINCREMENT, -- Uniek ID voor de vriendschap
    accountnr1 INT NOT NULL,                         -- Eerste gebruiker in de relatie
    accountnr2 INT NOT NULL,                         -- Tweede gebruiker in de relatie
    FOREIGN KEY (accountnr1) REFERENCES accounts(accountnr) ON DELETE CASCADE,
    FOREIGN KEY (accountnr2) REFERENCES accounts(accountnr) ON DELETE CASCADE,
    UNIQUE(accountnr1, accountnr2),                 -- Voorkomt duplicaten
    CHECK (accountnr1 <> accountnr2)                -- Voorkomt dat iemand vriend met zichzelf is
);

-- Optioneel: Tabel voor gedeelde games tussen vrienden
CREATE TABLE shared_games (
    sharednr INTEGER PRIMARY KEY AUTOINCREMENT,   -- Uniek ID voor gedeelde games
    friendnr INT NOT NULL,                    -- Verwijzing naar een vriendschap
    librarynr INT NOT NULL,                        -- Verwijzing naar een game in de bibliotheek
    FOREIGN KEY (friendnr) REFERENCES friends(friendnr) ON DELETE CASCADE,
    FOREIGN KEY (librarynr) REFERENCES library(librarynr) ON DELETE CASCADE
);
