def build_menu_tree(menu_slug, current_path):
    from ..models import MenuItem

    items = MenuItem.objects.select_related('menu', 'parent').filter(menu__slug=menu_slug)
    item_map = {}
    root_items = []
    active_item = None
    active_path = set()

    # Находим активный пункт
    for item in items:
        url = item.get_url()
        if url != '#' and current_path.startswith(url):
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
        item_map[item.id] = {
            'item': item,
            'children': [],
            'is_active': item.id == (active_item.id if active_item else None),
            'is_in_path': item.id in active_path,
            'is_expanded': False,
        }

    for node in item_map.values():
        item = node['item']
        if item.parent_id and item.parent_id in item_map:
            item_map[item.parent_id]['children'].append(node)
        else:
            root_items.append(node)

    # Развёртка
    def mark_expanded(nodes):
        for node in nodes:
            if node['is_in_path']:
                node['is_expanded'] = True
                if node['is_active']:
                    for child in node['children']:
                        child['is_expanded'] = True
                mark_expanded(node['children'])

    mark_expanded(root_items)
    return root_items