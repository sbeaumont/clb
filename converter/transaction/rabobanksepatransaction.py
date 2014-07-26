"""Format of the new (2014) SEPA compliant Rabobank exports.

Based on http://www.rabobank.nl/images/formaatbeschrijving_csv_kommagescheiden_nieuw_29539176.pdf

ba = Betaalautomaat
ck = Chipknip
db = Rente Lening (debet?)
ga = geldautomaat
tb = intern overgeboekt
id = CJJIB
ma = afgeschreven
cb = credit boeking?
sb = salaris betaling?
bg = een of andere overboeking
kh = stortingsapparaat
ac = betaling aan publieke dienst

"""

import re
import transaction
from transaction import Transaction

SEPA_COMPLIANT_FIELDS = (
    ("REKENINGNUMMER_REKENINGHOUDER", "^NL\d{2}RABO\d{10}$"),
    ("MUNTSOORT", "^EUR$"),
    ("RENTEDATUM", "^\d{8}$"),
    ("BY_AF_CODE", "^[DC]$"),
    ("BEDRAG", "^\d{,12}\.\d{2}$"),
    ("TEGENREKENING", "^\w{,35}$"),
    ("NAAR_NAAM", "^.{,70}$"),
    ("BOEKDATUM", "^\d{8}$"),
    ("BOEKCODE", "^\w{,2}$"),
    ("FILLER", "^.{,6}$"),
    ("OMSCHR1", "^.{,35}$"),
    ("OMSCHR2", "^.{,35}$"),
    ("OMSCHR3", "^.{,35}$"),
    ("OMSCHR4", "^.{,35}$"),
    ("OMSCHR5", "^.{,35}$"),
    ("OMSCHR6", "^.{,35}$"),
    ("END_TO_END_ID", "^.{,35}$"),
    ("ID_TEGENREKENINGHOUDER", "^.{,35}$"),
    ("MANDAAT_ID", "^.{,35}$")
)

NUM_FIELDS_SEPA = len(SEPA_COMPLIANT_FIELDS)

def isRabobankSEPATransaction(csvtransaction):
    return (len(csvtransaction) == NUM_FIELDS_SEPA) and re.match(SEPA_COMPLIANT_FIELDS[0][1], csvtransaction[0])

class RabobankSEPATransaction(Transaction):
    def fields(self):
        return SEPA_COMPLIANT_FIELDS

    def fromAccount(self):
        return self.source[0]

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