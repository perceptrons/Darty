window.onload = function() {
  rect = d3.select("rectangle");
  map = "dartboard";
  coordsList = ['100,100 100,400 400,400 400,100 100,100', '200,10 250,190 160,210'];
  createSVG(window.location.href, 500, 500);
  var svgNS = document.getElementsByTagName("svg")[0].namespaceURI;
  populateSVG(coordsList, map, svgNS);
};

// Description: Takes a list of coordinates for each shape and appends to the
// object appendTo.
// Inputs: coordsList - list of x and y polygon coordinates for a shape
//         appendTo - id of html object to append shapes to
// Output: appends all coordsList shapes to appendTo object
function populateSVG(coordsList, id, svgNS) {
  len = coordsList.length;
  for (var i = 0; i < len; i++) {
    var shapeNode = document.createElementNS(svgNS, "polygon");
    shapeNode.setAttribute("name", "polygon_" + i);
    shapeNode.setAttribute("class", "poly");
    shapeNode.setAttribute("points", coordsList[i]);
    // shapeNode.setAttribute("style", "fill:green;stroke:black;stroke-width:5");
    document.getElementById(id).appendChild(shapeNode);
  }
}

// needs URI for dynamically adding svg
function createSVG(uri, width, height) {
  var svg = document.createElementNS(uri, "svg");
  svg.setAttribute("id", "dartboard");
  svg.setAttribute("width", width);
  svg.setAttribute("height", height);
}
