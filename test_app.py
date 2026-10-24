
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

    
def test_unrelated_question_does_not_call_model(monkeypatch):
    import rag

    def fail_if_called(*args, **kwargs):
        raise AssertionError("Mallia ei pitäisi kutsua ilman sopivia lähteitä")

    monkeypatch.setattr(rag, "OpenAI", fail_if_called)

    result = rag.answer_question(
        "Vuosilomaa haetaan henkilöstöjärjestelmässä.",
        "Miten haen avioeroa?",
    )

    assert result["sources"] == []
    assert "ei löytynyt" in result["answer"].lower()


def test_answer_question_uses_local_ollama(monkeypatch):
    import rag

    captured = {}

    class FakeResponse:
        output_text = "Vuosilomaa haetaan henkilöstöjärjestelmässä. [Lähde 1]"

    class FakeResponses:
        def create(self, **kwargs):
            captured.update(kwargs)
            return FakeResponse()

    class FakeClient:
        def __init__(self, **kwargs):
            captured["client"] = kwargs
            self.responses = FakeResponses()

    monkeypatch.setattr(rag, "OpenAI", FakeClient)

    document = "Vuosilomaa haetaan henkilöstöjärjestelmässä."
    result = rag.answer_question(document, "Miten vuosilomaa haetaan?")

    assert result["answer"] == FakeResponse.output_text
    assert result["sources"]
    assert captured["client"]["base_url"] == "http://localhost:11434/v1"
    assert captured["model"] == "qwen3:8b"


def test_question_word_alone_does_not_match():
    document = "Miten työasema lukitaan työpisteeltä poistuttaessa."

    result = search_document(
        document,
        "Miten haen avioeroa?",
    )

    assert result == []


def test_search_prioritizes_relevant_sentence():
    document = (
        "Työasema lukitaan työpisteeltä poistuttaessa. "
        "Sairauspoissaolosta ilmoitetaan esihenkilölle. "
        "Työhuone pidetään siistinä."
    )

    result = search_document(
        document,
        "Kenelle sairauspoissaolosta ilmoitetaan?",
    )

    assert result
    assert "sairauspoissaolosta" in result[0].lower()

def test_normalize_tokens_handles_finnish_inflection():
    from search import normalize_tokens

    query_tokens = normalize_tokens("vuosilomaa")
    document_tokens = normalize_tokens("vuosiloman")

    assert set(query_tokens) & set(document_tokens)

    
def test_unrelated_question_returns_no_results_after_normalization():
    document = "Vuosilomaa haetaan henkilöstöjärjestelmässä."

    result = search_document(
        document,
        "Miten haen avioeroa?",
    )

    assert result == []


from rag import validate_citations


def test_valid_citations_are_accepted():
    answer = "Lomaa haetaan järjestelmässä. [Lähde 1]"
    assert validate_citations(answer, 1)


def test_nonexistent_citation_is_rejected():
    answer = "Lomaa haetaan järjestelmässä. [Lähde 3]"
    assert not validate_citations(answer, 1)


def test_answer_without_citations_is_rejected():
    answer = "Lomaa haetaan järjestelmässä."
    assert not validate_citations(answer, 1)


def test_invalid_citation_is_rejected():
    from rag import validate_citations

    assert not validate_citations(
        "Lomaa haetaan järjestelmässä. [Lähde 2]",
        1,
    )


def test_multiple_valid_citations_are_accepted():
    from rag import validate_citations

    answer = "Lomaa haetaan järjestelmässä [Lähde 1]. Poissaolosta ilmoitetaan [Lähde 2]."

    assert validate_citations(answer, 2)

