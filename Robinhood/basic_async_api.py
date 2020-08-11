import asyncio

import aiohttp
import multidict
import ujson


class ApiOperations(object):
    def __init__(self):
        self.session = None
        self.default_header = multidict.CIMultiDict({})
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.open_session())

    async def open_session(self):
        async with aiohttp.ClientSession(headers=self.default_header, json_serialize=ujson.dumps) as session:
            self.session = session
            await self.main()

    async def async_get_wild(self, url, params=None, headers=None, jsonify_data=False):
        async with self.session.get(url, params=params, headers=headers, ssl=False) as resp:
            if jsonify_data:
                try:
                    response = await resp.json()
                except aiohttp.client_exceptions.ContentTypeError as err:
                    print(err)
                    print(await resp.text())
                    raise
            else:
                response = await resp.text()
            return response

    async def async_post_wild(self, url, payload, params=None, headers=None, jsonify_data=False):
        async with self.session.post(url, params=params, data=payload, headers=headers, ssl=False) as resp:
            if jsonify_data:
                resp = await resp.json()
            else:
                resp = await resp.text()
            return resp

    async def async_delete(self, url, headers, payload):
        async with self.session.delete(url, headers=headers, data=payload, ssl=False) as resp:
            json_resp = await resp.json()
            return json_resp

    async def main(self):
        resp = await self.async_get_wild(
            'https://eth.nanopool.org/api/v1/load_account/0x0ac7e3f5060700cf30da11a9f1a503dd8c471840',
            jsonify_data=False)
        print(resp)


if __name__ == '__main__':
    instance = ApiOperations()
