import getpass
import pickle
import random
from datetime import datetime, timedelta
from pathlib import Path

import jwt
import multidict
import ujson

import Robinhood.urls as urls
from Robinhood.helper import ApiOperations


class Authorization(ApiOperations):

    def __init__(self):
        super(Authorization, self).__init__()

    @staticmethod
    def is_token_valid(access_token, minutes_before_exp=30):
        time_stamp = jwt.decode(access_token, verify=False)['exp']
        real_time_stamp = datetime.fromtimestamp(time_stamp)
        return real_time_stamp - timedelta(minutes=minutes_before_exp) > datetime.now()

    async def custom_async_get_wild(self, url, data_type='regular', headers=None, params=None, jsonify_data=True):
        if not jsonify_data:
            res = await self.async_get_wild(url, headers=headers, params=params, jsonify_data=False)
            return res
        res = await self.async_get_wild(url, headers=headers, jsonify_data=True)
        if data_type == 'results':
            return res['results']
        elif data_type == 'pagination':
            data = [res['results']]
            count = 0
            if 'next' in res:
                while res['next']:
                    res = await self.async_get_wild(res['next'], jsonify_data=True)
                    count += 1
                    assert count < 100
                    if 'results' in res:
                        for item in res['results']:
                            data.append(item)
            return data
        elif data_type == 'indexzero':
            data = res['results'][0]
            return data
        else:
            return res

    @staticmethod
    def generate_device_token():
        """This function will generate a token used when logging on.

        :returns: A string representing the token.

        """
        rands = []
        for i in range(0, 16):
            r = random.random()
            rand = 4294967296.0 * r
            rands.append((int(rand) >> ((3 & i) << 3)) & 255)

        hexa = []
        for i in range(0, 256):
            hexa.append(str(hex(i + 256)).lstrip("0x").rstrip("L")[1:])

        ids = ""
        for i in range(0, 16):
            ids += hexa[rands[i]]

            if (i == 3) or (i == 5) or (i == 7) or (i == 9):
                ids += "-"

        return ids

    async def login(self, username=None, password=None, expires_in=86400, scope='internal', by_sms=True,
                    store_session=True, pickle_file="robinhood"):
        """This function will effectivly log the user into robinhood by getting an
        authentication token and saving it to the session header. By default, it
        will store the authentication token in a pickle file and load that value
        on subsequent logins.

        :param pickle_file: The name of the pickle file
        :type pickle_file: Optional[str]
        :param username: The username for your robinhood account, usually your email.
            Not required if credentials are already cached and valid.
        :type username: Optional[str]
        :param password: The password for your robinhood account. Not required if
            credentials are already cached and valid.
        :type password: Optional[str]
        :param expires_in: The time until your login session expires. This is in seconds.
        :type expires_in: Optional[int]
        :param scope: Specifies the scope of the authentication.
        :type scope: Optional[str]
        :param by_sms: Specifies whether to send an email(False) or an sms(True)
        :type by_sms: Optional[boolean]
        :param store_session: Specifies whether to save the log in authorization
            for future log ins.
        :type store_session: Optional[boolean]
        :returns:  A dictionary with log in information. The 'access_token' keyword contains the access token, and the 'detail' keyword \
        contains information on whether the access token was generated or loaded from pickle file.

        """
        device_token = Authorization.generate_device_token()
        header_states = Path.cwd().joinpath(f'confidential/header_states/{pickle_file}.json')
        pickle_path = Path.cwd().joinpath(f'confidential/account_states/{pickle_file}.pickle')
        url = urls.login_url()
        payload = {
            'client_id': 'c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS',
            'expires_in': expires_in,
            'grant_type': 'password',
            'password': password,
            'scope': scope,
            'username': username,
            'challenge_type': "sms" if by_sms else "email",
            'device_token': device_token
        }
        # If authentication has been stored in pickle file then load it. Stops login server from being pinged so much.

        # If store_session has been set to false then delete the pickle file, otherwise try to load it.
        # Loading pickle file will fail if the access_token has expired.
        if store_session:
            recreate_token = False
            if header_states.exists():
                with open(str(header_states), 'r') as header_file:
                    untested_default_header = ujson.load(header_file)
                if 'Authorization' in untested_default_header:
                    access_token = untested_default_header['Authorization'].split(' ')[1]
                    if self.is_token_valid(access_token):
                        self.default_header = multidict.CIMultiDict(untested_default_header)
                    else:
                        header_states.unlink()
                        recreate_token = True
                else:
                    header_states.unlink()
                    recreate_token = True
            if pickle_path.exists():
                with open(str(pickle_path), 'rb') as f:
                    pickle_data = pickle.load(f)
                access_token = pickle_data['access_token']
                if self.is_token_valid(access_token):
                    token_type = pickle_data['token_type']
                    refresh_token = pickle_data['refresh_token']
                    pickle_device_token = pickle_data['device_token']
                    payload['device_token'] = pickle_device_token
                    if not recreate_token:
                        return {'access_token': access_token,
                                'token_type': token_type,
                                'expires_in': expires_in,
                                'scope': scope,
                                'detail': f'logged in using authentication in {pickle_file}.pickle',
                                'backup_code': None,
                                'refresh_token': refresh_token}
                else:
                    pickle_path.unlink()

        # Try to log in normally.
        if not username:
            username = input("Robinhood username: ")
            payload['username'] = username
        if not password:
            password = getpass.getpass("Robinhood password: ")
            payload['password'] = password

        data = await self.async_post_wild(url, payload, headers=self.default_header, jsonify_data=True)
        # Handle case where mfa or challenge is required.
        if data:
            if 'mfa_required' in data:
                mfa_token = input("Please type in the MFA code: ")
                payload['mfa_code'] = mfa_token
                res = await self.async_post_wild(url, payload, jsonify_data=False)
                while res.status_code != 200:
                    mfa_token = input(
                        "That MFA code was not correct. Please type in another MFA code: ")
                    payload['mfa_code'] = mfa_token
                    res = await self.async_post_wild(url, payload, jsonify_data=False)
                data = res.json()
            elif 'challenge' in data:
                challenge_id = data['challenge']['id']
                sms_code = input('Enter Robinhood code for validation: ')
                res = await self.respond_to_challenge(challenge_id, sms_code)
                while 'challenge' in res and res['challenge']['remaining_attempts'] > 0:
                    sms_code = input(
                        f"That code was not correct. {res['challenge']['remaining_attempts']} tries remaining. Try Again: ")
                    res = await self.respond_to_challenge(challenge_id, sms_code)
                data = await self.async_post_wild(url, payload,
                                                  headers={'X-ROBINHOOD-CHALLENGE-RESPONSE-ID': challenge_id},
                                                  jsonify_data=True)
            # Update Session data with authorization or raise exception with the information present in data.
            if 'access_token' in data:
                token = f"{data['token_type']} {data['access_token']}"
                self.default_header['Authorization'] = token
                data['detail'] = "logged in with brand new authentication code."
                if store_session:
                    with open(str(pickle_path), 'wb') as f:
                        pickle.dump({'token_type': data['token_type'],
                                     'access_token': data['access_token'],
                                     'refresh_token': data['refresh_token'],
                                     'device_token': device_token}, f)
                    with open(str(header_states), 'w') as f:
                        f.write(ujson.dumps(dict(self.default_header), indent=4, sort_keys=True))
            else:
                raise Exception(data['detail'])
        else:
            raise Exception('Error: Trouble connecting to Robinhood API. Check internet connection.')
        return data

    @staticmethod
    def save_to_json_dict(filename, contents):
        with open(filename, 'w') as f:
            f.write(ujson.dumps(contents, indent=4, sort_keys=True))

    @staticmethod
    def save_to_json(filename, contents):
        with open(filename, 'w') as f:
            f.write(ujson.dumps(contents, indent=4))

    async def respond_to_challenge(self, challenge_id, sms_code):
        """This function will post to the challenge url.

        :param challenge_id: The challenge id.
        :type challenge_id: str
        :param sms_code: The sms code.
        :type sms_code: str
        :returns:  The response from requests.

        """
        url = urls.challenge_url(challenge_id)
        payload = {
            'response': sms_code
        }
        resp = await self.async_post_wild(url, payload, jsonify_data=True)
        return resp

    async def id_for_stock(self, symbol):
        """Takes a stock ticker and returns the instrument id associated with the stock.

        :param symbol: The symbol to get the id for.
        :type symbol: str
        :returns:  A string that represents the stocks instrument id.

        """

        symbol = symbol.upper().strip()

        url = 'https://api.robinhood.com/instruments/'
        payload = {'symbol': symbol}
        data = await self.async_get_wild(url, 'indexzero', payload, jsonify_data=True)
        return filter(data, 'id')

    async def id_for_chain(self, symbol):
        """Takes a stock ticker and returns the chain id associated with a stocks option.

        :param symbol: The symbol to get the id for.
        :type symbol: str
        :returns:  A string that represents the stocks options chain id.

        """
        try:
            symbol = symbol.upper().strip()
        except AttributeError as message:
            print(message)
            return (None)

        payload = {'symbol': symbol}
        url = 'https://api.robinhood.com/instruments/'
        data = await self.async_get_wild(url, headers=self.default_header, params=payload, jsonify_data=True)
        return data['results'][0]['tradable_chain_id']

    async def id_for_group(self, symbol):
        """Takes a stock ticker and returns the id associated with the group.

        :param symbol: The symbol to get the id for.
        :type symbol: str
        :returns:  A string that represents the stocks group id.

        """
        try:
            symbol = symbol.upper().strip()
        except AttributeError as message:
            print(message)
            return (None)

        url = f'https://api.robinhood.com/options/chains/{await self.id_for_chain(symbol)}/'
        data = await self.async_get_wild(url, headers=self.default_header, jsonify_data=True)
        return data['underlying_instruments'][0]['id']

    async def id_for_option(self, symbol, expiration_date, strike, option_type):
        """Returns the id associated with a specific option order.

        :param symbol: The symbol to get the id for.
        :type symbol: str
        :param expiration_date: The expiration date as YYYY-MM-DD
        :type expiration_date: str
        :param strike: The strike price.
        :type strike: str
        :param option_type: Either call or put.
        :type option_type: str
        :returns:  A string that represents the stocks option id.

        """
        symbol = symbol.upper()

        payload = {
            'chain_symbol': symbol,
            'expiration_date': expiration_date,
            'strike_price': strike,
            'type': option_type,
            'state': 'active'
        }
        url = 'https://api.robinhood.com/options/instruments/'
        data = await self.custom_async_get_wild(url, 'pagination', params=payload)

        list_of_options = [item for item in data if item["expiration_date"] == expiration_date]
        if len(list_of_options) == 0:
            print(
                'Getting the option ID failed. Perhaps the expiration date is wrong format, or the strike price is wrong.')
            return None

        return list_of_options[0]['id']

    @staticmethod
    def error_argument_not_key_in_dictionary(keyword):
        return f'Error: The keyword "{keyword}" is not a key in the dictionary.'

    @staticmethod
    def filter(data, info):
        """Takes the data and extracts the value for the keyword that matches info.

        :param data: The data returned by request_get.
        :type data: dict or list
        :param info: The keyword to filter from the data.
        :type info: str
        :returns:  A list or string with the values that correspond to the info keyword.

        """
        if (data == None):
            return (data)
        elif (data == [None]):
            return ([])
        elif (type(data) == list):
            if (len(data) == 0):
                return ([])
            compareDict = data[0]
            noneType = []
        elif (type(data) == dict):
            compareDict = data
            noneType = None

        if info is not None:
            if info in compareDict and type(data) == list:
                return ([x[info] for x in data])
            elif info in compareDict and type(data) == dict:
                return (data[info])
            else:
                print(Authorization.error_argument_not_key_in_dictionary(info))
                return (noneType)
        else:
            return (data)

    async def main(self):
        data = await self.login()
        print(data)


if __name__ == '__main__':
    instance = Authorization()
