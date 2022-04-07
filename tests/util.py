def generic_serialize_roundtrip_test(cls, obj):
    json_data = obj.to_json()
    loaded = cls.from_json(json_data)
    print("LOADED ", loaded, "obj =>", obj)
    assert obj == loaded  # noqa
