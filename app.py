import pandas as pd
from sqlalchemy import create_engine

# ==========================================================
# Подключение к базе данных
# ==========================================================
DB_USER = "anuar21"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "nba_db"
DB_PASS = ""  

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# ==========================================================
# SQL-запросы (10 аналитических запросов)
# ==========================================================
queries = {
    "avg_points_per_game": """
        SELECT
          p."PLAYER_NAME",
          ROUND(AVG(COALESCE(gd."PTS", 0))::numeric, 2) AS avg_points_per_game
        FROM games_details gd
        JOIN players p ON gd."PLAYER_ID" = p."PLAYER_ID"
        GROUP BY p."PLAYER_NAME"
        HAVING COUNT(*) >= 5
        ORDER BY avg_points_per_game DESC
        LIMIT 20;
    """,

    "avg_assists_per_game": """
        SELECT
          p."PLAYER_NAME",
          ROUND(AVG(COALESCE(gd."AST", 0))::numeric, 2) AS avg_assists_per_game
        FROM games_details gd
        JOIN players p ON gd."PLAYER_ID" = p."PLAYER_ID"
        GROUP BY p."PLAYER_NAME"
        HAVING COUNT(*) >= 5
        ORDER BY avg_assists_per_game DESC
        LIMIT 20;
    """,

    "avg_rebounds_per_game": """
        SELECT
          p."PLAYER_NAME",
          ROUND(AVG(COALESCE(gd."REB", 0))::numeric, 2) AS avg_rebounds_per_game
        FROM games_details gd
        JOIN players p ON gd."PLAYER_ID" = p."PLAYER_ID"
        GROUP BY p."PLAYER_NAME"
        HAVING COUNT(*) >= 5
        ORDER BY avg_rebounds_per_game DESC
        LIMIT 20;
    """,

    "avg_blocks_per_game": """
        SELECT
          p."PLAYER_NAME",
          ROUND(AVG(COALESCE(gd."BLK", 0))::numeric, 2) AS avg_blocks_per_game
        FROM games_details gd
        JOIN players p ON gd."PLAYER_ID" = p."PLAYER_ID"
        GROUP BY p."PLAYER_NAME"
        HAVING COUNT(*) >= 5
        ORDER BY avg_blocks_per_game DESC
        LIMIT 20;
    """,

    "avg_steals_per_game": """
        SELECT
          p."PLAYER_NAME",
          ROUND(AVG(COALESCE(gd."STL", 0))::numeric, 2) AS avg_steals_per_game
        FROM games_details gd
        JOIN players p ON gd."PLAYER_ID" = p."PLAYER_ID"
        GROUP BY p."PLAYER_NAME"
        HAVING COUNT(*) >= 5
        ORDER BY avg_steals_per_game DESC
        LIMIT 20;
    """,

    "avg_3pm_per_game": """
        SELECT
          p."PLAYER_NAME",
          SUM(COALESCE(gd."FG3M", 0)) AS total_3pm,
          COUNT(*) AS games_played,
          ROUND(AVG(COALESCE(gd."FG3M", 0))::numeric, 2) AS avg_3pm_per_game
        FROM games_details gd
        JOIN players p ON gd."PLAYER_ID" = p."PLAYER_ID"
        GROUP BY p."PLAYER_NAME"
        HAVING COUNT(*) >= 5
        ORDER BY avg_3pm_per_game DESC
        LIMIT 20;
    """,

    "avg_fg_percentage": """
        SELECT
          p."PLAYER_NAME",
          ROUND(AVG(COALESCE(gd."FG_PCT", 0))::numeric * 100, 2) AS avg_fg_percentage
        FROM games_details gd
        JOIN players p ON gd."PLAYER_ID" = p."PLAYER_ID"
        GROUP BY p."PLAYER_NAME"
        ORDER BY avg_fg_percentage DESC
        LIMIT 20;
    """,

    "avg_plus_minus": """
        SELECT
          p."PLAYER_NAME",
          ROUND(AVG(COALESCE(gd."PLUS_MINUS", 0))::numeric, 2) AS avg_plus_minus
        FROM games_details gd
        JOIN players p ON gd."PLAYER_ID" = p."PLAYER_ID"
        GROUP BY p."PLAYER_NAME"
        ORDER BY avg_plus_minus DESC
        LIMIT 20;
    """,

    "avg_team_points": """
        SELECT
          gd."TEAM_ABBREVIATION",
          ROUND(AVG(COALESCE(gd."PTS", 0))::numeric, 2) AS avg_team_points
        FROM games_details gd
        GROUP BY gd."TEAM_ABBREVIATION"
        ORDER BY avg_team_points DESC
        LIMIT 20;
    """,

    "ft_percentage": """
        SELECT
          p."PLAYER_NAME",
          SUM(COALESCE(gd."FTM", 0)) AS total_ft_made,
          SUM(COALESCE(gd."FTA", 0)) AS total_ft_attempted,
          ROUND(
            CASE WHEN SUM(COALESCE(gd."FTA", 0)) > 0
                 THEN (SUM(COALESCE(gd."FTM", 0))::numeric / SUM(COALESCE(gd."FTA", 0))) * 100
                 ELSE 0 END, 2
          ) AS ft_percentage
        FROM games_details gd
        JOIN players p ON gd."PLAYER_ID" = p."PLAYER_ID"
        GROUP BY p."PLAYER_NAME"
        HAVING SUM(COALESCE(gd."FTA", 0)) >= 10
        ORDER BY ft_percentage DESC
        LIMIT 20;
    """
}

# ==========================================================
# Выполнение запросов и вывод результатов
# ==========================================================
def run_queries():
    print("🏀 DataHoop Analytics — NBA SQL Insights\n")
    with engine.connect() as conn:
        for name, query in queries.items():
            print(f"▶ Запрос: {name}")
            df = pd.read_sql(query, conn)
            print(df)
            print("-" * 60)

    print("\n✅ Все 10 запросов успешно выполнены!")

# ==========================================================
# Точка входа
# ==========================================================
if __name__ == "__main__":
    run_queries()
