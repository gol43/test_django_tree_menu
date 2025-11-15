from django import template
from django.template.loader import render_to_string
from .menu_utils import build_menu_tree

register = template.Library()

@register.simple_tag(takes_context=True)
def draw_menu(context, menu_slug):
    request = context['request']
    tree = build_menu_tree(menu_slug, request.path)
    return render_to_string('menu/menu_item.html', {'items': tree}, request=request)