import pytest
import httpx
from unittest.mock import patch, AsyncMock
from cow_py.order_book.requests import request 

URL = 'https://cow.fi'
ERROR_MESSAGE = '💣💥 Booom!'
OK_RESPONSE = {'status': 200, 'ok': True, 'content': {'some': 'data'}}

@pytest.mark.asyncio
async def test_no_re_attempt_if_success():
    with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mocked_request:
        mocked_request.return_value = httpx.Response(200, json=OK_RESPONSE)
        result = await request(URL, {'path': '', 'method': 'GET'}, {'max_tries': 10})
        mocked_request.assert_awaited_once()
        assert result == OK_RESPONSE

@pytest.mark.asyncio
async def test_re_attempts_if_fails_then_succeeds():
    success_response = httpx.Response(200, json=OK_RESPONSE)
    
    mock_call = AsyncMock(side_effect=[
        httpx.HTTPStatusError(message=ERROR_MESSAGE, request=None, response=httpx.Response(500)),
        httpx.HTTPStatusError(message=ERROR_MESSAGE, request=None, response=httpx.Response(500)),
        httpx.HTTPStatusError(message=ERROR_MESSAGE, request=None, response=httpx.Response(500)),
        success_response
    ])

    with patch('httpx.AsyncClient.request', new=mock_call):
        result = await request(URL, {"method": "GET", "path": ""}, {'max_tries':10})
        
        assert result == OK_RESPONSE        
        assert mock_call.call_count == 4

@pytest.mark.asyncio
async def test_succeeds_last_attempt():
    success_response = httpx.Response(200, json=OK_RESPONSE)
    
    mock_call = AsyncMock(side_effect=[
        httpx.HTTPStatusError(message=ERROR_MESSAGE, request=None, response=httpx.Response(500)),
        httpx.HTTPStatusError(message=ERROR_MESSAGE, request=None, response=httpx.Response(500)),
        httpx.HTTPStatusError(message=ERROR_MESSAGE, request=None, response=httpx.Response(500)),
        success_response
    ])

    with patch('httpx.AsyncClient.request', new=mock_call):
        result = await request(URL, {"method": "GET", "path": ""}, {'max_tries':4})
        
        assert result == OK_RESPONSE        
        assert mock_call.call_count == 4

@pytest.mark.asyncio
async def test_does_not_reattempt_after_max_failures():
    with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mocked_request:
        with pytest.raises(Exception) as exc_info:  # Replace Exception with your specific exception
            mocked_request.return_value = httpx.Response(500, json={'error': ERROR_MESSAGE})
            await request(URL, {'path': '', 'method': 'GET'}, {'max_tries': 3})
            assert str(exc_info.value) == ERROR_MESSAGE
            assert len(mocked_request.call_count) == 3