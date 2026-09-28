from typing import Annotated
import asyncpg
from fastapi import APIRouter, Depends, Query
from pgvector import Vector
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/vectors", tags=["Vector Search"])

class CustomerVectorResult(BaseModel):
    customer_id: str
    cosine_similarity: float
    metadata: dict

async def search_customers_by_embedding(
    conn: asyncpg.Connection,
    embedding: list[float],
    limit: int = 10,
    min_similarity: float = 0.70
) -> list[CustomerVectorResult]:
    vec = Vector(embedding)
    sql = """
        SELECT 
            customer_id,
            metadata,
            1 - (features_vector <=> $1) AS cosine_similarity
        FROM customer_embeddings
        WHERE 1 - (features_vector <=> $1) >= $2
        ORDER BY features_vector <=> $1 ASC
        LIMIT $3;
    """
    rows = await conn.fetch(sql, vec, min_similarity, limit)
    return [
        CustomerVectorResult(
            customer_id=r["customer_id"],
            cosine_similarity=round(float(r["cosine_similarity"]), 4),
            metadata=r["metadata"] or {}
        )
        for r in rows
    ]
