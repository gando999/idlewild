import sys

import parser
from builder import Builder


if len(sys.argv) == 2:
    with open(sys.argv[1]) as f:
        data = f.read()
        try:
            nodes = parser.parse(data)
            builder = Builder()
            builder.build(nodes)
        except SyntaxError as se:
            print('Parse Error: {0}'.format(se))
else:
    print('Usage: idlewild [idl-file]')
    raise SystemExit
