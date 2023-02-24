// Prompt user to enter day and/or campus
var day = prompt("Enter day (Monday, Tuesday, Wednesday, Thursday, Friday):");
var campus = prompt("Enter campus (Busch, Livingston, College Avenue, Cook, Douglass):");

// Load class data from JSON file
var xmlhttp = new XMLHttpRequest();
xmlhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
    var classData = JSON.parse(this.responseText);

    // Filter classes by day and/or campus
    var filteredClasses = [];
    for (var i = 0; i < classData.length; i++) {
      var classDay = classData[i].days.find(function(d) { return d.toLowerCase() == day.toLowerCase(); });
      var classCampus = classData[i].campuses.find(function(c) { return c.toLowerCase() == campus.toLowerCase(); });
      if ((!day || classDay) && (!campus || classCampus)) {
        filteredClasses.push(classData[i]);
      }
    }

    // Display filtered classes as calendar blocks
    for (var i = 0; i < filteredClasses.length; i++) {
      var classStartTime = filteredClasses[i].time.split(" - ")[0];
      var classEndTime = filteredClasses[i].time.split(" - ")[1];
      var classDuration = (new Date("1970-01-01T" + classEndTime + "Z")) - (new Date("1970-01-01T" + classStartTime + "Z"));
      var classTop = ((new Date("1970-01-01T" + classStartTime + "Z")).getHours() - 8) * 60 + (new Date("1970-01-01T" + classStartTime + "Z")).getMinutes();
      var classHeight = classDuration / (1000 * 60);
      var classHtml = "<div class='class-block' style='top: " + classTop + "px; height: " + classHeight + "px;'>" + filteredClasses[i].name + "<br>" + filteredClasses[i].time + "<br>" + filteredClasses[i].campuses.join(", ") + "</div>";
      document.getElementById("calendar").innerHTML += classHtml;
    }
  }
};
xmlhttp.open("GET", "class_data.json", true);
xmlhttp.send();
