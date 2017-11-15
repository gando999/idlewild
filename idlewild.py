import logging
import sys

import parser
from builder import Builder


def setup_logging(logfile_name=None):
    logger = logging.getLogger()
    ch = (
        logging.FileHandler(logfile_name) if logfile_name
        else logging.StreamHandler()
    )
    logger.setLevel(logging.INFO)
    ch.setLevel(logging.INFO)
    format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(format_string)
    ch.setFormatter(formatter)
    logger.addHandler(ch)


if len(sys.argv) == 2:
    setup_logging()
    with open(sys.argv[1]) as f:
        data = f.read()
        try:
            nodes = parser.parse(data)
            builder = Builder()
            builder.build(nodes)
            schema = builder.schema
            if schema is not None:
                print(schema)
        except SyntaxError as se:
            print('Parse Error: {0}'.format(se))
else:
    print('Usage: idlewild [idl-file]')
    raise SystemExit
