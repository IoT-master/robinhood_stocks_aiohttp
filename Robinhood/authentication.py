import getpass
import pickle
from pathlib import Path

import multidict
import ujson

import Robinhood.urls as urls


async def login(self, username=None, password=None, expires_in=86400, scope='internal', by_sms=True,
                store_session=True, pickle_file="robinhood", client_id='c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS'):
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
    device_token = self.generate_device_token()
    header_states = Path.cwd().joinpath(f'confidential/header_states/{pickle_file}.json')
    pickle_path = Path.cwd().joinpath(f'confidential/account_states/{pickle_file}.pickle')
    url = urls.login_url()
    payload = {
        'client_id': client_id,
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
                    return True
                else:
                    header_states.unlink()
                    recreate_token = True
            else:
                header_states.unlink()
                recreate_token = True
        # if pickle_path.exists():
        #     with open(str(pickle_path), 'rb') as f:
        #         pickle_data = pickle.load(f)
        #     access_token = pickle_data['access_token']
        #     if self.is_token_valid(access_token):
        #         token_type = pickle_data['token_type']
        #         refresh_token = pickle_data['refresh_token']
        #         pickle_device_token = pickle_data['device_token']
        #         payload['device_token'] = pickle_device_token
        #         if not recreate_token:
        #             return {'access_token': access_token,
        #                     'token_type': token_type,
        #                     'expires_in': expires_in,
        #                     'scope': scope,
        #                     'detail': f'logged in using authentication in {pickle_file}.pickle',
        #                     'backup_code': None,
        #                     'refresh_token': refresh_token}
        #     else:
        #         pickle_path.unlink()

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



