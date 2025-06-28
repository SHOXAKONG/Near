from drf_spectacular.extensions import OpenApiSerializerFieldExtension
from drf_spectacular.utils import extend_schema_field

@extend_schema_field({
    'type': 'object',
    'properties': {
        'latitude': {'type': 'number', 'format': 'double'},
        'longitude': {'type': 'number', 'format': 'double'},
    }
})
class PointFieldSerializerExtension(OpenApiSerializerFieldExtension):
    target_class = 'src.api.common.fields.PointFieldSerializer'

    def map_serializer_field(self, auto_schema, direction):
        return auto_schema._map_serializer_field(self.target, direction, self.get_schema())