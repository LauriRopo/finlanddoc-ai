
import re

from rank_bm25 import BM25Okapi

import spacy

nlp = spacy.load("fi_core_news_sm")


def normalize_tokens(text: str) -> list[str]:
    """Convert Finnish words to their base forms."""
    doc = nlp(text.lower())
    return [
        token.lemma_.lower()
        for token in doc
        if not token.is_space and not token.is_punct
    ]


STOP_WORDS = {
    "miten",
    "mikä",
    "mitä",
    "miksi",
    "milloin",
    "missä",
    "mistä",
    "minne",
    "kuka",
    "kenen",
    "kenelle",
    "onko",
    "voiko",
    "hakea",
}


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

    question_tokens = [
    token
    for token in normalize_tokens(question)
    if token not in STOP_WORDS
]

    tokenized_sentences = [
    normalize_tokens(sentence)
    for sentence in sentences
]

    if not question_tokens or not tokenized_sentences:
        return []

    
    query_terms = set(question_tokens)

    candidates = []

    for index, tokens in enumerate(tokenized_sentences):
        sentence_terms = set(tokens)
        matched_terms = query_terms.intersection(sentence_terms)

        # Require at least one meaningful term to match.
        if matched_terms:
            candidates.append(index)

    if not candidates:
        return []

    if not candidates:
        return []

    bm25 = BM25Okapi(tokenized_sentences)
    scores = bm25.get_scores(question_tokens)

    ranked_indices = sorted(
        candidates,
        key=lambda index: scores[index],
        reverse=True,
    )

    return [
        sentences[index]
        for index in ranked_indices[:3]
    ]
