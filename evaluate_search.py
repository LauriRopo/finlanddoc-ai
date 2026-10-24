
from search import search_document


CASES = [
    {
        "name": "Vuosiloman hakeminen",
        "document": (
            "Vuosilomaa haetaan henkilöstöjärjestelmässä. "
            "Sairauspoissaolosta ilmoitetaan esihenkilölle."
        ),
        "question": "Miten vuosilomaa haetaan?",
        "expected_match": True,
        "expected_term": "vuosilom",
    },
    {
        "name": "Sairauspoissaolosta ilmoittaminen",
        "document": (
            "Vuosilomaa haetaan henkilöstöjärjestelmässä. "
            "Sairauspoissaolosta ilmoitetaan esihenkilölle."
        ),
        "question": "Kenelle sairauspoissaolosta ilmoitetaan?",
        "expected_match": True,
        "expected_term": "sairauspoissaol",
    },
    {
        "name": "Asiaankuulumaton avioerokysymys",
        "document": "Vuosilomaa haetaan henkilöstöjärjestelmässä.",
        "question": "Miten haen avioeroa?",
        "expected_match": False,
        "expected_term": None,
    },
    {
        "name": "Asiaankuulumaton tietokonekysymys",
        "document": "Vuosilomaa haetaan henkilöstöjärjestelmässä.",
        "question": "Miten lukitsen työaseman?",
        "expected_match": False,
        "expected_term": None,
    },
    {
        "name": "Työaseman lukitseminen",
        "document": (
            "Työasema lukitaan työpisteeltä poistuttaessa. "
            "Vuosilomaa haetaan henkilöstöjärjestelmässä."
        ),
        "question": "Miten työasema lukitaan?",
        "expected_match": True,
        "expected_term": "työasema",
    },
    
    {
        "name": "Vuosiloman ajankohdasta sopiminen",
        "document": (
            "Vuosiloman ajankohdasta sovitaan esihenkilön kanssa. "
            "Sairauspoissaolosta ilmoitetaan esihenkilölle."
        ),
        "question": "Kenen kanssa loman ajankohdasta sovitaan?",
        "expected_match": True,
        "expected_term": "vuosiloman ajankohdasta",
    },
    {
        "name": "Puuttuva palkkatieto",
        "document": (
            "Vuosilomaa haetaan henkilöstöjärjestelmässä. "
            "Sairauspoissaolosta ilmoitetaan esihenkilölle."
        ),
        "question": "Paljonko lomarahaa maksetaan?",
        "expected_match": False,
        "expected_term": None,
    },
    {
        "name": "Puuttuva etätyöohje",
        "document": (
            "Työasema lukitaan työpisteeltä poistuttaessa. "
            "Vuosilomaa haetaan henkilöstöjärjestelmässä."
        ),
        "question": "Kuinka monta päivää viikossa saa tehdä etätöitä?",
        "expected_match": False,
        "expected_term": None,
    },

]


def evaluate() -> None:
    correct = 0

    for case in CASES:
        results = search_document(
            case["document"],
            case["question"],
        )

        if case["expected_match"]:
            passed = any(
                case["expected_term"] in result.lower()
                for result in results
            )
        else:
            passed = len(results) == 0

        correct += int(passed)

        status = "OK" if passed else "VIRHE"
        print(f"[{status}] {case['name']}")
        print(f"  Kysymys: {case['question']}")
        print(f"  Hakutulokset: {results}")

    total = len(CASES)
    print(f"\nTulos: {correct}/{total} ({correct / total:.0%})")


if __name__ == "__main__":
    evaluate()
