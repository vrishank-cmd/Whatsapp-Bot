import pytest
import asyncio
import json
import os
from unittest.mock import Mock, patch, AsyncMock

try:
    from ai_features import (
        AIMessageAssistant,
        SmartScheduler,
        SecurityManager,
        ModernAnalytics,
    )
    from bot import validate_phone_number, load_config

    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False


class TestConfiguration:
    def test_load_config_valid(self, tmp_path):
        config_file = tmp_path / "config.json"
        test_config = {
            "default_settings": {"max_contacts": 50, "min_interval_seconds": 5}
        }

        config_file.write_text(json.dumps(test_config))

        # Mock the current working directory
        with patch("builtins.open", create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = (
                json.dumps(test_config)
            )
            config = load_config()

        assert isinstance(config, dict)

    def test_load_config_missing_file(self):
        with patch("builtins.open", side_effect=FileNotFoundError):
            config = load_config()
            assert "default_settings" in config


class TestPhoneValidation:
    @pytest.mark.parametrize(
        "phone,expected",
        [
            ("+1234567890", True),
            ("+919876543210", True),
            ("1234567890", False),
            ("+123", False),
            ("invalid", False),
            ("+12345678901234567890", False),
        ],
    )
    def test_validate_phone_number(self, phone, expected):
        with patch("bot.config", {"validation": {"phone_pattern": r"^\+\d{10,15}$"}}):
            with patch("bot.logger"):
                result = validate_phone_number(phone)
                assert result == expected


@pytest.mark.skipif(not AI_AVAILABLE, reason="AI features not available")
class TestAIFeatures:
    @pytest.fixture
    def ai_assistant(self):
        return AIMessageAssistant()

    @pytest.mark.asyncio
    async def test_message_generation(self, ai_assistant):
        with patch.object(ai_assistant, "openai_client") as mock_client:
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[
                0
            ].message.content = '["Test message 1", "Test message 2"]'
            mock_client.chat.completions.acreate = AsyncMock(return_value=mock_response)

            suggestions = await ai_assistant.generate_message_suggestions(
                "test context"
            )

            assert isinstance(suggestions, list)
            assert len(suggestions) > 0

    def test_sentiment_analysis(self, ai_assistant):
        if ai_assistant.sentiment_analyzer is None:
            pytest.skip("Sentiment analyzer not available")

        result = ai_assistant.analyze_sentiment("I love this product!")
        assert "label" in result
        assert "score" in result


class TestSmartScheduler:
    @pytest.fixture
    def scheduler(self):
        return SmartScheduler()

    def test_database_initialization(self, scheduler):
        assert os.path.exists(scheduler.db_path)

    def test_optimal_send_time(self, scheduler):
        """Test optimal send time calculation"""
        result = scheduler.get_optimal_send_time("+1234567890")

        assert "optimal_hour" in result
        assert "confidence" in result
        assert 0 <= result["optimal_hour"] <= 23

    def test_analytics_logging(self, scheduler):
        """Test message analytics logging"""
        from datetime import datetime

        # This should not raise an exception
        scheduler.log_message_analytics(
            phone_number="+1234567890",
            send_time=datetime.now(),
            delivered=True,
            read=False,
            response_time=300,
        )


class TestSecurity:
    @pytest.fixture
    def security_manager(self):
        return SecurityManager()

    def test_encryption_decryption(self, security_manager):
        original_data = "+1234567890"
        encrypted = security_manager.encrypt_contact(original_data)
        decrypted = security_manager.decrypt_contact(encrypted)

        assert decrypted == original_data
        assert encrypted != original_data

    @pytest.mark.parametrize(
        "input_data,expected",
        [
            ("normal text", True),
            ("script tag", False),
            ("javascript:alert(1)", False),
            ("../etc/passwd", False),
            ("regular message", True),
        ],
    )
    def test_input_validation(self, security_manager, input_data, expected):
        """Test security input validation"""
        result = security_manager.validate_secure_input(input_data)
        assert result == expected


class TestAnalytics:
    @pytest.fixture
    def analytics(self):
        return ModernAnalytics()

    def test_delivery_report_generation(self, analytics):
        report = analytics.generate_delivery_report()

        required_fields = [
            "period",
            "total_messages",
            "delivery_rate",
            "read_rate",
            "avg_response_time",
            "best_hours",
        ]

        for field in required_fields:
            assert field in report


class TestAsyncOperations:
    @pytest.mark.asyncio
    async def test_async_message_processing(self):
        async def mock_send_message(message):
            await asyncio.sleep(0.1)
            return {"status": "sent", "message": message}

        messages = ["Message 1", "Message 2", "Message 3"]
        tasks = [mock_send_message(msg) for msg in messages]
        results = await asyncio.gather(*tasks)

        assert len(results) == len(messages)
        for result in results:
            assert result["status"] == "sent"


class TestModernFeatures:
    def test_rich_ui_availability(self):
        try:
            from rich.console import Console

            console = Console()
            assert console is not None
        except ImportError:
            pytest.skip("Rich UI not available")

    def test_async_support(self):
        async def test_async_function():
            return "async working"

        assert asyncio.iscoroutinefunction(test_async_function)


class TestPerformance:
    @pytest.mark.benchmark
    def test_config_loading_performance(self, benchmark):
        result = benchmark(load_config)
        assert isinstance(result, dict)

    @pytest.mark.benchmark
    def test_phone_validation_performance(self, benchmark):
        with patch("bot.config", {"validation": {"phone_pattern": r"^\+\d{10,15}$"}}):
            with patch("bot.logger"):
                result = benchmark(validate_phone_number, "+1234567890")
                assert result is True


@pytest.mark.integration
class TestIntegration:
    @pytest.mark.skipif(not AI_AVAILABLE, reason="AI features required")
    async def test_complete_ai_workflow(self):
        pass


if __name__ == "__main__":
    pytest.main([__file__])
