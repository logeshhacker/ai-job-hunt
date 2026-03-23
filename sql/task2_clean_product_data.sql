-- Task 2: Clean product data for analysis
-- Returns cleaned product data without modifying the original table.
--
-- Column criteria applied:
--   product_id         : No missing values (enforced by DB structure)
--   product_type       : Missing values replaced with 'Unknown'
--   brand              : Missing values replaced with 'Unknown'
--   weight             : Missing values replaced with overall median weight (positive, rounded to 2 dp)
--   price              : Missing values replaced with overall median price  (positive, rounded to 2 dp)
--   average_units_sold : Missing values replaced with 0
--   year_added         : Missing values replaced with 2022
--   stock_location     : Missing values replaced with 'Unknown'

WITH medians AS (
    SELECT
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY weight) AS median_weight,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY price)  AS median_price
    FROM products
)
SELECT
    p.product_id,

    COALESCE(p.product_type, 'Unknown')                                AS product_type,

    COALESCE(p.brand, 'Unknown')                                       AS brand,

    ROUND(COALESCE(p.weight, m.median_weight)::NUMERIC, 2)             AS weight,

    ROUND(COALESCE(p.price,  m.median_price)::NUMERIC,  2)             AS price,

    COALESCE(p.average_units_sold, 0)                                  AS average_units_sold,

    COALESCE(p.year_added, 2022)                                       AS year_added,

    COALESCE(p.stock_location, 'Unknown')                              AS stock_location

FROM products p
CROSS JOIN medians m;
