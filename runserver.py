#!/usr/bin/env python

#-----------------------------------------------------------------------
# runserver.py
# Authors: Shelby Fulton, Matthew Barrett, Jessica Lin, Alfred Ripoll
#-----------------------------------------------------------------------

import sys
import timemanager
import argparse


def main():
    parser = argparse.ArgumentParser(
        description='The calendar application')
    parser.add_argument('port', type=int,
                        help='the port at which the'
                        ' server should listen')
    port = parser.parse_args().port

    try:
        timemanager.app.run(host='localhost', port=port, debug=True)
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

# ----------------------------------------------------------------------

if __name__ == '__main__':
    main()
