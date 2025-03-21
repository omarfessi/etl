date_dim_create = """
CREATE TABLE IF NOT EXISTS date_dim(
								event_date date PRIMARY KEY,
								day int ,
								week int,
								month int,
								year int,
								dayofweek int)"""

tables_creation_queries = [date_dim_create]
