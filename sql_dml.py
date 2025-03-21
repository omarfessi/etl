date_table_insert = """
INSERT INTO date_dim (event_date, day, week, month, year, dayofweek)
VALUES (%s, %s, %s, %s, %s, %s)
ON CONFLICT (event_date) DO NOTHING """
