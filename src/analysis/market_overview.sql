
SELECT
    CASE
        WHEN is_free THEN 'Free'
        ELSE 'Paid'
    END AS game_type,

    COUNT(*) AS game_count,

    ROUND(
        AVG(total_positive + total_negative),
        2
    ) AS avg_review_count,

    ROUND(
        100.0 * SUM(total_positive)
        / NULLIF(
            SUM(total_positive + total_negative),
            0
        ),
        2
    ) AS positive_review_rate

FROM games_index

GROUP BY is_free
ORDER BY game_count DESC;
