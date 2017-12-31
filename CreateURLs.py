"""
Quick and dirty script to create a number of URLs. We need to create a large number of
(content free) URLs to test the best way of bulk retrieval.
"""

import argparse
import jinja2
import os
import logging

if __name__ == '__main__':

    ap = argparse.ArgumentParser(description='Create URLs')
    ap.add_argument('--target', metavar='directory', help='Target directory', default='/var/www/html/')
    ap.add_argument('--template', metavar='file', help = 'jinja2 template HTML file', default='urltemplate.html')
    ap.add_argument('--urllist', metavar='file', help = 'URL list file', default='urllist.txt')
    ap.add_argument('--urlprefix', metavar='prefix', help='URL prefix', default='http://merlin')
    ap.add_argument('--number', metavar='n', help='Number of URLs to create', default=100)
    args = ap.parse_args()
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s: %(levelname)8s %(message)s')

    environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()), trim_blocks=True)
    template = environment.get_template(os.path.split(args.template)[1])

    try:
        with open(args.urllist, 'w') as urllist:
            for i in range(args.number):
                filename = 'url{:08d}.html'.format(i)
                pathname = os.path.join(args.target, filename)
                url = os.path.join(args.urlprefix, filename)
                try:
                    with open(pathname, 'w') as htmlfile:
                        htmlfile.write(template.render(i = i))
                except (PermissionError, IOError) as e:
                    logging.critical("Can't open {} for writing: {}".format(pathname, e))
                else:
                    urllist.write('{}\n'.format(url))
    except (PermissionError, IOError) as e:
        logging.critical("Can't open {} for writing: {}".format(args.urllist, e))


