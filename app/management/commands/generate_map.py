import folium
import json
from django.core.management.base import BaseCommand
from app.models import Country

class Command(BaseCommand):
    help = 'Generate a map with country risk levels and interactivity'

    def handle(self, *args, **kwargs):
        # Load GeoJSON data
        geojson_file_path = 'C:/Users/pauli/PycharmProjects/AAA_draudiklis/app/management/commands/map/countries.geojson'  # Replace with the actual path to your GeoJSON file
        with open(geojson_file_path, 'r', encoding='utf-8') as f:
            geojson_data = json.load(f)

        # Create a map centered around the world
        m = folium.Map(location=[0, 0], zoom_start=2)

        # Define a function to get the risk level color
        def get_color(risk_level):
            colors = {
                'Low': 'green',
                'Medium': 'yellow',
                'High': 'orange',
                'Very High': 'red',
                'Extreme': 'black'
            }
            return colors.get(risk_level, 'gray')

        # Prepare a dictionary with country risk levels
        country_risk_levels = {country.name: country.risk_level for country in Country.objects.all()}

        # Define the style function
        def style_function(feature):
            return {
                'fillColor': get_color(country_risk_levels.get(feature['properties']['NAME'], 'Unknown')),
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.7,
            }

        # Define the highlight function
        def highlight_function(feature):
            return {
                'fillColor': '#000000',
                'color': '#000000',
                'fillOpacity': 0.1,
                'weight': 0.1,
            }

        # Add GeoJSON to the map with interactivity
        folium.GeoJson(
            geojson_data,
            style_function=style_function,
            highlight_function=highlight_function,
            tooltip=folium.GeoJsonTooltip(fields=['NAME'], aliases=['Country:']),
            name='geojson'
        ).add_to(m)

        # Add custom JavaScript to handle clicks
        click_js = """
        function(e) {
            var country = e.target.feature.properties.NAME;
            window.location.href = "/calculate/?country=" + country;
        }
        """

        # Attach the click event to the map
        folium.LayerControl().add_to(m)
        folium.Element("""
        <script>
            var geojson = geojson;  // Reference the geojson layer by its name
            geojson.eachLayer(function (layer) {
                layer.on('click', """ + click_js + """);
            });
        </script>
        """).add_to(m.get_root())

        # Save the map to an HTML file
        output_file = 'country_map.html'
        m.save(output_file)
        self.stdout.write(self.style.SUCCESS(f'Map has been generated and saved to {output_file}'))
