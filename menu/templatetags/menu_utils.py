from menu.models import MenuItem


def build_menu_tree(menu_slug, current_path):

    # 1 SQL-запрос: все items с related
    items = MenuItem.objects.select_related('parent', 'menu').filter(menu__slug=menu_slug)
    item_map = {}
    root_items = []
    active_item = None
    active_path = set()

    # Активный по URL
    for item in items:
        url = item.get_url()
        if url != '#' and current_path.startswith(url.rstrip('/')):
            if active_item is None or len(url) > len(active_item.get_url()):
                active_item = item

    # Путь до активного
    if active_item:
        cur = active_item
        while cur:
            active_path.add(cur.id)
            cur = cur.parent

    # Строим дерево
    for item in items:
        node = {
            'item': item,
            'children': [],
            'is_active': item.id == (active_item.id if active_item else None),
            'is_in_path': item.id in active_path,
            'is_expanded': False,
        }
        item_map[item.id] = node

    for node in item_map.values():
        if node['item'].parent_id and node['item'].parent_id in item_map:
            item_map[node['item'].parent_id]['children'].append(node)
        else:
            root_items.append(node)

    # Развёртка: путь + 1 уровень под активным
    def mark_expanded(nodes):
        for node in nodes:
            if node['is_in_path']:
                node['is_expanded'] = True
                if node['is_active']:
                    for child in node['children']:
                        child['is_expanded'] = True  # Только 1 уровень
                mark_expanded(node['children'])

    mark_expanded(root_items)
    return root_items