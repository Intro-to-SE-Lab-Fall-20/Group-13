def test_empty_db():
    """Start with a blank database."""

    assert b'No entries here so far' in rv.data