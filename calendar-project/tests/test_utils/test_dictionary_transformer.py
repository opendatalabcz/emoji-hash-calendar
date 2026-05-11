from app.utilities.emoji_transformers.dictionary_transformer import DictionaryTransformer


def test_single_word_match():
    transformer = DictionaryTransformer({"hello": "👋"})
    assert transformer.transform("hello") == ["👋"]


def test_case_insensitive_match():
    transformer = DictionaryTransformer({"hello": "👋"})
    assert transformer.transform("HeLLo") == ["👋"]


def test_stemming_match():
    transformer = DictionaryTransformer({"run": "🏃"})
    assert transformer.transform("running fast") == ["🏃"]


def test_bigram_match_preferred_over_single():
    transformer = DictionaryTransformer({
        "new york": "🗽",
        "new": "🆕"
    })
    assert transformer.transform("I love New York city") == ["🗽"]


def test_trigram_match_preferred_over_bigram_and_single():
    transformer = DictionaryTransformer({
        "new york city": "🌆",
        "new york": "🗽",
        "city": "🏙️"
    })
    assert transformer.transform("Welcome to New York City") == ["🌆"]


def test_overlapping_phrases_do_not_repeat():
    transformer = DictionaryTransformer({
        "new york": "🗽",
        "york city": "🏙️"
    })
    assert transformer.transform("New York City") == ["🗽"]


def test_multiple_non_overlapping_matches():
    transformer = DictionaryTransformer({
        "new york": "🗽",
        "pizza": "🍕"
    })
    assert transformer.transform("New York has great pizza") == ["🗽", "🍕"]


def test_apostrophes_are_removed():
    transformer = DictionaryTransformer({"dont": "🚫"})
    assert transformer.transform("don't do that") == ["🚫"]


def test_no_matches_returns_empty_list():
    transformer = DictionaryTransformer({"hello": "👋"})
    assert transformer.transform("nothing here") == []
