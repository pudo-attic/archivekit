from pkg_resources import iter_entry_points


def get_stores():
    stores = {}
    for ep in iter_entry_points('barn.stores'):
        stores[ep.name] = ep.load()
    return stores


def get_resource_types():
    types = {}
    for ep in iter_entry_points('barn.resource_types'):
        types[ep.name] = ep.load()
    return types
