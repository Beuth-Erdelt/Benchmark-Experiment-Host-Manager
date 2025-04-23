SELECT 
    schemaname || '.' || relname AS table_name,
    pg_size_pretty(pg_relation_size(schemaname || '.' || relname)) AS table_size,
    pg_size_pretty(pg_indexes_size(schemaname || '.' || relname)) AS index_size,
    pg_size_pretty(pg_total_relation_size(schemaname || '.' || relname)) AS total_size
FROM 
    pg_stat_user_tables
ORDER BY 
    pg_total_relation_size(schemaname || '.' || relname) DESC;
