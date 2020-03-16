Bank Simulation GUI BUilt with Python's Tkinter framework/library.
It is supported by a SQLite database that holds it's data and feeds it accordingly.
Functions are: Add new bank customer, Search customer table for a customer, view all customers, update a customers details,delete a customer, Credit a customers account and debit a customers account.
Using SQLites auto increment feature, a new unique Custoemer ID is generated for every new user as well as a new unique Account number. 
A balance of 0 is automatically entered for everx new customer.
RegularExpressions: For data consistency and integrity, regular expressions where used to control possible entries. Clear messages are returned to the user when any of their entries fail the regular expression. 
Post Code and Phone numbers: Since these vary in format from country to country, a table is used to hold the regular expressions of phone numbers and postcodes for each county. Depending on the country of the user, the coressponding regular expression is fetched from the table and the phone number and post code values passed through them. 
All other fields use the same regular expressions irrepective of country.
The same table also contains a column hoilding the international dial codes of each country and is automatically returned for selected country. It is concatinated with the rest of the number entered in the mobile field in the database.
Current balance is checked before every possible withdrawal. Withdrawal cannot be greater than current balance.
Accounts table: For every new customer, a new unique account number is generated and stored ion the Accounts table. The CIid column in this table is a foreign key reference to the Customer table.
Transactions table: Every credit and debit made to and from all accounts respectively are recorded in this table. Additionally, when a user leaves the bank, the system assumes the withdrawal of their current balance and records it here.
InfoTable table: Discussed earlier, contains dial code as well as phone and post code regular expressions of each country. They are fetched accordingly during every addition and update of customer information.
CustomerArchive table: Automatically updated when new user is added or existing user is updated. When user leaves the bank, they are removed from the Customer table but remain in this table. Their last known information, including final balanmce before leaving are stored here.
Customer table: Contains information of all customers as well as current balance.
Customer and Transaction views: When a user is clicked on in the bigger display that shows all customers, all thei credit and debit history is displayed on the smaller display below it. We can easily use this secondary display for other purposes or even show only the last or first x transactions.
Using logic and TRY statements, all known possible errors have been caught to return an intuitive and specific message. Although further testing can always reveal more uncaptured errors.
Intuitive and vry specific messages are returned all accross the system for ease of use.
FURTHER WORK: Establish a second optional type of bank account and incorporate it into the system, etc.
