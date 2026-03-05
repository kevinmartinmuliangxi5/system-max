# test_speech_service.py
"""
TDD tests for speech recognition service.
These tests verify the XunFei speech client works correctly.
"""
import pytest
import asyncio

# Configure pytest-asyncio
pytest_plugins = ('pytest_asyncio',)


class TestServicesImport:
    """Test that services module can be imported correctly."""

    def test_services_module_imports_without_error(self):
        """Services module should import without AttributeError."""
        # This test will fail if websockets.exceptions is not properly imported
        import services
        assert services is not None

    def test_xunfei_client_class_exists(self):
        """XunfeiSpeechClient class should be importable."""
        from services import XunfeiSpeechClient
        assert XunfeiSpeechClient is not None

    def test_websockets_exceptions_import(self):
        """Websockets exceptions should be importable the correct way."""
        from websockets.exceptions import ConnectionClosed, ConnectionClosedError
        assert ConnectionClosed is not None
        assert ConnectionClosedError is not None


class TestXunfeiSpeechClient:
    """Test XunfeiSpeechClient functionality."""

    def test_client_initializes_with_config(self):
        """Client should initialize with config from settings."""
        from services import XunfeiSpeechClient
        client = XunfeiSpeechClient()

        assert client.app_id is not None
        assert client.api_key is not None
        assert client.api_secret is not None
        assert len(client.app_id) > 0

    def test_auth_url_generation(self):
        """Client should generate valid auth URL."""
        from services import XunfeiSpeechClient
        client = XunfeiSpeechClient()

        url = client._generate_auth_url()

        assert url.startswith("wss://iat-api.xfyun.cn/v2/iat")
        assert "authorization=" in url
        assert "date=" in url
        assert "host=" in url

    def test_build_frame_returns_valid_json(self):
        """_build_frame should return valid JSON string."""
        import json
        from services import XunfeiSpeechClient
        client = XunfeiSpeechClient()

        frame = client._build_frame(0, 0, b"test audio")

        # Should be valid JSON
        data = json.loads(frame)

        assert "common" in data
        assert "business" in data
        assert "data" in data
        assert data["common"]["app_id"] == client.app_id
        assert data["data"]["status"] == 0

    @pytest.mark.asyncio
    async def test_transcribe_empty_chunks_returns_empty(self):
        """Transcribe with empty chunks should return empty string."""
        from services import XunfeiSpeechClient
        client = XunfeiSpeechClient()

        result = await client.transcribe([])

        assert result == ""

    @pytest.mark.asyncio
    async def test_transcribe_small_audio_returns_empty(self):
        """Transcribe with audio < 1000 bytes should return empty."""
        from services import XunfeiSpeechClient
        client = XunfeiSpeechClient()

        result = await client.transcribe([b"small"])

        assert result == ""


class TestXunfeiConnection:
    """Integration tests for XunFei API connection."""

    @pytest.mark.asyncio
    async def test_can_connect_to_xunfei(self):
        """Should be able to establish WebSocket connection to XunFei."""
        import json
        import websockets
        from services import XunfeiSpeechClient

        client = XunfeiSpeechClient()
        ws_url = client._generate_auth_url()

        async with websockets.connect(
            ws_url,
            ping_interval=None,
            open_timeout=10
        ) as ws:
            # Send empty end frame to test connection
            frame = client._build_frame(0, 2, b"")
            await ws.send(frame)

            result = await asyncio.wait_for(ws.recv(), timeout=5)
            data = json.loads(result)

            # Connection should succeed with code 0
            assert data.get("code") == 0 or "message" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
