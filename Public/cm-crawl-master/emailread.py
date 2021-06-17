import sched
import time
import datetime
from imap_tools import MailBox, AND
import logging.config
import logging.handlers
from config import LOGGING_CONFIG,LOGGER_NAME
from dotenv import load_dotenv
import os
import sys
import uuid
import requests
import json

load_dotenv()  # take environment variables from .env.

logging.config.dictConfig(LOGGING_CONFIG)
logger=logging.getLogger(LOGGER_NAME)

smtp=logging.handlers.SMTPHandlers(mailhost='server',fromaddr='readmail@example.com',toaddr=['mail@example.com'],subject='readmail',credentials=('user','pwd'),secure=None)

logger.addHandler(smtp)
logger.info("logger configured")

LOGGER_NAME="emailread"
LOGGING_CONFIG=dict(version=1,disable_existing_loggers=True,formatters={'verbose':{'format': '{}-%(asctime)s-%(filename)s-%(module)s-%(funcName)s-%(lineo)d-[%(levelname)s]-%(message)s'.format(uuid.uuid4())}})
handlers={'log_file':{'level':'DEBUG','class':'logging.StreamHandler','formatter': 'verbose','stream':sys.stdout,'filename':'logging.lo'}}
loggers={LOGGER_NAME:{'handlers': ['log_file'],'level':'DEBUG','propagate':False}}



imap_server=os.environ.get('IMAP_SERVER')
imap_port=os.environ.get('IMAP_PORT')
imap_email=os.environ.get('IMAP_EMAIL')
imap_password=os.environ.get('IMAP_PASSWORD')
node_api_url=os.environ.get('NODE_API_URL')
file_stoarge=os.environ.get('FILE_STORAGE')



mailbox = MailBox(imap_server,port=imap_port,starttls=False)
mailbox.login(imap_email, imap_password, initial_folder='INBOX')  # or mailbox.folder.set instead 3d arg
def job():
  mydate = datetime.datetime.now() - datetime.timedelta(days=1)
  print(mydate.date())
  subjects=[]
  for msg in mailbox.fetch(AND(seen=False,date_gte=mydate.date())):
      case={}
      case['reportedDate']= msg.date_str
      case['routeOfEnquiryId']=2
      case['receievedDate']=msg.date_str
      case['caseDescription']=msg.text
      case['caseSubject']=msg.subject
      case['caseStatus']= "Open"
      case['reporterEmail']= msg.from_
      case['files']=[]
      subjects.append(msg.subject)
      for att in msg.attachments:  # list: imap_tools.MailAttachment
          # Creating a file at specified location
          with open(os.path.join(file_stoarge, att.filename), 'wb') as fp:
            # To write data to new file uncomment
            # this fp.write("New file created")
            fp.write(att.payload)
         
          case['files'].append(att.filename)
          print(att.filename)             # str: 'cat.jpg'
          #print(att.payload)              # bytes: b'\xff\xd8\xff\xe0\'
          print(att.content_id)           # str: 'part45.06020801.00060008@mail.ru'
          print(att.content_type)         # str: 'image/jpeg'
          print(att.content_disposition)  # str: 'inline'
          #print(att.part)                 # email.message.Message: original object
          print(att.size)   
      r = requests.post(node_api_url, data=json.dumps(case))
      print(r.status_code)
  print(subjects)
  #Send the request to API using JSON
  


schedule.every(30).seconds.do(job)

while 1:
    n = schedule.idle_seconds()
    if n is None:
        # no more jobs
        break
    elif n > 0:
        # sleep exactly the right amount of time
        time.sleep(n)
    schedule.run_pending()
