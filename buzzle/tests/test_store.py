from os import path
import subprocess
import asyncio
import time

import aiofiles
import aiohttp
import async_timeout

import buzzle
from buzzle.src.variables import url, virtual_env

TEST_FILE = path.abspath(path.join(path.dirname(buzzle.__file__), 'tests', 'stuff', 'file.gif'))
path_to_wsgi = path.abspath(path.join(path.dirname(buzzle.__file__), 'src', 'wsgi.py'))
TIMEOUT = 2

async def test_store(loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        async with aiofiles.open(TEST_FILE, 'rb') as file:
            payload = {
                'file': await file.read()
            }
            async with session.post(url, data=payload) as resp:
                assert await resp.text() == 'Ok'
            async with session.get('%s?filename=file' % url) as resp:
                assert await resp.text() == TEST_FILE


subprocess.Popen([virtual_env, path_to_wsgi])
time.sleep(1)

loop = asyncio.get_event_loop()
loop.run_until_complete(test_store(loop))

subprocess.Popen(['killall', '-9', 'python3.5'])
