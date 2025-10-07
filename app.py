import psycopg2
import pandas as pd

# ------------------------------
# Настройки подключения к базе
# ------------------------------
DB_SETTINGS = {
    "dbname": "nba_db",
    "user": "anuar21",
    "password": "",   # ← замени на свой пароль
    "host": "localhost",
    "port": "5432"
}

# ------------------------------
# SQL-запросы для аналитики
# ------------------------------
QUERIES = {
    "avg_points_per_game": """
        SELECT 
          p."PLAYER_NAME",
          ROUND(AVG(COALESCE(gd."PTS", 0))::numeric, 2) AS avg_points_per_game
        FROM games_details gd
        JOIN players p ON gd."PLAYER_ID" = p."PLAYER_ID"
        GROUP BY p."PLAYER_NAME"
        HAVING COUNT(*) >= 5
        ORDER BY avg_points_per_game DESC
        LIMIT 10;
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
        LIMIT 10;
    """,

    "avg_3pt_per_game": """
        SELECT
          p."PLAYER_NAME",
          ROUND(AVG(COALESCE(gd."FG3M", 0))::numeric, 2) AS avg_3pm_per_game
        FROM games_details gd
        JOIN players p ON gd."PLAYER_ID" = p."PLAYER_ID"
        GROUP BY p."PLAYER_NAME"
        HAVING COUNT(*) >= 5
        ORDER BY avg_3pm_per_game DESC
        LIMIT 10;
    """,

    "avg_ft_percentage": """
        SELECT
          p."PLAYER_NAME",
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
        LIMIT 10;
    """
}


# ------------------------------
# Основная функция
# ------------------------------
def run_queries():
    try:
        conn = psycopg2.connect(**DB_SETTINGS)
        print("✅ Connected to PostgreSQL database successfully!\n")

        for name, query in QUERIES.items():
            print(f"▶ Executing: {name}")
            df = pd.read_sql_query(query, conn)
            print(df)
            df.to_csv(f"{name}.csv", index=False)
            print(f"💾 Results saved to {name}.csv\n")

    except Exception as e:
        print("❌ Error:", e)
    finally:
        if 'conn' in locals():
            conn.close()
            print("🔒 Connection closed.")


if __name__ == "__main__":
    run_queries()
