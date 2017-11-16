import time
import logging
import sys

import parser
from builder import Builder


LOGGER = logging.getLogger("idlewild")


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


def parse_idl(idl):
    try:
        LOGGER.info('Starting parsing')
        start = time.time()
        nodes = parser.parse(data)
        LOGGER.info('Parsing complete in [{}] ms'.format(
            (time.time()-start) / 3600
        ))
        return nodes
    except SyntaxError as se:
        LOGGING.error('Parse Error: {0}'.format(se))


def parse_and_build_idl(idl, resolver_mappings=None):
    nodes = parse_idl(idl)
    builder = Builder(resolver_mappings)
    LOGGER.info('Starting build')
    start_build = time.time()
    builder.build(nodes)
    LOGGER.info('Schema built in [{}] ms'.format(
        (time.time()-start_build) / 3600
    ))
    return builder.schema
    

if len(sys.argv) == 2:
    setup_logging()
    with open(sys.argv[1]) as f:
        data = f.read()
        schema = parse_and_build_idl(data)
        if schema is not None:
            print(schema)
else:
    print('Usage: idlewild [idl-file]')
    raise SystemExit
