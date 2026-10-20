
import re

from rank_bm25 import BM25Okapi


def tokenize(text: str) -> list[str]:
    """Convert text into lowercase word tokens."""
    return re.findall(r"\w+", text.lower(), flags=re.UNICODE)


def search_document(document: str, question: str) -> list[str]:
    """Rank document sentences by relevance using BM25."""
    if not document.strip() or not question.strip():
        return []

    sentences = [
        sentence.strip()
        for sentence in re.split(r"[.!?]+", document)
        if sentence.strip()
    ]

    question_tokens = tokenize(question)
    tokenized_sentences = [tokenize(sentence) for sentence in sentences]

    if not question_tokens or not tokenized_sentences:
        return []

    # Avoid returning unrelated sentences when there are no shared words.
    query_terms = set(question_tokens)
    candidates = [
        index
        for index, tokens in enumerate(tokenized_sentences)
        if query_terms.intersection(tokens)
    ]

    if not candidates:
        return []

    bm25 = BM25Okapi(tokenized_sentences)
    scores = bm25.get_scores(question_tokens)

    ranked_indices = sorted(
        candidates,
        key=lambda index: scores[index],
        reverse=True,
    )

    return [sentences[index] for index in ranked_indices[:3]]