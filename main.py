# Import required libraries
from flask import Flask, send_file
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.patches import Patch
from apscheduler.schedulers.background import BackgroundScheduler
import geopandas as gpd
import matplotlib.pyplot as plt
import io
import requests
import subprocess
import logging
import os
from datetime import datetime, timedelta

IP_API = os.getenv('IP_API', 'https://api.ipify.org')
GEO_IP_API = os.getenv('GEO_IP_API', 'https://freegeoip.app/json/')
IMAGE_GEN_INTERVAL = int(os.getenv('IMAGE_GEN_INTERVAL', 90)) 

# Create a logs directory if not exists
if not os.path.exists('logs'):
    os.makedirs('logs')

# Initialize logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] - %(message)s',
                    handlers=[logging.FileHandler('logs/debug.log'), logging.StreamHandler()])
logger = logging.getLogger('iptables2worldchartlogger')

# Initialize Flask application
application = Flask(__name__)

# Initialize map as a global variable
world_map_image = None
cache_time = None

# Function to parse IPtables rules
def get_iptables_countries():
    # Get iptables rules
    iptables_output = subprocess.run(['sudo', 'iptables', '-L'], capture_output=True, text=True).stdout

    # Parse rules to get countries
    blocked_countries = []

    for line in iptables_output.split('\n'):
        if '--source-country ' in line:
            country = line.split('--source-country ')[1][:2]
            if 'DROP' in line:
                blocked_countries.append(country)

    # Load a GeoDataFrame from a shapefile (downloaded from https://www.naturalearthdata.com/downloads/110m-cultural-vectors/110m-admin-0-countries/)
    world = gpd.read_file('ne_110m_admin_0_countries.shp')

    # Get all the countries from the geopandas dataframe
    all_countries = world['ISO_A2'].tolist()

    # Assume that any country not in the blocked list is allowed
    allowed_countries = [country for country in all_countries if country not in blocked_countries]
    print(allowed_countries)

    return allowed_countries, blocked_countries

def generate_image():
    global world_map_image, cache_time

    logger.info("Starting image generation")

    # Get server's public IP address
    server_country = 'NL'

    # Parse IPtables rules to get allowed and blocked countries
    allowed_countries, blocked_countries = get_iptables_countries()
    # Load a GeoDataFrame from a shapefile (downloaded from https://www.naturalearthdata.com/downloads/110m-cultural-vectors/110m-admin-0-countries/)
    world = gpd.read_file('ne_110m_admin_0_countries.shp')
    # Add a new column to the GeoDataFrame indicating whether each country is allowed, blocked, or the server country
    world['status'] = world['ISO_A2'].apply(lambda x: 'allowed' if x in allowed_countries else 'blocked')
    fig, ax = plt.subplots(1, 1, dpi=400)

    world[world['status'] == 'blocked'].plot(ax=ax, color='red')
    
    if 'allowed' in world['status'].values:
        world[world['status'] == 'allowed'].plot(ax=ax, color='green')
    
    ax.axis('off')

    # Create legend
    legend_elements = [Patch(facecolor='green', edgecolor='black', label='Allowed'),
                       Patch(facecolor='red', edgecolor='black', label='Blocked'),
                       Patch(facecolor='purple', edgecolor='black', label='Server')]
    ax.legend(handles=legend_elements, loc='lower left')

    # Add generation time to image
    gen_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ax.text(1, 0, f"Generated at: {gen_time}", color='black',
            bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'),
            horizontalalignment='right', verticalalignment='bottom', transform=ax.transAxes)

    png_image = io.BytesIO()
    FigureCanvas(fig).print_png(png_image)
    world_map_image = png_image.getvalue()
    cache_time = datetime.now()

    logger.info("Image generation completed")

@application.route('/')
def home():
    global world_map_image, cache_time

    return send_file(io.BytesIO(world_map_image), mimetype='image/png')

scheduler = BackgroundScheduler()
scheduler.add_job(generate_image, 'interval', minutes=IMAGE_GEN_INTERVAL)
scheduler.start()

generate_image()

if __name__ == '__main__':
    application.run(debug=True)
