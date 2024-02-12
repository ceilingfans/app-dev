from bardapi import BardCookies
import os 

cookie_dict = {
    "__Secure-1PSID": os.environ.get("Secure-1PSID"),
    "__Secure-1PSIDTS": os.environ.get("secure-1PSIDTS"),
    "__Secure-1PSIDCC": os.environ.get("secure-1PSIDCC")
}

bard = BardCookies(cookie_dict=cookie_dict)

def bardchat(message):
    return bard.get_answer(message)['content']