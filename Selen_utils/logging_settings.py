import logging
for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

logging.basicConfig(
            level=logging.INFO,
            format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
            datefmt="%d/%b/%Y %H:%M:%S",
            filename='debug.log', filemode='a')
