import rabobanksepatransaction
import rabobanknonsepatransaction
import ingnonsepatransaction
import nulltransaction

def createTransaction(transaction):
    """Factory for transaction types. Subclass Transaction and register here to extend types of transactions handled.
    Take care to implement the check routines so that they uniquely identify each type!
    
    Returns a NullTransaction if no match is found."""
    if rabobanksepatransaction.isRabobankSEPATransaction(transaction):
        return rabobanksepatransaction.RabobankSEPATransaction(transaction)
    elif rabobanknonsepatransaction.isRabobankNonSEPATransaction(transaction):
        return rabobanknonsepatransaction.RabobankNonSEPATransaction(transaction)
    elif ingnonsepatransaction.isINGNonSEPATransaction(transaction):
        return ingnonsepatransaction.INGNonSEPATransaction(transaction)
    else:
        return nulltransaction.NullTransaction(transaction)
