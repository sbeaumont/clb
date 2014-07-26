"""Format of the older, non-SEPA Rabobank exports.

Based on http://www.rabobank.nl/images/formaatbeschrijving_csv_kommagescheiden_nieuw_29539176.pdf

Because we live in a SEPA compliant world now, this type will add the Rabobank IBAN prefix to the 'from account' number.
This makes sure that all transactions for an account end up in the same account in the output file, whether they came
from a compliant or non-compliant source."""

import transaction
from transaction import Transaction

NON_SEPA_COMPLIANT_FIELDS = (
    ("VAN_REK", "^\d{10}$"),
    ("MUNTSOORT", "^EUR$"),
    ("RENTEDATUM", "^\d{8}$"),
    ("BY_AF_CODE", "^[DC]$"),
    ("BEDRAG", "^\d{,12}\.\d{2}$"),
    ("NAAR_REK", "^\w{,10}$"),
    ("NAAR_NAAM", "^.{,24}$"),
    ("BOEKDATUM", "^\d{8}$"),
    ("BOEKCODE", "^\w{,2}$"),
    ("BUDGETCODE", "^.{,6}$"),
    ("OMSCHR1", "^.{,32}$"),
    ("OMSCHR2", "^.{,32}$"),
    ("OMSCHR3", "^.{,32}$"),
    ("OMSCHR4", "^.{,32}$"),
    ("OMSCHR5", "^.{,32}$"),
    ("OMSCHR6", "^.{,32}$")
)

NUM_FIELDS_NON_SEPA = len(NON_SEPA_COMPLIANT_FIELDS)

def isRabobankNonSEPATransaction(csvtransaction):
    """Recognizes a Rabobank (old) non-SEPA transaction because it has 16 fields and has no IBAN prefix in the first account number field."""
    return (len(csvtransaction) == NUM_FIELDS_NON_SEPA) and (not csvtransaction[0].startswith(transaction.IBAN_RABOBANK_PREFIX))

class RabobankNonSEPATransaction(Transaction):
    def fields(self):
        return NON_SEPA_COMPLIANT_FIELDS

    def fromAccount(self):
        if not self.ibansource:
            import request
            self.ibansource = (request.get("http://www.openiban.nl/?rekeningnummer=%s&output=json)" % self.source[0])).json()['iban']
        print self.ibansource
        return self.ibansource
        
        #return transaction.IBAN_RABOBANK_PREFIX + self.source[0]

    def name(self):
        return self.source[6]
    
    def type(self):
        return self.source[3]
        
    def amount(self):
        return self.source[4]
        
    def to(self):
        #tegenrekening
        return self.source[5]
    
    def date(self):
        return self.source[7]
    
    def description(self):
        return self.source[10]