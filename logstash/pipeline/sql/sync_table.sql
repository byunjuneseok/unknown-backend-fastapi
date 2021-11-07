SELECT *, update_date_time AS ts FROM agd.store
WHERE update_date_time > :sql_last_value AND update_date_time < NOW()
ORDER BY id