"""
Ultra-simple syntax validation tests
"""
import ast
import os


def test_python_syntax_bot():
    """Test that bot.py has valid Python syntax"""
    try:
        with open('bot.py', 'r', encoding='utf-8') as f:
            code = f.read()
        ast.parse(code)
        assert True  # Syntax is valid
    except Exception as e:
        print(f"Syntax error in bot.py: {e}")
        assert False, f"bot.py has syntax errors: {e}"


def test_python_syntax_ai_features():
    """Test that ai_features.py has valid Python syntax"""
    try:
        with open('ai_features.py', 'r', encoding='utf-8') as f:
            code = f.read()
        ast.parse(code)
        assert True  # Syntax is valid
    except Exception as e:
        print(f"Syntax error in ai_features.py: {e}")
        assert False, f"ai_features.py has syntax errors: {e}"


def test_python_syntax_cli():
    """Test that cli.py has valid Python syntax"""
    try:
        with open('cli.py', 'r', encoding='utf-8') as f:
            code = f.read()
        ast.parse(code)
        assert True  # Syntax is valid
    except Exception as e:
        print(f"Syntax error in cli.py: {e}")
        assert False, f"cli.py has syntax errors: {e}"


def test_config_json_valid():
    """Test that config.json is valid JSON"""
    import json
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            json.load(f)
        assert True  # JSON is valid
    except Exception as e:
        print(f"Invalid JSON in config.json: {e}")
        assert False, f"config.json is not valid JSON: {e}"


if __name__ == "__main__":
    # Run all syntax tests
    test_python_syntax_bot()
    test_python_syntax_ai_features()
    test_python_syntax_cli()
    test_config_json_valid()
    print("All syntax validation tests passed!")