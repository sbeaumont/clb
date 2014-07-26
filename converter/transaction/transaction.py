import re

IBAN_RABOBANK_PREFIX = "NL20RABO"

class CSVParseError(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)

class Transaction:
    """Base type for all transaction types. Subclass this and update the TransactionFactory to extend the
    types of transactions the TransactionCSVReader can handle.
    """
    def __init__(self, source):
        self.source = source
    
    def __str__(self):
        return self.__class__.__name__ + " (" + str(self.source) + ")"
    
    def validate(self):
        """Validates the transaction fields with the regexes given by the fields() method.

        Throws a CSVParseError if any violation is found."""
        transaction = self.source
        fields = self.fields()

        for i in range(len(transaction)):
            pattern = fields[i][1]
            value = transaction[i]
            if not re.match(pattern, value):
                fieldname = fields[i][0]
                msg = "Field #%s(%s) value: '%s' did not comply with expected pattern '%s'" % (str(i), fieldname, transaction[i], pattern)
                raise CSVParseError, msg 

    def fields(self):
        """The fields of the transaction in the order they are in the CSV file.
        
        Each field is a tuple (fieldname, regex for syntax checking)."""
        pass

    def fromAccount(self):
        """The from accountnumber."""
        pass

    def name(self):
        """The name of the counterparty of the transaction."""
        pass
    
    def type(self):
        """The transaction type e.g. debit, credit."""
        pass
        
    def amount(self):
        """The signed amount from the client's perspective."""
        pass
        
    def to(self):
        """The account number of the counterparty."""
        pass
    
    def date(self):
        """The book date of the transaction."""
        pass
    
    def description(self):
        """Extra description text of the transaction."""
        pass
