import cartpilot


def test_hello_returns_greeting():
    result = cartpilot.hello()
    assert result == "Hello from cartpilot!"
