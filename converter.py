from datetime import datetime
import glob
import os
import pathlib
import sys

from pelican.utils import slugify


if __name__ == '__main__':
    lektor_base_dir = 'export/'
    try:
        os.mkdir(lektor_base_dir)
    except FileExistsError:
        pass

    for filename in glob.iglob('./**/*.md'):
        basename = '.'.join(filename.split('/')[-1].split('.')[:-1])
        print('Processing {}'.format(basename))
        try:
            os.mkdir(pathlib.Path(lektor_base_dir) / basename)
        except FileExistsError:
            pass

        with open(filename, 'r') as pelican_file:
            content = pelican_file.readlines()

        try:
            header_delimiter = content.index('\n')
        except ValueError:
            continue

        blog_text = content[header_delimiter + 1:]
        header = {
            line.split(':')[0]: ':'.join(line.split(':')[1:]).strip()
            for line in content[:header_delimiter]
        }
        pub_date = header.get('Date')
        if not pub_date:
            pub_date = datetime.fromtimestamp(os.path.getmtime(filename)).strftime('%Y-%m-%d')

        lektor_header = [
            'title: {}'.format(header['Title']),
            '---',
            '_slug: {}'.format(slugify(header['Title'], ())),
            '---',
            'author: {}'.format(header.get('Authors', 'rixx')),
            '---',
            'summary: {}'.format(header.get('Summary', '')),
            '---',
            'pub_date: {}'.format(pub_date),
            '---',
            'body:', ''
        ]
        lektor_lines = [line + '\n' for line in lektor_header] + blog_text

        with open(pathlib.Path(lektor_base_dir) / basename / 'contents.lr', 'w') as lektor_file:
            lektor_file.writelines(lektor_lines)
