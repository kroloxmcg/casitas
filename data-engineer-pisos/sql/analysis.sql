-- Precio medio por distrito (Madrid)
SELECT
    district,
    count(*) AS listings,
    round(avg(price), 0) AS avg_price,
    round(avg(calculated_price_m2), 0) AS avg_price_m2,
    round(avg(size), 0) AS avg_size_m2,
    round(avg(rooms), 1) AS avg_rooms
FROM listings
WHERE municipality = 'Madrid'
GROUP BY district
ORDER BY avg_price_m2 DESC;

-- Distribución de precios por tipo de operación
SELECT
    operation,
    count(*) AS total,
    round(percentile_cont(0.25) WITHIN GROUP (ORDER BY price), 0) AS p25,
    round(percentile_cont(0.50) WITHIN GROUP (ORDER BY price), 0) AS median,
    round(percentile_cont(0.75) WITHIN GROUP (ORDER BY price), 0) AS p75,
    round(avg(price), 0) AS mean
FROM listings
GROUP BY operation;

-- Pisos con mejor relación precio/m² (outliers baratos)
SELECT
    property_code,
    address,
    district,
    neighborhood,
    price,
    size,
    rooms,
    calculated_price_m2,
    has_lift,
    floor
FROM listings
WHERE calculated_price_m2 IS NOT NULL
  AND size > 40
  AND rooms >= 2
ORDER BY calculated_price_m2 ASC
LIMIT 20;

-- Evolución IPV (para cruzar con datos de anuncios)
SELECT
    category,
    period,
    value
FROM ipv
ORDER BY category, period;
