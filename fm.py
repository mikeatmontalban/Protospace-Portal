#
######################################################################
#
# Filter Interac email messages for:
#       greeting, containing the payer
#       Message:
#       Reference Number:
#
# 2018-09-13
#
######################################################################

import re

#mre = '.*Content-Type: text/plain;.*?PROTOSPACE LTD.,(.+)\s+ has.*?amount of (.+) and .*?Message:\s+(.*?)Reference Number\s+:\s+(\w+).*'

#mre = '.*Content-Type: text/plain;.*?PROTOSPACE LTD.,(.+?)\s+has.*?amount of (.+?) and .*?Message:(.+?)Reference Number\s+:\s+(\w+).*'
mre = '.*Content-Type: text/plain;.*?PROTOSPACE LTD.,(.+?)\s+has.*?amount of\s+(.+?\){1}).+?and\s+.*?Message:(.+?)Reference Number\s+:\s+(\w+).*'
mre = '.*Content-Type: text/plain;.*?PROTOSPACE LTD.,(.+?)\s+has.*?amount of\s+(.+?\){1}).*?Message:\s?(.+?)Reference Number\s+:\s+(\w+).*'

f = open("interac.10.txt")

m = f.read()

f.close()

s = re.search(mre,m)

if s is not None:
    print('Name: ' + s.group(1) + '\nAmount: ' + s.group(2) + '\nMessage: ' + s.group(3) + '\nReference Number: ' + s.group(4))
else:
    print('Not found.')
    
