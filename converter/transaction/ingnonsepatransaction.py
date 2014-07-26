"""
Format for ING Bank exports.

Format found on http://wiki.yuki.nl/ING-Bank-CSV-formaat.ashx


Veld  Omschrijving              Formaat                   Voorbeeld
====  ========================  ========================  =============
1     Eigen Bankrekening        Tekst                     "551.951.253"
2     Datum                     Tekst                     "20-11-2008"
3     AF of BIJ                 Tekst                     "BIJ"
4     Bedrag                    Getal met decimale komma  2291,34
5     Bankrekening tegenpartij  Tekst                     "231.159.113"

"""

from transaction import Transaction
from converter import ibanconverter

def isINGNonSEPATransaction(transaction):
    """Recognizes an ING transaction due to its number of fields (5). Converts any commas to dots in amount and removes the dots in the account number."""
    return len(transaction) == 5

class INGNonSEPATransaction(Transaction):
    """ING CSV Format transaction.
    
    Converts 'from account' number to IBAN format.
    To Do: use look up service to convert counteraccounts.
    Changes (dutch) comma for amount to a dot, which is the standard of this tool."""
    
    def _convertToIBAN(self, accountNumber):
        return ibanconverter.check(accountNumber.replace(".", "").rjust(10, "0"))
    
    def fields(self):
        pass

    def fromAccount(self):
        return self._convertToIBAN(self.source[0])

    def name(self):
        return ""
    
    def type(self):
        return self.source[2]
        
    def amount(self):
        return self.source[3].replace(",", ".")
        
    def to(self):
        return self._convertToIBAN(self.source[4])
    
    def date(self):
        return self.source[1]
    
    def description(self):
        return ""
