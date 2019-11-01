from ipaddress import IPv4Address, IPv6Address, IPv4Network, IPv6Network

from django import template

from netaddr import EUI

from ..merge import MergedCell, SourceValue

register = template.Library()

PRE_TYPES = (IPv4Address, IPv6Address, IPv4Network, IPv6Network, EUI)


def render_value(value):
    return f'<pre>{str(value)}</pre>' if isinstance(value, PRE_TYPES) else str(value)


def render_source_value(source_value: SourceValue):
    return f'<li>{source_value.source}: {render_value(source_value.value)}</li>'


def render_invalid(mc: MergedCell):
    return f'<ul>{[render_source_value(sv) for sv in mc.values]}</ul>'


@register.simple_tag
def merged_column(mc: MergedCell):
    inner = render_value(mc.values[0]) if mc.valid else render_invalid(mc)
    return f'<td>{inner}</td>'
