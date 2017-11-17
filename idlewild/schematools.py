import time
import logging
import sys

import idlewild.parser as parser
from idlewild.builder import Builder


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
        nodes = parser.parse(idl)
        LOGGER.info('Parsing complete in [{}] ms'.format(
            (time.time()-start) / 3600
        ))
        return nodes
    except SyntaxError as se:
        LOGGER.error('Parse Error: {0}'.format(se))


def build_idl_schema(
        nodes,
        resolver_mappings=None,
        interface_resolver_mappings=None):
    builder = Builder(
        resolver_mappings, interface_resolver_mappings
    )
    LOGGER.info('Starting build')
    start_build = time.time()
    builder.build(nodes)
    LOGGER.info('Schema built in [{}] ms'.format(
        (time.time()-start_build) / 3600
    ))
    return builder.schema


def parse_and_build_idl(
        idl,
        resolver_mappings=None,
        interface_resolver_mappings=None):
    nodes = parse_idl(idl)
    return build_idl_schema(
        nodes, resolver_mappings, interface_resolver_mappings
    )


def parse_idl_file(filename):
    LOGGER.info('Loading IDL from {}'.format(filename))
    with open(filename) as f:
        data = f.read()
        return parse_idl(data)


def parse_and_build_idl_file(
        filename,
        resolver_mappings=None,
        interface_resolver_mappings=None):
    LOGGER.info('Building schema from {}'.format(filename))
    nodes = parse_idl_file(filename)
    return build_idl_schema(
        nodes, resolver_mappings, interface_resolver_mappings
    )


if __name__ == '__main__':
    if len(sys.argv) == 2:
        setup_logging()
        schema = parse_and_build_idl_file(sys.argv[1])
        LOGGER.info('Parsed and validated schema')
    else:
        print('Usage: schematools [idl-file]')
        raise SystemExit
