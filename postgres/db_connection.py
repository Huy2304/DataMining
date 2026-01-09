import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor, execute_values
from typing import Optional, List, Tuple, Any

class PostgreSQLConnection:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self, **kwargs: Any) -> bool:
        conn_params = {}

        try:
            conn_params['host'] = kwargs.get('host')
            conn_params['port'] = kwargs.get('port')
            conn_params['database'] = kwargs.get('database')
            conn_params['user'] = kwargs.get('user')
            conn_params['password'] = kwargs.get('password')

            self.connection = psycopg2.connect(**conn_params)
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            print(f"Successfully connected to database: {conn_params.get('database')} at {conn_params.get('host')}:{conn_params.get('port')}")
            return True
        except Exception as e:
            print(f"Failed to connect to database: {e}")
            return False

    def excute_query(self, query: str, params: Optional[Any] = None, fetch: bool = False) -> Optional[List[Tuple[bool, ...]]]:
        try:
            if params:
                self.cursor.execute(query, params)
                print(f"Executing parameterized query: {query[:50]}... with params: {params}")
            else:
                self.cursor.excute(query)
                print(f"Executing query: {query[:50]}...")

            if fetch:
                results = self.cursor.fetchall()
                print(f"Query executed successfully. Fetched {len(results)} rows.")
                return results
            else:
                self.connection.commit()
                print(f"Query executed successfully. Transaction committed.")

            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Query execution failed: {e}")
            return False

    def insert_many(self, table: str, columns: List[str], values: List[Tuple[Any, ...]]) -> Optional[int]:

        query = sql.SQL("INSERT INTO {} ({}) VALUES %s").format(
            sql.Identifier(table),
            sql.SQL(', ').join(map(sql.Identifier, columns))
        )

        try:
            execute_values(self.cursor, query, values)
            self.connection.commit()
            print(f"{self.cursor.rowcount} rows inserted")
            return self.cursor.rowcount
        except Exception as e:
            self.connection.rollback()
            print(f"Bulk Insert failed for {table}: {e}")

    def close(self) -> None:
        if self.cursor:
            self.cursor.close()
            print("Database cursor closed.")
        if self.connection:
            self.connection.close()
            print("Database connection closed.")

        print("PostgreSQL connection cleanup completed.")
