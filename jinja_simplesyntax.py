# -*- coding: utf-8 -*-

import re

from collections import deque

from jinja2.ext import Extension



__version__ = '0.1.0'


class SimpleSyntaxExtension(Extension):

    line_statement_prefix = '%:'


    single_line_blocks = set([
        'import', 'extends', 'set', 'include', 'from', 'do', 'continue',
        'break', 'else', 'elif', 'pluralize'])



    def preprocess(self, source, name, filename=None):

        if self.environment.line_statement_prefix is not None:
            line_statement_prefix = self.environment.line_statement_prefix

            single_line_tags_re = re.compile(
                    r'^(\s*)'+line_statement_prefix+'(.*?)$', re.M)
            inline_content_re = re.compile(
                    r'^(\s*)'+line_statement_prefix+'(\w+) (.+?) \| (.+?)$', re.M)

            source = inline_content_re.sub(r'\1{% \2 \3 %}\4{% end\2 %}', source)
            source = single_line_tags_re.sub(r'\1{% \2 %}', source)


        if '{% end %}' in source:
            source = self.replace_short_end_statements(source)

        return source

    def replace_short_end_statements(self, source):

        block_pattern_re = re.compile(r'{% ?(\w+).*?%}')
        blocks =  block_pattern_re.finditer(source)
        stack = []
        added_offset = 0

        for block in blocks:

            name = block.group(1)

            if name in self.single_line_blocks:
                continue

            try:
                stack[0]
            except IndexError:
                if not name.startswith('end'):
                    stack.append(block)
                continue

            if not name.startswith('end'):
                stack.append(block)
                continue

            prev_block = stack.pop()

            #if its already a complete end tag there is no need to replace it.
            if name != 'end':
                continue

            new_end = '{% end'+prev_block.group(1)+ ' %}'

            source = source[:block.start()+added_offset] + new_end + source[block.end()+added_offset:]

            added_offset += len(new_end) - len(block.group(0))

        return source

