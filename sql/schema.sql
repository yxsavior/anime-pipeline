-- Main entity: stores the core information about each anime
CREATE TABLE IF NOT EXISTS anime (
    mal_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    type TEXT NOT NULL
        CHECK (
            type IN (
                'TV',
                'Movie',
                'OVA',
                'ONA',
                'Special',
                'Music',
                'CM',
                'PV',
                'TV Special'
            )
        ),
    episodes INTEGER
        CHECK (episodes >= 0),
    status TEXT NOT NULL,
    rating TEXT,
    score NUMERIC(4,2)
        CHECK (score BETWEEN 0 AND 10),
    scored_by INTEGER
        CHECK (scored_by >= 0),
    season TEXT,
    year INTEGER
        CHECK (year >= 1960)
);

-- Lookup tables: store reusable reference data
CREATE TABLE IF NOT EXISTS genre (
    mal_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS theme (
    mal_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS studio (
    mal_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

-- Junction tables: implement many-to-many relationships
CREATE TABLE IF NOT EXISTS anime_genre (
    anime_mal_id INTEGER NOT NULL 
        REFERENCES anime(mal_id) 
        ON DELETE CASCADE,

    genre_mal_id INTEGER NOT NULL 
        REFERENCES genre(mal_id) 
        ON DELETE CASCADE,

    PRIMARY KEY (anime_mal_id, genre_mal_id)
);

CREATE TABLE IF NOT EXISTS anime_theme (
    anime_mal_id INTEGER NOT NULL 
        REFERENCES anime(mal_id) 
        ON DELETE CASCADE,

    theme_mal_id INTEGER NOT NULL 
        REFERENCES theme(mal_id) 
        ON DELETE CASCADE,

    PRIMARY KEY (anime_mal_id, theme_mal_id)
);

CREATE TABLE IF NOT EXISTS anime_studio (
    anime_mal_id INTEGER NOT NULL 
        REFERENCES anime(mal_id) 
        ON DELETE CASCADE,

    studio_mal_id INTEGER NOT NULL 
        REFERENCES studio(mal_id) 
        ON DELETE CASCADE,

    PRIMARY KEY(anime_mal_id, studio_mal_id)
);