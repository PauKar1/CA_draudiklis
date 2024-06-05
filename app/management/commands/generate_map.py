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
        def get_color(map_risk):
            return {
                'Low': 'green',
                'Medium': 'yellow',
                'High': 'orange',
                'Very High': 'red',
                'Extreme': 'black'
            }.get(map_risk, 'gray')

        # Prepare a dictionary with country risk levels
        country_risk_levels = {country.name: country.map_risk for country in Country.objects.all()}

        # Style function
        def style_function(feature):
            return {
                'fillColor': get_color(country_risk_levels.get(feature['properties']['NAME'], 'Unknown')),
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.7,
            }

        # Highlight function for borders
        def highlight_function(feature):
            return {
                'fillColor': get_color(country_risk_levels.get(feature['properties']['NAME'], 'Unknown')),
                'color': 'blue',
                'weight': 3,
                'fillOpacity': 0.7,
            }

        # Add GeoJSON to the map with interactivity
        geojson = folium.GeoJson(
            geojson_data,
            style_function=style_function,
            highlight_function=highlight_function,
            tooltip=folium.GeoJsonTooltip(fields=['NAME'], aliases=['Country:']),
        ).add_to(m)

        # Add click event to highlight borders
        geojson.add_child(folium.features.GeoJsonPopup(fields=['NAME']))

        # Save the map to an HTML file
        output_file = 'country_map.html'
        m.save(output_file)
        self.stdout.write(self.style.SUCCESS(f'Map has been generated and saved to {output_file}'))
