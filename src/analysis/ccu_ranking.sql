
SELECT
    c.app_id,
    g.name,
    COUNT(*) AS observed_days,
    MAX(c.max_players) AS peak_ccu,
    ROUND(AVG(c.max_players), 2) AS avg_daily_peak_ccu
FROM ccu_daily AS c
LEFT JOIN games_index AS g
    ON c.app_id = g.app_id
GROUP BY c.app_id, g.name
ORDER BY peak_ccu DESC, c.app_id
LIMIT 10;
