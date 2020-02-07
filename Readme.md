**Minemydata**

This project attempts to see whether Hong Kong SFC licensee holders are awarded enough disciplinary actions. Information about licensee holders and their disciplinary actions are publically available on the SFC website. However, there is no consolidated list of all licensee holders or disciplinary actions.
The approach used in this project is to start from David Webb's Webb-Site. Webb-site has a large and well-organized database of companies and license holders which is a good starting point for such a project.

The project is split into four steps - 
  1. Scraping the leaguetable from Webb-site (https://webb-site.com/dbpub/SFClicount.asp). The resulting table is called LeagueTable.csv and it includes an extra column for the hyperlink underlying the company names.
  2. Step 2 is to go through each row of the league table and scrape the hyperlink for each company. An example table can be seen at this hyperlink: https://webb-site.com/dbpub/SFClicensees.asp?p=1464&a=0&h=Y&sort=posdn&d=2020-02-07. A csv is generated for each company of the league table in the Officers folder. Multiple csv's are used instead of one concatenated file as the data would be too long otherwise. Hyperlinks to each officer's page on Webb-site is also added to each table.
  3. Next, each company's table is updated with each officer's SFC ID and the hyperlink to their SFC page. https://webb-site.com/dbpub/natperson.asp?p=115355 is an example.
  4. Last, each company's file is cycled through and each officer's SFC page's disciplinary action section (https://www.sfc.hk/publicregWeb/indi/ALS080/disciplinaryAction) is scraped. The disciplinary action table is looked for any entries and if there are none, the word 'None' is added to the column 'DiscAct'.
