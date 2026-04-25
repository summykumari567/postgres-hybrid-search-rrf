from app.db import get_connection
from app.search import hybrid_search

if __name__ == "__main__":
    conn = get_connection()

    query = "machine learning models"
    results = hybrid_search(conn, query)

    for r in results:
        print(r)

    conn.close()