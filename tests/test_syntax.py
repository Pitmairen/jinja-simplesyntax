# -*- coding: utf-8 -*-

import unittest

from jinja_simplesyntax import SimpleSyntaxExtension


class Environment(object):
    line_statement_prefix = '%:'

class TestCase(unittest.TestCase):

    def setUp(self):
        self.simplesyntax = SimpleSyntaxExtension(Environment())

    def _p(self, source):
        return self.simplesyntax.preprocess(source, '<string>', '<string>')


    def test_extends(self):

        s = self._p('''%:extends "base.html"''')
        r = '''{% extends "base.html" %}'''

        self.assertEqual(s, r)

    def test_import(self):

        s = self._p('''%:import "test.html" as test''')
        r = '''{% import "test.html" as test %}'''

        self.assertEqual(s, r)

    def test_from_import(self):

        s = self._p('''%:from "test.html" import test''')
        r = '''{% from "test.html" import test %}'''

        self.assertEqual(s, r)

    def test_set(self):

        s = self._p('''%:set i=1''')
        r = '''{% set i=1 %}'''

        self.assertEqual(s, r)

    def test_do(self):

        s = self._p('''%:do test.append(1)''')
        r = '''{% do test.append(1) %}'''

        self.assertEqual(s, r)

    def test_continue(self):

        s = self._p('''%:continue''')
        r = '''{% continue %}'''

        self.assertEqual(s, r)

    def test_break(self):

        s = self._p('''%:break''')
        r = '''{% break %}'''

        self.assertEqual(s, r)


    def test_inline_content(self):

        s = self._p('''%:block test | Test content''')
        r = '''{% block test %}Test content{% endblock %}'''

        self.assertEqual(s, r)

    def test_inline_content(self):

        s = self._p('''%:if 1 == 43: | Test content''')
        r = '''{% if 1 == 43: %}Test content{% endif %}'''

        self.assertEqual(s, r)


    def test_line_block_end(self):

        s = self._p('''
%:if 1 == 43:
    Test content
%:else:
    Test content
%:end
''')
        r = '''
{% if 1 == 43: %}
    Test content
{% else: %}
    Test content
{% endif %}
'''

        self.assertEqual(s, r)

    def test_line_block_end2(self):

        s = self._p('''
%:for i in range(10):
    Test content
    %:if i == 32:
        Test content
    %:end
%:else:
    Test content
%:end
''')
        r = '''
{% for i in range(10): %}
    Test content
    {% if i == 32: %}
        Test content
    {% endif %}
{% else: %}
    Test content
{% endfor %}
'''

        self.assertEqual(s, r)

    def test_normal_block_end(self):

        s = self._p('''
{% if 1 == 43: %}
    Test content
{% elif: %}
    Test content
{% else: %}
    Test content
{% end %}
''')
        r = '''
{% if 1 == 43: %}
    Test content
{% elif: %}
    Test content
{% else: %}
    Test content
{% endif %}
'''

        self.assertEqual(s, r)

    def test_normal_block_end2(self):

        s = self._p('''
{% if 1 == 43: %}Test content{% else: %}Test content{% end %}
''')
        r = '''
{% if 1 == 43: %}Test content{% else: %}Test content{% endif %}
'''

        self.assertEqual(s, r)


    def test_trans(self):

        s = self._p('''
{% trans 23 %}
Test
{% pluralize %}
Tests
{% end %}
''')
        r = '''
{% trans 23 %}
Test
{% pluralize %}
Tests
{% endtrans %}
'''

        self.assertEqual(s, r)


    def test_mixed_end_and_lines(self):

        s = self._p('''
{% if 1 == 43: %}
    {% if 1 == 44: %}
        Test content
    {% endif %}
    Test content
{% elif: %}
    %:if 1 == 23:
        Test content
    %:end
    Test content
{% else: %}
    %:for i in range(10):
        {% if i == 3 %}
            Test content
        {% endif %}
    %:end
    Test content
{% end %}
''')
        r = '''
{% if 1 == 43: %}
    {% if 1 == 44: %}
        Test content
    {% endif %}
    Test content
{% elif: %}
    {% if 1 == 23: %}
        Test content
    {% endif %}
    Test content
{% else: %}
    {% for i in range(10): %}
        {% if i == 3 %}
            Test content
        {% endif %}
    {% endfor %}
    Test content
{% endif %}
'''

        self.assertEqual(s, r)

if __name__ == '__main__':

    unittest.main()