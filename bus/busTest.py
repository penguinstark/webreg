import requests, json, csv, os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.animation import FuncAnimation
import numpy as np

url = "https://transloc-api-1-2.p.rapidapi.com/vehicles.json"
querystring = {
    "agencies": "1323",
    "geo_area": "40.504728,-74.448948|6000",
    "callback": "call"
}
with open('pass.txt') as f:
    key = f.readline()
    print(key)

headers = {
    "X-RapidAPI-Key": key,
    "X-RapidAPI-Host": "transloc-api-1-2.p.rapidapi.com"
}

fig, ax = plt.subplots()
scat = ax.scatter([], [], c='red')
route_colors = {}
img = mpimg.imread('map.png')
ax.imshow(img, extent=[-74.48, -74.41, 40.47, 40.54])

bus_scatters = {}
bus_positions = {}
bus_headings = {}

def init():
    ax.set_xlim(-74.48,-74.41)
    ax.set_ylim(40.47,40.54)
    # ax.set_xlim(-75,-74)
    # ax.set_ylim(40,41)
    bus_scatters.clear()
    return [scat] + list(bus_scatters.values())

with open('routes.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    rows = list(reader)

def route(id):
    for row in rows:
        if row[0] == id: return row[2]

def update(frame):
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        data = json.loads(response.text)
        lats, lngs, colors = [], [], []
        for key in data['data']:
            for vehicle in data['data'][key]:
                bus_id = vehicle['vehicle_id']
                route_id = vehicle['route_id']
                lat = vehicle['location']['lat']
                lng = vehicle['location']['lng']
                heading = vehicle['heading']
                lats.append(lat)
                lngs.append(lng)
                if route_id not in route_colors:
                    route_colors[route_id] = np.random.rand(3,)
                colors.append(route_colors[route_id])
                if bus_id not in bus_positions:
                    bus_positions[bus_id] = [(lng, lat)]
                    bus_headings[bus_id] = [heading]
                else:
                    bus_positions[bus_id].append((lng, lat))
                    bus_headings[bus_id].append(heading)
        scat.set_offsets(np.c_[lngs, lats])
        scat.set_color(colors)
    return scat,

ani = FuncAnimation(fig, update, frames=None, init_func=init, blit=True, interval=2000, cache_frame_data=False)

# fig = plt.figure(figsize=(10, 8))
# img = mpimg.imread('map.png')
# plt.imshow(img, extent=[-74.48, -74.41, 40.47, 40.54])
plt.show()