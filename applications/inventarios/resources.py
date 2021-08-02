from import_export import resources
from .models import Productos

class ProductosRecursos(resources.ModelResource):
    class Meta:
        model = Productos