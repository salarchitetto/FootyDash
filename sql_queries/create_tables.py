staging_table_create= ("""
CREATE TABLE IF NOT EXISTS footy_matches (
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
    copy footy_matches {} from 's3://footydashdata/{}'
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

create_table_queries = [staging_table_create]
drop_table_queries = ['DROP TABLE IF EXISTS footy_matches']