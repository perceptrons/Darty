$(document).ready(function() {
  $.ajaxSetup({cache: false});
  map = "dartboard";
  coordsList = ['100,100 100,400 400,400 400,100 100,100', '200,10 250,190 160,210',
                '0,0 0,50 50,50 50,0 0,0'];
  createSVG(window.location.href, 100, 100);
  var svgNS = document.getElementsByTagName("svg")[0].namespaceURI;
  populateSVG(coordsList, map, svgNS);
  zeroFillRegionData();
  // Setup the game
  $('.start-btn').click(function() {
    $('.game-board').removeClass('hidden');
    $('.start-btn').addClass('hidden');
  });

  // Show clicked region
  $('.poly').click(function() {
    $this = $(this);
    // make sure everything is unselected
    $('.poly').removeClass('poly-selected');
    $('.poly').addClass('poly-unset');
    $this.addClass('poly-selected');
    $this.removeClass('poly-unset');
    // TODO: make poly-set z-index lower priority than selected index but don't remove it
  });

  // Submit region file form
  $('.region-points-btn').click(function() {
    // check that a poly is clicked
    if ($('.poly-selected').attr("name") == undefined) {
      alert("Please click a region to enter a value!");
      return;
    }
    var regionName = $('.poly-selected').attr("name");
    var regionPoints = $('.region-points-input').val();
    if (regionPoints == "" || isNaN(regionPoints) == true) {
      alert("Please enter a number for this region!");
    } else {
      $.post('writeRegionPointsToFile.php', {regionName: regionName, regionPoints: regionPoints},
      function(result) {
        console.log(regionPoints + " written to region_data.json!");
      });
    }
  });

  // Display point value of currently hovered-on poly
  $('.poly').hover(function() {
    $('[name="hover-region-value"]').text += $(this).attr("name");
  }, function() {
    $('[name="hover-region-value"]').text += 'N/A';
  });
});

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
    shapeNode.setAttribute("class", "poly poly-unset");
    shapeNode.setAttribute("points", coordsList[i]);
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

// create new region_data.json file
// 0 initialize all region_data.json poly's
function zeroFillRegionData() {
  // $.ajax({
  //   url: '/region_data.json',
  //   type: 'head',
  //   error: function() {
  // $.post("check_file_exists.php", function(result) {
  //   console.log("region_data.json file written");
  // });
  polys = $('.poly');
  poly_names = []; len = polys.length; zeros = [];
  for (var i = 0; i < len; i++) {
    poly_names.push($(polys[i]).attr("name"));
    zeros.push("0");
  }
  $.post('zeroFillRegionData.php', {regionNames: poly_names, regionPoints: zeros},
  function(result) {
    console.log(result); 
    console.log("Zeros written to region_data.json!");
  });
    // },
    // success: function() {
    //   console.log("region_data.json already exists");
    // }
  // });
}
