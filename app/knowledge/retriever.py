"""
Knowledge Retriever

Hybrid Retriever
"""

from app.knowledge.embedding import get_embedding
from app.knowledge.hybrid import hybrid_search


def retrieve(
    question: str,
    top_k: int = 5
):
    """
    Hybrid Retrieval
    """

    embedding = get_embedding(question)

    return hybrid_search(
        question=question,
        embedding=embedding,
        top_k=top_k
    )


def retrieve_by_embedding(
    embedding: list[float],
    question: str,
    top_k: int = 5
):
    """
    已有Embedding直接Hybrid检索
    """

    return hybrid_search(
        question=question,
        embedding=embedding,
        top_k=top_k
    )


def retrieve_context(
    question: str,
    top_k: int = 5
):
    """
    返回Context
    """

    docs = retrieve(
        question,
        top_k
    )

    if not docs:

        return ""

    texts = []

    seen = set()

    for item in docs:

        text = item["text"].strip()

        if text in seen:

            continue

        seen.add(text)

        texts.append(text)

    return "\n\n".join(texts)


def retrieve_context_by_embedding(
    embedding: list[float],
    question: str,
    top_k: int = 5
):
    """
    已有Embedding直接Hybrid检索
    """

    docs = retrieve_by_embedding(
        embedding=embedding,
        question=question,
        top_k=top_k
    )

    if not docs:

        return ""

    texts = []

    seen = set()

    for item in docs:

        text = item["text"].strip()

        if text in seen:

            continue

        seen.add(text)

        texts.append(text)

    return "\n\n".join(texts)


if __name__ == "__main__":

    print("=" * 60)

    print(

        retrieve_context(

            "谁熟悉Python开发？"

        )

    )

    print("=" * 60)