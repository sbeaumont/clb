import urllib

#?getBIC=true&validateBankCode=true
params = urllib.urlencode({'number': '323129684', 'bank': 'RABO'})
f =  urllib.urlopen("http://www.ibannl.org/iban_check.php", data=params )
print f.read()