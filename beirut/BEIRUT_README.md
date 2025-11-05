🗺️ Beirut Module — Quick Start README
This README captures exactly how to get the Beirut mapping module running inside your WHISPER_STREAMING project — from a clean setup to extracting Beirut streets & POIs.
🧩 1) Create and activate a virtual environment
From your project root (WHISPER_STREAMING/):
python3 -m venv .venv
source .venv/bin/activate   # macOS / Linux
# Windows (PowerShell)
# .venv\Scripts\Activate.ps1
You should see your prompt prefixed with:
(.venv)
⚙️ 2) Install requirements
Install the packages needed for the Beirut module:
pip install pyrosm geopandas shapely pyproj rapidfuzz folium
If you already have a requirements.txt file, simply run:
pip install -r requirements.txt
(Optional) Freeze your environment
To save your exact package versions for later:
pip freeze > requirements.txt
📁 3) What the beirut/ folder does
This folder contains everything related to offline Beirut place/streets search and map generation.
You’ll use it to power “voice → place → map pin” flows for fire dispatchers.
Folder structure
WHISPER_STREAMING/
├── .venv/                           # your virtual environment
├── beirut/
│   ├── lebanon-251104.osm.pbf       # Lebanon OSM extract (Geofabrik)
│   ├── extract_data.py              # extracts Beirut streets + POIs → GeoJSON
│   ├── beirut_search.py             # fuzzy search text → map pin (test script)
│   ├── beirut_streets.geojson       # (generated) streets in Beirut
│   ├── beirut_pois.geojson          # (generated) hotels, markets, hospitals, etc.
│   └── README.md                    # this file
├── whisper_online_server.py
├── whisper_online.py
└── ...
🧠 Files explained
🗺️ lebanon-251104.osm.pbf
The OpenStreetMap extract for all of Lebanon (downloaded from Geofabrik).
Used as the base dataset to extract Beirut-only information.
⚙️ extract_data.py
Reads the .pbf map file.
Locates the Beirut Governorate boundary (محافظة بيروت).
Extracts all streets and points of interest (POIs) within that boundary.
Exports:
beirut_streets.geojson
beirut_pois.geojson
🔍 beirut_search.py
Loads the generated .geojson files.
Performs fuzzy text matching on a hardcoded Arabic sentence (like “لانكستر الروشة”).
Finds the closest matching POI/street.
Saves an HTML map with a pin.
🌍 4) Download the OSM data (once)
Download Lebanon from Geofabrik
and place it inside the beirut/ folder.
Example:
lebanon-latest.osm.pbf → lebanon-251104.osm.pbf
Rename it if needed to match your script:
mv ~/Downloads/lebanon-latest.osm.pbf beirut/lebanon-251104.osm.pbf
🚀 5) Run the Beirut extractor
From inside the beirut/ folder:
python extract_data.py
Expected output (simplified):
⏳ Loading OSM map data for Lebanon...
📍 Locating Beirut boundary...
✅ Found Beirut boundary
🚗 Extracting street (road) network...
💾 Saved XXXX streets → beirut_streets.geojson
🏢 Extracting Points of Interest (POIs)...
💾 Saved XXXX POIs → beirut_pois.geojson
🎉 Extraction complete.
This generates the local GeoJSON datasets you’ll use for offline location search.
🧭 6) Test the search + map pin
Still inside beirut/:
python beirut_search.py
open beirut_result_map.html   # macOS
# On Windows, just double-click the file
This uses a sample Arabic phrase (e.g., “لانكستر الروشة”) to fuzzy-match a POI or street,
then opens a map with a location pin.
⚠️ Notes & Gotchas (and fixes)
❌ File not found
ValueError: File does not exist: Found: lebanon-latest.osm.pbf
Fix: Make sure the filename in your script matches the actual file in beirut/:
PBF_PATH = "lebanon-251104.osm.pbf"
❌ Beirut boundary not found
❌ Could not find 'Beirut' in the OSM dataset.
Fix: Use the Arabic name for the governorate in OSM:
beirut_area = osm.get_boundaries(name="محافظة بيروت")
❌ API change in Pyrosm (bounding box)
TypeError: OSM.get_network() got an unexpected keyword argument 'bounding_box' (or 'bbox')
Fix: In newer Pyrosm versions, pass the bounding box when creating the OSM instance,
not inside method calls:
osm_full = OSM(PBF_PATH)
beirut_area = osm_full.get_boundaries(name="محافظة بيروت")
beirut_bbox = beirut_area.total_bounds
osm = OSM(PBF_PATH, bounding_box=beirut_bbox)  # limit data to Beirut
streets = osm.get_network(network_type="driving")
pois = osm.get_pois(custom_filter=custom_filter)
🔮 Where to continue later
Hook beirut_search.py into your Whisper → GPT cleanup pipeline.
Expand coverage beyond محافظة بيروت (e.g., قضاء بعبدا, قضاء عاليه).
Add more POI categories (fuel, banks, schools) to custom_filter.
