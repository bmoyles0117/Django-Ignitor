import settings

from telapi import rest

client = rest.Client(*settings.TELAPI_CREDENTIALS)
telapi_account = client.accounts[client.account_sid]