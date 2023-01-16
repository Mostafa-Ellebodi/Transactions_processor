import logging

# remove intialized logger handlers
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Create and configure loggers
# info logger is created to log status, input and output and print to console
# error logger to track errors

# General logger that will log all 
logging.basicConfig(filename="./logs.log",
                    datefmt = '%m/%d/%Y %I:%M:%S %p',
                    format='[%(levelname)s]--%(asctime)s: %(message)s',
                    #filemode='w',
                    level = logging.INFO)

# creating console handler and info logger
console = logging.StreamHandler()
console.setLevel(logging.INFO)
infoLogger = logging.getLogger(name='info_logger')


# configuring info logger
formatter = logging.Formatter('[%(levelname)s]--%(asctime)s: %(message)s')
infofileHandler = logging.FileHandler("./info.log")
console.setFormatter(formatter)
infofileHandler.setFormatter(formatter)
infoLogger.addHandler(console)
infoLogger.addHandler(infofileHandler)
infoLogger.setLevel(logging.INFO)

# creating and configuring error logger
errformatter = logging.Formatter('[%(levelname)s]--%(asctime)s >> %(module)s line (%(lineno)d): %(message)s')
errorLogger = logging.getLogger(name='error_logger')
errorfileHandler = logging.FileHandler("./error.log")
errorfileHandler.setFormatter(errformatter)
errorLogger.addHandler(errorfileHandler)
errorLogger.setLevel(logging.ERROR)