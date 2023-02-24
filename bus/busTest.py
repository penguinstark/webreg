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
headers = {
    "X-RapidAPI-Key": "8ef2058ea0msha740dd60a3b95abp173661jsn6c955e38b6ff",
    "X-RapidAPI-Host": "transloc-api-1-2.p.rapidapi.com"
}

fig, ax = plt.subplots()
scat = ax.scatter([], [], c='red')
route_colors = {}
img = mpimg.imread('map.png')
ax.imshow(img, extent=[-74.48, -74.41, 40.47, 40.54])
scats = {}

with open('routes.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    rows = list(reader)

def route(id):
    for row in rows:
        if row[0] == id: return row[2]

previous = {}

def init():
    ax.set_xlim(-74.48,-74.41)
    ax.set_ylim(40.47,40.54)
    global trails
    trails = {}
    return scats.values(), previous

def update(frame):
    global previous
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        data = json.loads(response.text)
        lats, lngs, colors = [], [], []
        for key in data['data']:
            for vehicle in data['data'][key]:
                route_id = vehicle['route_id']
                lat = vehicle['location']['lat']
                lng = vehicle['location']['lng']
                if route_id not in route_colors:
                    route_colors[route_id] = np.random.rand(3,)
                colors.append(route_colors[route_id])
                
                if vehicle['vehicle_id'] in previous:
                    # shrink the size of the previous point by 2
                    ax.collections[previous[vehicle['vehicle_id']]].set_sizes([s/2 for s in ax.collections[previous[vehicle['vehicle_id']]].get_sizes()])
                    
                    # remove the previous point if the maximum number of points has been reached
                    if len(trails[vehicle['vehicle_id']]) == 5:
                        ax.collections.pop(previous[vehicle['vehicle_id']])
                        trails[vehicle['vehicle_id']].pop(0)
                        previous[vehicle['vehicle_id']] -= 1
                        
                # add the current point
                sc = ax.scatter(lng, lat, c=colors[-1], s=25)
                trails.setdefault(vehicle['vehicle_id'], []).append(sc)
                previous[vehicle['vehicle_id']] = len(trails[vehicle['vehicle_id']])-1
                    
        # update the location of the previous points
        for t in trails.values():
            for i, sc in enumerate(t[:-1]):
                t[i] = t[i+1]
                ax.collections[sc].set_offsets(np.vstack((ax.collections[sc].get_offsets(), [np.nan, np.nan])))
        # update the location of the last point
        lngs, lats = [], []
        for t in trails.values():
            if t:
                lng, lat = t[-1].get_offsets().flatten()
                lngs.append(lng)
                lats.append(lat)
        scat.set_offsets(np.c_[lngs, lats])
        scat.set_color(colors)
    return scat,

ani = FuncAnimation(fig, update, frames=None, init_func=init, blit=True, interval=1000, cache_frame_data=False)
ani.save('animation.gif', writer='pillow')
plt.show()
# 
