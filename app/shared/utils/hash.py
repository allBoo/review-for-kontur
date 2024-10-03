

def get_object_hash(obj: object, keys: list[str]) -> str:
    return '-'.join([str(getattr(obj, key)) for key in keys])
