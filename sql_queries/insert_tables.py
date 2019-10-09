insert_home_results = ("""
INSERT INTO
    home_results (
        hometeam,
        total_home_matches,
        home_wins,
        home_losses,
        draws,
        home_points,
        draw_points,
        goals_for_h,
        goals_against_h,
        season,
        division
    )
SELECT
    hometeam,
    COUNT(ftr) AS total_home_matches,
    COUNT(
        CASE
            WHEN ftr = 'H' THEN 1
        END
    ) AS home_win,
    COUNT(
        CASE
            WHEN ftr = 'A' THEN 1
        END
    ) AS home_loss,
    COUNT(
        CASE
            WHEN ftr = 'D' THEN 1
        END
    ) AS draw,
    SUM(
        CASE
            WHEN ftr = 'H' THEN 3
        END
    ) AS home_points,
    SUM(
        CASE
            WHEN ftr = 'D' THEN 1
        END
    ) AS draw_points,
    ROUND(SUM(fthg), 0) AS goals_for_h,
    ROUND(SUM(ftag), 0) AS goals_against_h,
    season,
    division
FROM
    staging_footy_matches
GROUP BY
    hometeam,
    season,
    division;
""")

insert_away_results = ("""
INSERT INTO
    away_results (
        awayteam,
        total_away_matches,
        away_wins,
        away_losses,
        draws,
        away_points,
        goals_for_a,
        goals_against_a,
        season,
        division
    )
SELECT
    awayteam,
    COUNT(ftr) AS total_away_matches,
    COUNT(
        CASE
            WHEN ftr = 'A' THEN 1
        END
    ) AS away_win,
    COUNT(
        CASE
            WHEN ftr = 'H' THEN 1
        END
    ) AS away_loss,
    COUNT(
        CASE
            WHEN ftr = 'D' THEN 1
        END
    ) AS draw,
    SUM(
        CASE
            WHEN ftr = 'A' THEN 3
        END
    ) AS away_points,
    round(SUM(ftag), 0) AS goals_for_a,
    ROUND(SUM(fthg), 0) AS goals_against_a,
    season,
    division
FROM
    staging_footy_matches
GROUP BY
    awayteam,
    season,
    division;
""")

insert_league_tables = ("""
INSERT INTO
    league_tables (
        club,
        matches_played,
        wins,
        draws,
        losses,
        goals_for,
        goals_against,
        goal_differential,
        points,
        season,
        division
    )
SELECT
    team,
    sum(matches) AS matches,
    SUM(wins) AS wins,
    SUM(draws) AS draws,
    SUM(losses) AS losses,
    SUM(gf) as goals_for,
    SUM(ga) as goals_against,
    (SUM(gf) - SUM(ga)) as goal_differential,
    (SUM(points) + SUM(draws)) as points,
    season,
    division
FROM
    (
        SELECT
            hometeam AS team,
            total_home_matches AS matches,
            home_wins AS wins,
            draws AS draws,
            home_losses AS losses,
            goals_for_h AS gf,
            goals_against_h as ga,
            home_points as points,
            season,
            division
        FROM
            home_results
        UNION ALL
        SELECT
            awayteam AS team,
            total_away_matches AS matches,
            away_wins AS wins,
            draws AS draws,
            away_losses AS losses,
            goals_for_a AS gf,
            goals_against_a as ga,
            away_points as points,
            season,
            division
        FROM
            away_results
    )
GROUP BY
    team,
    division,
    season;
""")

insert_queries = [insert_home_results, insert_away_results, insert_league_tables]