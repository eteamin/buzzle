from os import path
import threading

import pytest
import aiohttp
import aiofiles
import async_timeout

import buzzle
from buzzle.src.wsgi import buzzle_app


def run_sandbox_server():
    pass


TEST_FILE = path.abspath(path.join(path.dirname(buzzle.__file__), 'tests', 'stuff', 'file.gif'))
TIMEOUT = 2
server = threading.Thread(target=run_sandbox_server, daemon=True)
server.start()


@pytest.mark.asyncio
async def test_store():
    async with aiofiles.open(TEST_FILE, 'rb') as file:
        pass


