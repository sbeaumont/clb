clb
===

Command Line Banker: manipulate bank transaction exports to a format usable by banking tools

For my personal banking I have always wanted to get a good overview of my spending habits, and this means that you have to tell the banking app in some way what transaction goes where. There is currently no tool that this in a open and reusable fashion. Some tools have nice reports, other tools have nice parsing features, but none have it all.

The Command Line Banker tries to fill the gap by doing three things:

1) Cleaning and deduplicating transactions (currently also includes converting to IBAN)
2) Converting transactions to a common format (OFX) that is used by most banking tools
3) Add tags to all transactions that allow easy categorization in banking tools.

Currently 1 and 2 work for the dutch Rabobank and ING, I've made the code extensible so that adding your own bank means adding a transaction subtype.

