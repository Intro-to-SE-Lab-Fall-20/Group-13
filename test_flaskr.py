def test_empty_db():
    """Start with a blank database."""

    rv = client.get('/')
    assert b'No entries here so far' in rv.data