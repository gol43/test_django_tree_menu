from django import template
register = template.Library()

@register.inclusion_tag('menu/menu_item.html', takes_context=True)
def draw_menu_recursive(context, items):
    return {'items': items}