var canvas = document.getElementById("myCanvas");
var ctx = canvas.getContext("2d");

var url = "https://transloc-api-1-2.p.rapidapi.com/vehicles.json";
var querystring = {
    "agencies": "1323",
    "geo_area": "40.504728,-74.448948|6000",
    "callback": "call"
};
var headers = {
    "X-RapidAPI-Key": "[key]",
    "X-RapidAPI-Host": "transloc-api-1-2.p.rapidapi.com"
};

var route_colors = {};

function get_route_color(route_id) {
  if (!(route_id in route_colors)) {
    route_colors[route_id] = [Math.random(), Math.random(), Math.random()];
  }
  return route_colors[route_id];
}

function update() {
  fetch(url + '?' + new URLSearchParams(querystring), {headers})
    .then(response => response.json())
    .then(data => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      for (var key in data['data']) {
        for (var i = 0; i < data['data'][key].length; i++) {
          var vehicle = data['data'][key][i];
          var route_id = vehicle['route_id'];
          var lat = vehicle['location']['lat'];
          var lng = vehicle['location']['lng'];
          var color = get_route_color(route_id);
          ctx.fillStyle = 'rgba(' + color[0]*255 + ',' + color[1]*255 + ',' + color[2]*255 + ',0.5)';
          ctx.beginPath();
          ctx.arc((lng + 74.41) * canvas.width / 0.07, (40.54 - lat) * canvas.height / 0.07, 5, 0, 2*Math.PI);
          ctx.fill();
        }
      }
    });
}

update();
setInterval(update, 2000);
