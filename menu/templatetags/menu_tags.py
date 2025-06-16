from django import template
from ..models import MenuItem
from collections import defaultdict

register = template.Library()

@register.inclusion_tag('menu/template.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    menu_items = MenuItem.objects.filter(menu__name=menu_name).order_by('order')
    
    if not menu_items:
        return {'menu_tree': []}
    
    items_dict = {item.id: item for item in menu_items}
    children_dict = defaultdict(list)
    for item in menu_items:
        children_dict[item.parent_id].append(item)
    
    active_item = None
    for item in menu_items:
        if item.get_url() == request.path:
            active_item = item
            break
    
    expanded_ids = set()
    if active_item:
        current = active_item
        while current:
            expanded_ids.add(current.id)
            current = items_dict.get(current.parent_id)
    
    def build_tree(parent_id):
        return [
            {
                'item': item,
                'children': build_tree(item.id),
                'is_expanded': item.id in expanded_ids,
                'is_active': item.id == getattr(active_item, 'id', None)
            }
            for item in children_dict[parent_id]
        ]
    
    return {'menu_tree': build_tree(None)}