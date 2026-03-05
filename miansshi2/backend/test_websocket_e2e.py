# test_websocket_e2e.py
"""
End-to-end tests for WebSocket speech recognition.
"""
import pytest
import asyncio
import json
import base64
import websockets


pytest_plugins = ('pytest_asyncio',)


class TestWebSocketSpeechRecognition:
    """End-to-end tests for WebSocket speech recognition endpoint."""

    @pytest.mark.asyncio
    async def test_websocket_connection_success(self):
        """Should be able to connect to WebSocket endpoint."""
        ws_url = "ws://localhost:8000/api/ws/speech"

        async with websockets.connect(
            ws_url,
            origin="http://localhost:5173",  # Must match CORS origins
            open_timeout=10
        ) as ws:
            # Connection should succeed
            assert ws.open

    @pytest.mark.asyncio
    async def test_websocket_start_message(self):
        """Should receive empty response on start message."""
        ws_url = "ws://localhost:8000/api/ws/speech"

        async with websockets.connect(
            ws_url,
            origin="http://localhost:5173",
            open_timeout=10
        ) as ws:
            # Send start message
            await ws.send(json.dumps({"type": "start"}))

            # Should receive response
            response = await asyncio.wait_for(ws.recv(), timeout=5)
            data = json.loads(response)

            assert "text" in data
            assert "is_final" in data
            assert data["is_final"] == False

    @pytest.mark.asyncio
    async def test_websocket_stop_without_audio(self):
        """Should handle stop without audio gracefully."""
        ws_url = "ws://localhost:8000/api/ws/speech"

        async with websockets.connect(
            ws_url,
            origin="http://localhost:5173",
            open_timeout=10
        ) as ws:
            # Send start
            await ws.send(json.dumps({"type": "start"}))
            await ws.recv()

            # Send stop immediately
            await ws.send(json.dumps({"type": "stop"}))

            # Should receive final response
            response = await asyncio.wait_for(ws.recv(), timeout=10)
            data = json.loads(response)

            assert data["is_final"] == True
            # Empty audio should return empty text
            assert data["text"] == ""

    @pytest.mark.asyncio
    async def test_websocket_audio_processing(self):
        """Should process audio data and return recognition result."""
        ws_url = "ws://localhost:8000/api/ws/speech"

        async with websockets.connect(
            ws_url,
            origin="http://localhost:5173",
            open_timeout=10
        ) as ws:
            # Send start
            await ws.send(json.dumps({"type": "start"}))
            await ws.recv()

            # Generate some dummy audio (16KHz, 16bit, mono, 1 second)
            # This is just zeros, so it won't produce meaningful text
            # but it tests the audio processing pipeline
            sample_rate = 16000
            duration = 1  # seconds
            num_samples = sample_rate * duration
            audio_data = bytes(num_samples * 2)  # 16-bit = 2 bytes per sample

            # Send audio in chunks
            chunk_size = 4096
            for i in range(0, len(audio_data), chunk_size):
                chunk = audio_data[i:i + chunk_size]
                audio_b64 = base64.b64encode(chunk).decode('utf-8')
                await ws.send(json.dumps({
                    "type": "audio",
                    "audio_data": audio_b64
                }))

            # Send stop
            await ws.send(json.dumps({"type": "stop"}))

            # Wait for final response with longer timeout for XunFei processing
            final_response = None
            for _ in range(20):  # Increased iterations
                try:
                    response = await asyncio.wait_for(ws.recv(), timeout=10)  # Longer timeout
                    data = json.loads(response)
                    print(f"Received: {data}")  # Debug
                    if data.get("is_final"):
                        final_response = data
                        break
                except asyncio.TimeoutError:
                    print("Timeout waiting for response")
                    break
                except websockets.exceptions.ConnectionClosed as e:
                    print(f"Connection closed: {e}")
                    break

            assert final_response is not None, "Should receive a final response"
            assert final_response["is_final"] == True
            # Silence may produce empty text or an error (XunFei API behavior)
            # The important thing is we get a response


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
