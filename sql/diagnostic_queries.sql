-- =========================================================================
-- INDUSTRIAL LOGISTICS COMMAND CENTER - DIAGNOSTIC QUERIES
-- Target: GitHub Repository & LinkedIn Executive Insights (English)
-- =========================================================================

-- 1. Bottleneck Analysis by Distribution Center (CDs)
WITH cd_performance AS (
    SELECT 
        c.cd_name,
        c.area_m2,
        COUNT(f.transaction_id) AS total_shipments,
        SUM(CASE WHEN f.on_time_status = 0 THEN 1 ELSE 0 END) AS delayed_shipments,
        AVG(f.delay_hours) AS avg_delay_hours
    FROM fact_deliveries f
    JOIN dim_cd c ON f.cd_id = c.cd_id
    GROUP BY c.cd_name, c.area_m2
)
SELECT 
    cd_name,
    area_m2,
    total_shipments,
    delayed_shipments,
    ROUND((CAST(delayed_shipments AS FLOAT) / total_shipments) * 100, 2) AS delay_rate_pct,
    ROUND(avg_delay_hours, 2) AS avg_delay_hours
FROM cd_performance
ORDER BY delay_rate_pct DESC;

-- 2. Fleet Cost & Capacity Utilization Analysis (100 Trucks)
SELECT 
    v.vehicle_type,
    COUNT(DISTINCT v.vehicle_id) AS fleet_count,
    ROUND(AVG(f.estimated_freight_cost / NULLIF(f.distance_km, 0)), 2) AS avg_cost_per_km,
    ROUND(AVG(f.transported_weight_kg / v.max_weight_kg * 100), 2) AS avg_weight_capacity_utilization_pct
FROM fact_deliveries f
JOIN dim_fleet v ON f.vehicle_id = v.vehicle_id
GROUP BY v.vehicle_type
ORDER BY avg_cost_per_km DESC;