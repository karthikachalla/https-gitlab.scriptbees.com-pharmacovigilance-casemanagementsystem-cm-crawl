import logging
logging.basicConfig(filename='log.txt',level=logging.DEBUG,format='%(asctime)s:%(levelname)s:%(message)s',datefmt='%d-%m-%Y %I:%M:%s %p')
logging.info('A new request came')
try:
    x=int(input('Enter first number:'))
    y=int(input('Enter second number:'))
    print('The result:', x/y)
except ZeroDivisionError as message:
    print('cannot divide with zero')
    logging.exception(message)
except ValueError as message:
    print('please provide int values only')
    logging.exception(message)
    logging.info('Request processing completed')
    
