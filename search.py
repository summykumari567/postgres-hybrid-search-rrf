from app.embeddings import embed

def hybrid_search(conn, query: str, alpha=0.5, k=10):
    emb = embed(query)

    sql = """
    WITH semantic AS (
        SELECT id,
        1.0 / (ROW_NUMBER() OVER (ORDER BY embedding <=> %(emb)s)) AS rrf_sem
        FROM documents
        ORDER BY embedding <=> %(emb)s
        LIMIT 60
    ),
    lexical AS (
        SELECT id,
        1.0 / (ROW_NUMBER() OVER (ORDER BY ts_rank DESC)) AS rrf_lex
        FROM documents,
        plainto_tsquery('english', %(q)s) query
        WHERE tsv @@ query
        ORDER BY ts_rank DESC
        LIMIT 60
    )
    SELECT COALESCE(s.id, l.id) AS id,
           (%(a)s * COALESCE(rrf_sem, 0) +
           (1 - %(a)s) * COALESCE(rrf_lex, 0)) AS score
    FROM semantic s
    FULL OUTER JOIN lexical l USING(id)
    ORDER BY score DESC
    LIMIT %(k)s;
    """

    with conn.cursor() as cur:
        cur.execute(sql, {
            "emb": emb,
            "q": query,
            "a": alpha,
            "k": k
        })
        return cur.fetchall()