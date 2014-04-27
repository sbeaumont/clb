try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

OFX_ROOT_TEMPLATE = """<OFX>
  <BANKMSGSRSV1>
    <STMTTRNRS>
      <STMTRS>
        <CURDEF>EUR</CURDEF>
        <BANKTRANLIST>
        </BANKTRANLIST>
      </STMTRS>
    </STMTTRNRS>
  </BANKMSGSRSV1>
</OFX>"""

OFX_STATEMENT_TEMPLATE = """<STMTTRN>
    <NAME></NAME>
    <DTPOSTED></DTPOSTED>
    <TRNTYPE></TRNTYPE>
    <TRNAMT></TRNAMT>
    <BANKACCTTO></BANKACCTTO>
    <MEMO></MEMO>
</STMTTRN>"""

class OFXWriter:
    """Writes Transaction instances into an OFX file.
    
    Based on OFX Specification 2.1.1.
    """
    
    def __init__(self):
        self._reset()
    
    def _reset(self):
        self.root = ET.Element("OFX")
        self.accountsRoot = ET.SubElement(ET.SubElement(self.root, "BANKMSGSRSV1"), "STMTTRNRS")
        self.accounts = {}
    
    def _transactionListForAccount(self, transaction):
        if (transaction.fromAccount() not in self.accounts):
            self._addFromAccount(transaction)
            
        return self.accounts[transaction.fromAccount()]
    
    def _addFromAccount(self, transaction):
        acctroot = ET.Element("STMTRS")
        ET.SubElement(acctroot, "CURDEF").text = "EUR"
        ET.SubElement(acctroot, "BANKACCTFROM").text = transaction.fromAccount()
        transactionList = ET.SubElement(acctroot, "BANKTRANLIST")
        self.accountsRoot.append(acctroot)
        
        self.accounts[transaction.fromAccount()] = transactionList
    
    def addTransaction(self, transaction):
        trnroot = ET.Element("STMTTRN")
        # Three things happen here for each line: create subnode, attach to transaction node, set node text
        ET.SubElement(trnroot, "NAME").text = transaction.name()
        ET.SubElement(trnroot, "DTPOSTED").text = transaction.date()
        ET.SubElement(trnroot, "TRNTYPE").text = transaction.type()
        ET.SubElement(trnroot, "TRNAMT").text = transaction.amount()
        ET.SubElement(trnroot, "BANKACCTTO").text = transaction.to()
        ET.SubElement(trnroot, "MEMO").text = transaction.description()
        
        self._transactionListForAccount(transaction).append(trnroot)
    
    def write(self):
        return ET.tostring(self.root)

if __name__ == '__main__':
    ofxwriter = OFXWriter()
    
    class TestTransaction:
        def fromAccount(self):
            return "1234"
        
        def name(self):
            return "name"
        
        def date(self):
            return "20140607"
        
        def type(self):
            return "DEBIT"
        
        def amount(self):
            return "-50.00"
        
        def to(self):
            return "NL20RABO123456890"
            
        def description(self):
            return "desc"
    

    ofxwriter.addTransaction(TestTransaction())
    ofxwriter.addTransaction(TestTransaction())
    ofxwriter.addTransaction(TestTransaction())
    
    print ofxwriter.write()
    