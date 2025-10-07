-- 1. Среднее количество очков за игру по игрокам
-- Показывает топ-20 игроков с наибольшим средним количеством очков за матч.
SELECT
  p."PLAYER_NAME",
  ROUND(AVG(COALESCE(gd."PTS", 0))::numeric, 2) AS avg_points_per_game
FROM games_details gd
JOIN players p ON gd."PLAYER_ID" = p."PLAYER_ID"
GROUP BY p."PLAYER_NAME"
HAVING COUNT(*) >= 5
ORDER BY avg_points_per_game DESC
LIMIT 20;

-- 2. Среднее количество передач (ассистов) по игрокам
-- Топ-20 игроков по среднему числу ассистов за матч.
SELECT
  p."PLAYER_NAME",
  ROUND(AVG(COALESCE(gd."AST", 0))::numeric, 2) AS avg_assists_per_game
FROM games_details gd
JOIN players p ON gd."PLAYER_ID" = p."PLAYER_ID"
GROUP BY p."PLAYER_NAME"
HAVING COUNT(*) >= 5
ORDER BY avg_assists_per_game DESC
LIMIT 20;

-- 3. Среднее количество подборов (REB) за игру
-- Топ-20 игроков с наибольшим средним количеством подборов.
SELECT
  p."PLAYER_NAME",
  ROUND(AVG(COALESCE(gd."REB", 0))::numeric, 2) AS avg_rebounds_per_game
FROM games_details gd
JOIN players p ON gd."PLAYER_ID" = p."PLAYER_ID"
GROUP BY p."PLAYER_NAME"
HAVING COUNT(*) >= 5
ORDER BY avg_rebounds_per_game DESC
LIMIT 20;

-- 4. Среднее количество блок-шотов (BLK)
-- Определяет лучших блокирующих игроков.
SELECT
  p."PLAYER_NAME",
  ROUND(AVG(COALESCE(gd."BLK", 0))::numeric, 2) AS avg_blocks_per_game
FROM games_details gd
JOIN players p ON gd."PLAYER_ID" = p."PLAYER_ID"
GROUP BY p."PLAYER_NAME"
HAVING COUNT(*) >= 5
ORDER BY avg_blocks_per_game DESC
LIMIT 20;

-- 5. Среднее количество перехватов (STL)
-- Топ-20 игроков по среднему числу перехватов.
SELECT
  p."PLAYER_NAME",
  ROUND(AVG(COALESCE(gd."STL", 0))::numeric, 2) AS avg_steals_per_game
FROM games_details gd
JOIN players p ON gd."PLAYER_ID" = p."PLAYER_ID"
GROUP BY p."PLAYER_NAME"
HAVING COUNT(*) >= 5
ORDER BY avg_steals_per_game DESC
LIMIT 20;

-- 6. Среднее количество 3-очковых попаданий за игру
-- Лидеры по эффективности 3-очковых бросков.
SELECT
  p."PLAYER_ID",
  p."PLAYER_NAME",
  SUM(COALESCE(gd."FG3M", 0)) AS total_3pm,
  COUNT(*) AS games_played,
  ROUND(AVG(COALESCE(gd."FG3M", 0))::numeric, 2) AS avg_3pm_per_game
FROM games_details gd
JOIN players p ON gd."PLAYER_ID" = p."PLAYER_ID"
GROUP BY p."PLAYER_ID", p."PLAYER_NAME"
HAVING COUNT(*) >= 5
ORDER BY avg_3pm_per_game DESC
LIMIT 20;

-- 7. Средний процент попадания с игры (FG_PCT)
-- Рассчитывает средний процент точности бросков по игрокам.
SELECT
  p."PLAYER_NAME",
  ROUND(AVG(COALESCE(gd."FG_PCT", 0))::numeric * 100, 2) AS avg_fg_percentage
FROM games_details gd
JOIN players p ON gd."PLAYER_ID" = p."PLAYER_ID"
GROUP BY p."PLAYER_NAME"
ORDER BY avg_fg_percentage DESC
LIMIT 20;

-- 8. Средний показатель +/- по игрокам
-- Определяет вклад игрока в разницу очков, когда он на площадке.
SELECT
  p."PLAYER_NAME",
  ROUND(AVG(COALESCE(gd."PLUS_MINUS", 0))::numeric, 2) AS avg_plus_minus
FROM games_details gd
JOIN players p ON gd."PLAYER_ID" = p."PLAYER_ID"
GROUP BY p."PLAYER_NAME"
ORDER BY avg_plus_minus DESC
LIMIT 20;

-- 9. Команды с наибольшим средним количеством очков за игру
-- Анализирует среднюю результативность команд.
SELECT
  gd."TEAM_ABBREVIATION",
  ROUND(AVG(COALESCE(gd."PTS", 0))::numeric, 2) AS avg_team_points
FROM games_details gd
GROUP BY gd."TEAM_ABBREVIATION"
ORDER BY avg_team_points DESC
LIMIT 20;

-- 10. Эффективность штрафных бросков по игрокам
-- Рассчитывает процент реализации штрафных (FTM/FTA).
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
