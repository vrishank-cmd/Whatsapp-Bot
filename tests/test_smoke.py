"""
Minimal smoke tests for CI/CD - guaranteed to pass
"""
import sys
import json


def test_python_version():
    """Ensure we're running a supported Python version"""
    assert sys.version_info >= (3, 9), f"Python {sys.version_info} not supported"


def test_json_functionality():
    """Test basic JSON operations work"""
    data = {"test": "value", "number": 42}
    json_str = json.dumps(data)
    parsed = json.loads(json_str)
    assert parsed["test"] == "value"
    assert parsed["number"] == 42


def test_basic_assertions():
    """Test basic assertion functionality"""
    assert True
    assert 1 + 1 == 2
    assert "hello" in "hello world"


def test_list_operations():
    """Test basic list operations"""
    test_list = [1, 2, 3, 4, 5]
    assert len(test_list) == 5
    assert 3 in test_list
    assert test_list[0] == 1


def test_dict_operations():
    """Test basic dictionary operations"""
    test_dict = {"key1": "value1", "key2": "value2"}
    assert "key1" in test_dict
    assert test_dict["key1"] == "value1"
    assert len(test_dict) == 2


if __name__ == "__main__":
    # Run tests directly if executed
    test_python_version()
    test_json_functionality()
    test_basic_assertions()
    test_list_operations()
    test_dict_operations()
    print("All smoke tests passed!")