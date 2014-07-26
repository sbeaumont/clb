from transaction import CSVParseError
from transaction import Transaction

class NullTransaction(Transaction):
    """Null type for unrecognized transaction types"""
    def name(self):
        return self.source
        
    def validate(self):
        raise CSVParseError, "Transaction " + str(self.source) + " of unknown type."
    