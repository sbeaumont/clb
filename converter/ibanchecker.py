import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../lib")

import urllib
import requests

r = requests.get("http://www.openiban.nl/?rekeningnummer=0323129684&output=json")
print r.json()

#?getBIC=true&validateBankCode=true
#params = urllib.urlencode({'number': '323129684', 'bank': 'RABO'})
# f =  urllib.urlopen("http://www.ibannl.org/iban_check.php", data=params )
#f =  urllib.urlopen("http://openiban.com/validata/IBAN_NUMBER", data=params )
#print f.read()