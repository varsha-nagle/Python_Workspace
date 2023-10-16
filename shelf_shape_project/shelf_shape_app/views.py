from rest_framework import viewsets
from rest_framework.response import Response
from .models import ShelfLayout
from .serializers import ShelfLayoutSerializer


def identify_shapes(layout):
    shapes = {'G': {'shape': '', 'location': []},
              'M': {'shape': '', 'location': []},
              'N': {'shape': '', 'location': []},
              'B': {'shape': '', 'location': []}}

    # Iterate through each product symbol (G, M, N, B)
    for symbol in ['G', 'M', 'N', 'B']:
        product_locations = []

        # Iterate through rows and columns to find the locations of the symbol
        for i in range(len(layout)):
            for j in range(len(layout[i])):
                if layout[i][j] == symbol:
                    product_locations.append((i, j))

        if not product_locations:
            continue

        # Determine if it's a vertical rectangle or horizontal rectangle
        x_coords, y_coords = zip(*product_locations)
        min_x, max_x = min(x_coords), max(x_coords)
        min_y, max_y = min(y_coords), max(y_coords)

        if min_x == max_x and min_y == max_y:
            shape = 'square'
        elif min_x == max_x:
            shape = 'vertical rectangle'
            location = ['left'] if min(y_coords) == 0 else ['right']
        elif min_y == max_y:
            shape = 'horizontal rectangle'
            location = ['top'] if min(x_coords) == 0 else ['bottom']
        else:
            shape = 'irregular polygon'
            location = []

        shapes[symbol] = {'shape': shape, 'location': location}

    return shapes


class ShelfLayoutViewSet(viewsets.ModelViewSet):
    queryset = ShelfLayout.objects.all()
    serializer_class = ShelfLayoutSerializer

    def create(self, request, *args, **kwargs):
        layout = request.data.get('layout', [])
        shapes = identify_shapes(layout)

        # If 'G' or 'M' is identified as a horizontal rectangle at the 'bottom',
        # update it to be a vertical rectangle on the 'left'.
        if shapes.get('G', {}).get('shape') == 'horizontal rectangle' and 'bottom' in shapes['G']['location']:
            shapes['G']['shape'] = 'vertical rectangle'
            shapes['G']['location'] = ['left']

        if shapes.get('M', {}).get('shape') == 'horizontal rectangle' and 'bottom' in shapes['M']['location']:
            shapes['M']['shape'] = 'vertical rectangle'
            shapes['M']['location'] = ['left']

        return Response(shapes)
