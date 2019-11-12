from typing import List, Tuple
from ipaddress import IPv4Address, IPv6Address, IPv4Network, IPv6Network

from django import template
from django.template.defaultfilters import safe

from netaddr import EUI

from ..merge import MergedCell, MergedRow, MergedTable, SourceValue

register = template.Library()

PRE_TYPES = (IPv4Address, IPv6Address, IPv4Network, IPv6Network, EUI)
LIST_TYPES = (list, tuple, set)


def render_value(value):
    if isinstance(value, PRE_TYPES):
        return f'<pre>{str(value)}</pre>'
    if isinstance(value, LIST_TYPES):
        return f'<ul>{"".join([f"<li>{str(v)}</li>" for v in value])}</ul>'
    return str(value)


def render_source_value(source_value: SourceValue):
    return f'<li>{source_value.source}: {render_value(source_value.value)}</li>'


def render_invalid(mc: MergedCell):
    return f'<ul>{"".join([render_source_value(sv) for sv in mc.values])}</ul>'


@register.simple_tag
def merged_cell(mc: MergedCell):
    if mc is None:
        return safe('<td>None</td>')
    inner = render_value(mc.values[0].value) if mc.valid else render_invalid(mc)
    class_name = 'valid' if mc.valid else 'invalid'
    order_attr = f' data-order="{mc.sort_order}"' if mc.sort_order is not None else ''
    return safe(f'<td class="{class_name}"{order_attr}>{inner}</td>')


@register.simple_tag
def merged_row(mr: MergedRow, cols: List[Tuple[str, str]], class_name=''):
    cells = [merged_cell(mr.cells.get(col[0])) for col in cols]
    return safe(f'<tr class="{class_name}">{"".join(cells)}</tr>')


@register.simple_tag
def merged_table(mt: MergedTable, class_name=''):
    headings = [
        f'<th>{c[1]}</th>'
        for c in mt.columns
    ]
    rows = [
        merged_row(mr, mt.columns)
        for mr in mt.rows.values()
    ]
    return safe(f'''
<table class="{class_name}">
    <thead>
        <tr>{"".join(headings)}</tr>
    </thead>
    <tbody>
        {"".join(rows)}
    </tbody>
</table>
''')
