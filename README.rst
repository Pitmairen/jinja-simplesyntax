========================
jinja-simplesyntax
========================

Overview
========

This extension to jinja make it posible to end tags
with just "end" instead of endif, endfor and so on.

It also works with line statements.


Usage
=====

::

    from jinja2 import Environment
    from jinja_simplesyntax import SimpleSyntaxExtension

    env = Environment(
			line_statement_prefix='%:'
			extensions=[SimpleSyntaxExtension])


Example
=======

::

	{% for i in range(10): %}
		{% if i == 0 %}
			First
		{% else %}
			{{ i }}
		{% end %}
	{% end %}



With line statements its also posible to use inline content
like this:

::

	%:block title | This is the title

	%:if True | Yes it's true

This becomes:
::

	{% block title %}This is the title{% endblock %}

	{% if True %}Yes it's true{% endif %}
