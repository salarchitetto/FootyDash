staging_table_create= ("""
CREATE TABLE IF NOT EXISTS staging_footy_matches (
    date VARCHAR(20) NOT NULL,
    hometeam VARCHAR(50) NOT NULL,
    awayteam VARCHAR(50) NOT NULL,
    fthg DECIMAL(12,2) NULL,
    ftag DECIMAL(12,2) NULL,
    ftr VARCHAR(3) NULL,
    hthg DECIMAL(12,2) NULL,
    htag DECIMAL NULL,
    htr VARCHAR(3) NULL,
    hs DECIMAL(12,2) NULL,
    aas DECIMAL(12,2) NULL,
    hst DECIMAL(12,2) NULL,
    ast DECIMAL(12,2) NULL,
    hfkc DECIMAL(12,2) NULL,
    afkc DECIMAL(12,2) NULL,
    hf DECIMAL(12,2) NULL,
    af DECIMAL(12,2) NULL,
    hc DECIMAL(12,2) NULL,
    ac DECIMAL(12,2) NULL,
    hy DECIMAL(12,2) NULL,
    ay DECIMAL(12,2) NULL,
    hr DECIMAL(12,2) NULL,
    ar DECIMAL(12,2) NULL,
    season VARCHAR(50),
    division VARCHAR(100))
""")

staging_copy = ("""
    copy staging_footy_matches {} from 's3://footydashdata/{}'
    credentials 'aws_iam_role={}'
    region 'us-east-1'
    compupdate off
    DELIMITER ','
    dateformat 'auto'
    FILLRECORD
    TIMEFORMAT 'auto'
    IGNOREHEADER 1
    removequotes
""")

home_results = ("""
CREATE TABLE IF NOT EXISTS home_results (
    hometeam VARCHAR NOT NULL,
    total_home_matches INT NOT NULL,
    home_wins INT NOT NULL,
    home_losses INT NOT NULL,
    draws INT NOT NULL,
    home_points INT NULL,
    draw_points INT NULL,
    goals_for_h INT NULL,
    goals_against_h INT NULL,
    season VARCHAR NOT NULL,
    division VARCHAR NOT NULL
);
""")

away_results = ("""
CREATE TABLE IF NOT EXISTS away_results (
    awayteam VARCHAR NOT NULL,
    total_away_matches INT NOT NULL,
    away_wins INT NOT NULL,
    away_losses INT NOT NULL,
    draws INT NOT NULL,
    away_points INT NULL,
    goals_for_a INT NULL,
    goals_against_a INT NULL,
    season VARCHAR NOT NULL,
    division VARCHAR NOT NULL
);
""")

create_league_table = ("""
CREATE TABLE league_tables (
    club VARCHAR NOT NULL,
    matches_played INT NOT NULL,
    wins INT NOT NULL,
    draws INT NOT NULL,
    losses INT NOT NULL,
    goals_for INT NOT NULL,
    goals_against INT NOT NULL,
    goal_differential INT NOT NULL,
    points INT NULL,
    season VARCHAR NOT NULL,
    division VARCHAR NOT NULL
);
""")

drop_staging = "DROP TABLE IF EXISTS staging_footy_matches"
drop_home = "DROP TABLE IF EXISTS home_results;"
drop_away = "DROP TABLE IF EXISTS away_results;"
drop_league = "DROP TABLE IF EXISTS league_tables;"

create_table_queries = [staging_table_create, home_results, away_results, create_league_table]
drop_table_queries = [drop_staging, drop_home, drop_away, drop_league]