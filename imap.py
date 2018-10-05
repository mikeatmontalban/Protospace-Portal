import getpass, imaplib

import re

mre = '.*Content-Type: text/plain;.*?PROTOSPACE LTD.,(.+)\s+ has.*?amount of (.+) and .*?Message:\s+(.+)Reference Number\s+:\s+(\w+).*'
mre = '.*Content-Type: text/plain;.*?PROTOSPACE LTD.,(.+?)\s+has.*?amount of (.+?) and .*?Message:(.+?)Reference Number\s+:\s+(\w+).*'
mre = '.*Content-Type: text/plain;.*?PROTOSPACE LTD.,(.+?)\s+has.*?amount of\s+(.+?\){1}).+?and\s+.*?Message:(.+?)Reference Number\s+:\s+(\w+).*'
mre = '.*Content-Type: text/plain;.*?PROTOSPACE LTD.,(.+?)\s+has.*?amount of\s+(.+?\){1}).*?Message:\s?(.+?)Reference Number\s+:\s+(\w+).*'

M = imaplib.IMAP4_SSL("morrow.pl")
M.login(getpass.getuser(),getpass.getpass())
M.select("protospace/interac",True)
typ, data = M.search(None, '(SUBJECT "[dl-info] INTERAC e-Transfer: A money transfer from")' )

for num in data[0].split():
    typ, data = M.fetch(num, '(BODY[TEXT])')

#    message = open("interac." + str(num) + ".txt","w")
#    message.write('Message %s\n%s\n' % (num, data[0][1]))
#    message.close()

    s = re.search(mre,str(data[0][1]))

    if s is not None:
        name = s.group(1)
        amount = s.group(2)
        message = s.group(3)
        reference_number = s.group(4)
        print('\n\nName: ' + name + '\nAmount: ' + amount + '\nMessage: ' + message + '\nReference Number: ' + reference_number)

    else:
        print('\n\nNot found.')
    
M.close()
M.logout()


