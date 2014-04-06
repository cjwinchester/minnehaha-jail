from mechanize import Browser
from bs4 import *
import datetime
from time import *
import re

today = str(datetime.date.today().strftime("%Y-%m-%d"))

mech = Browser()

f = open('minn-jail-' + today + '.txt', 'wb')

mech.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

mech.set_handle_robots(False)

baseurl = "http://web.minnehahacounty.org:9000/dept/so/jail/jail_inmate_info.php?pageNum_rsGetInmate=0"

page = mech.open(baseurl)
html = page.read()
soup = BeautifulSoup(html)

last = soup.find(text="Last >|").parent
string = last['href']
num = re.search(r'pageNum_rsGetInmate=(\d+)', string)
ok = int(num.group(0).replace('pageNum_rsGetInmate=',''))

counter = 0

def CheckNone(x):
   if len(x):
       return x.string
   else:
       return ''

while counter <= ok:
    table = soup.find(text="display table for all inmates start ").parent.next_sibling.next_sibling
    for row in table.findAll('tr')[2:]:
        col = row.findAll('td')
        last = CheckNone(col[0])
        mid = CheckNone(col[1])
        first = CheckNone(col[2])
        print first, last
        number = CheckNone(col[3])
        in_date = CheckNone(col[4])
        in_time = CheckNone(col[5])
        facility = CheckNone(col[6])
        bond = CheckNone(col[7])
        charges = CheckNone(col[8])
        record = (last, first, mid, number, in_date, in_time, facility, bond, charges)
        joined = "\t".join(record) + "\n"
        f.write(joined)
    counter += 1
    sleep(5)
    if counter != ok+1:
        nextpage = mech.follow_link(text_regex="Next >")
        nexthtml = nextpage.read()
        soup = BeautifulSoup(nexthtml)

print "Done!"
f.flush()
f.close()