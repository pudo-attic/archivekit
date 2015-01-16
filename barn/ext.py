from pkg_resources import iter_entry_points


def get_stores():
    stores = {}
    for ep in iter_entry_points('barn.stores'):
        stores[ep.name] = ep.load()
    return stores
