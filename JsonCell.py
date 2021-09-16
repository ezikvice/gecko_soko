import json


class JsonCell:
    r = 0
    c = 0
    objects = []

    def __init__(self, r, c):
        self.r = r
        self.c = c


class JsonCellEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, JsonCell):
            return {
                'r': obj.r,
                'c': obj.c,
                'objects': [ob.obj_id for ob in obj.objects]
            }
        return json.JSONEncoder.default(self, obj)
