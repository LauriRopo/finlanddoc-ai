
from search import search_document


def test_finds_matching_sentence():
    document = "Lomaa haetaan henkilöstöjärjestelmässä."

    result = search_document(document, "Miten lomaa haetaan?")

    assert len(result) == 1
    assert "lomaa" in result[0].lower()


def test_empty_document_returns_no_results():
    assert search_document("", "lomaa") == []


def test_unrelated_question_returns_no_results():
    document = "Tietokone lukitaan työpisteeltä poistuttaessa."

    assert search_document(document, "Miten lomaa haetaan?") == []