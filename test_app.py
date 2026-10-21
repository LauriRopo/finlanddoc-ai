
from search import search_document, tokenize


def test_finds_matching_sentence():
    document = (
        "Lomaa haetaan henkilöstöjärjestelmässä. "
        "Sairauspoissaolosta ilmoitetaan esihenkilölle."
    )

    result = search_document(document, "Miten lomaa haetaan?")

    assert result
    assert any("lomaa" in sentence.lower() for sentence in result)


def test_empty_document_returns_no_results():
    assert search_document("", "lomaa") == []


def test_empty_question_returns_no_results():
    assert search_document("Lomaa haetaan järjestelmässä.", "") == []


def test_unrelated_question_returns_no_results():
    document = "Tietokone lukitaan työpisteeltä poistuttaessa."

    assert search_document(document, "Miten lomaa haetaan?") == []


def test_search_returns_at_most_three_results():
    document = (
        "Lomaa haetaan järjestelmässä. "
        "Lomaa suunnitellaan etukäteen. "
        "Lomaa koskevat ohjeet löytyvät intranetistä. "
        "Lomapäivistä sovitaan esihenkilön kanssa."
    )

    result = search_document(document, "lomaa")

    assert len(result) <= 3
    assert len(result) > 0


def test_tokenize_handles_finnish_text_and_punctuation():
    assert tokenize("Lomaa haetaan, järjestelmässä!") == [
        "lomaa",
        "haetaan",
        "järjestelmässä",
    ]

from rag import answer_question


def test_answer_question_returns_source():
    document = (
        "Vuosilomaa haetaan henkilöstöjärjestelmässä. "
        "Sairauspoissaolosta ilmoitetaan esihenkilölle."
    )

    result = answer_question(document, "Miten vuosilomaa haetaan?")

    assert result["sources"]
    assert any(
        "vuosilomaa" in source.lower()
        for source in result["sources"]
    )


def test_unrelated_question_returns_no_answer():
    document = (
        "Vuosilomaa haetaan henkilöstöjärjestelmässä."
    )

    result = answer_question(document, "Miten haen avioeroa?")

    assert result["sources"] == []
    assert "ei löytynyt" in result["answer"].lower()