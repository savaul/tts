#!/usr/bin/env python
import getpass, imaplib
import email
M = imaplib.IMAP4_SSL('imap.gmail.com')
M.login('savusfridge@gmail.com','frigider')
M.select('inbox')
rezumat=""
#print "****************************"
rezumat=rezumat+"****************"+"\n"
def get_first_text_block( email_message_instance):
    maintype = email_message_instance.get_content_maintype()
    if maintype == 'multipart':
	start=str(email_message_instance).find('text/plain')
	start=str(email_message_instance).find ('quoted-printable', start)
	return str(email_message_instance)[start+17:start+117]
    elif maintype == 'text':
        return email_message_instance.get_payload()

    else:
	return "nu pot decodifica"	

result, data_raw = M.uid('search', None, "UNSEEN") # search and return uids instead
length=len(data_raw[0].split( ))
if length==0:
	#print "no new messages"
	#print "****************************"
	rezumat=rezumat+"no new messages"+"\n"+"****************"
for i in range(length, 0, -1): 
	latest_email_uid = data_raw[0].split()[i-1]
	#print latest_email_uid
#	result, data = M.uid('fetch', latest_email_uid, '(BODY[HEADER.FIELDS (SUBJECT)])')
	result, data = M.uid('fetch', latest_email_uid, '(RFC822)')
	#print data[0][1] 
	raw_email = data[0][1]
	email_message = email.message_from_string(raw_email)
 
#print email_message['To']
 
	from_str=str(email.utils.parseaddr(email_message['From'])) # for parsing "Yuji Tomita" <yuji@grovemade.com>
#	start=from.find(')
	end=from_str.find("'", 2)
	#print "de la: "+from_str[2:end]
	rezumat=rezumat+"de la: "+from_str[2:end]+"\n"
	result, subject=M.uid('fetch', latest_email_uid, '(BODY[HEADER.FIELDS (SUBJECT)])')
	#print str(subject[0][1])
	rezumat=rezumat+str(subject[0][1])+"\n"
	ms= get_first_text_block(email_message)
	end=ms.find('\n', 100)
	#print end
	if end ==-1:
		#print ms[0: 100]
		rezumat=rezumat+ms[0: 100]+"\n"
	else:
		#print ms[0:end]
		rezumat=rezumat+ms[0:end]+"\n"
####	M.uid('STORE',latest_email_uid, '+FLAGS', '\\SEEN')

	#print "****************************"
	rezumat=rezumat+"****************"+"\n"

rezumat=rezumat.replace("\r", "\n")

#rezumat='GGGGGGG'.join(rezumat.split("\n"))
while rezumat.find("\n\n")!=-1:
#	print rezumat.find("\n")
	rezumat=rezumat.replace("\n\n", "\n")
print rezumat
#print rezumat.find("\n\n")
#
#with open("rezumat.txt", "w") as myfile:
#
#    myfile.write(rezumat)

M.close()
M.logout()


