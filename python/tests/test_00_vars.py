import os

# Pre-flight check to ensure token list exists
def test_nacritan_tokens_exists():
    tokens = eval(os.environ['AUTH_TOKENS'])
    assert tokens

# Pre-flight check to ensure PyTest token is present
def test_nacritan_token_exists():
    tokens = eval(os.environ['AUTH_TOKENS'])
    assert 'PyTest' in tokens.values()
