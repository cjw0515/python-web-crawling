import logging

# DEBUG < INFO < *WARNING* < ERROR < CRITICAL


def logger(name):

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler(name + '.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

if __name__ == '__main__':
    mylogger = logging.getLogger("my")
    mylogger.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler()

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)
    mylogger.addHandler(stream_handler)
    #포맷 설정


    # file_handler = logging.FileHandler('my.log')
    # mylogger.addHandler(file_handler)
    mylogger.info("server start!!")