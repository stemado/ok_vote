import mechanicalsoup

browser = mechanicalsoup.StatefulBrowser()

browser.open("https://former.okhouse.gov/Legislation/ShowVotes.aspx")
browser.launch_browser()