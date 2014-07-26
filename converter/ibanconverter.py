import requests
import shelve
import logging

WEBSERVICE_DOMAIN = "openiban.nl"
IBAN_REQUEST_URL = "http://www.openiban.nl/?rekeningnummer=%s&output=json"
RESPONSE_IBAN_FIELD_NAME = "iban"
RESPONSE_ERROR_FIELD_NAME = "error"

CACHE_FILE_NAME = "ibancache"

log = logging.getLogger(__name__)

def check(accountNumber):
    """Convenience function that also ensures that ibanChecker is a singleton.
    Not thread safe! This is ok in the current context, because this code is
    only run as a single process on the command line."""
    return ibanChecker.checkForAccountNumber(accountNumber)

class IBANChecker():
    """Checks in a cache to see if the IBAN of an old account number can be found,
    otherwise goes out to a web service and fetches it. The result is cached on disk
    which is fine because the result is unchanging. The result is that you'll only need
    to fetch the IBAN the very first time the account number is encountered."""
    def __init__(self):
        self.cache = shelve.open(CACHE_FILE_NAME)
        
    def __del__(self):
        self.cache.close()
    
    def checkForAccountNumber(self, accountNumber):
        """Checks if an IBAN can be found for the given account number.
        Returns the IBAN if found, the original account number if not found.
        Returns empty string in case of a '0000..' account number (all zeroes)."""
        if self.cache.has_key(accountNumber):
            ibanNumber = self.cache[accountNumber]
        else:
            # Strip leading zeroes because the web service borks on them.
            strippedAccountNumber = accountNumber.lstrip("0")
            
            # In the 'corner case' (which actually is quite common in the 'to' field of Rabobank files)
            # of all zeroes you'll get an empty string, and the web service comes back with a web page
            # instead of an error response. In this case we'll just return an empty string, since that is
            # what a 00000000 bank account would represent: nothing.
            if strippedAccountNumber:            
                requestURL = IBAN_REQUEST_URL % strippedAccountNumber
                log.debug("Looking up %s", requestURL)
                webServiceResult = requests.get(requestURL)
                resultAsJSON = webServiceResult.json()
                if not resultAsJSON.has_key(RESPONSE_ERROR_FIELD_NAME):
                    # Everything is OK
                    log.info("%s result for %s is code (%s) with contents '%s'", WEBSERVICE_DOMAIN, requestURL, webServiceResult.status_code, webServiceResult.text)
                    ibanNumber = resultAsJSON[RESPONSE_IBAN_FIELD_NAME]
                else:
                    # Oops, could not find an IBAN. Just return the original account number in this case
                    log.warn("%s lookup UNSUCCESSFUL. Result for %s is code (%s) with contents '%s'", WEBSERVICE_DOMAIN, requestURL, webServiceResult.status_code, webServiceResult.text)
                    ibanNumber = accountNumber
                self.cache[accountNumber] = ibanNumber
            else:
                # Got a 000000... account number. Return empty account in this case.
                ibanNumber = ""
        return ibanNumber

ibanChecker = IBANChecker()