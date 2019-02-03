$(document).ready(function() {
  $.ajaxSetup({cache: false});

  // coordsList = ['100,100 100,400 400,400 400,100 100,100', '200,10 250,190 160,210',
  //             '0,0 0,50 50,50 50,0 0,0'];

  $.getJSON('regions.json', function(coordsList) {
      createSVG(window.location.href, 100, 100);
    // console.log("asdf" + svgNS);
    var svgNS = document.getElementsByTagName("svg")[0].namespaceURI;
    map = "dartboard";
    var len = Object.keys(coordsList).length;
    // coordsList = ['100,100 100,400 400,400 400,100 100,100', '200,10 250,190 160,210',
    //             '0,0 0,50 50,50 50,0 0,0'];
    coordsList.length = len;
    coordsList = Array.prototype.slice.call(coordsList);
    populateSVG(coordsList, map, svgNS);

    // populateSVG(coordsList, map, svgNS);
    zeroFillRegionData();

    // Setup the game
    $('.start-btn').click(function() {
      $('.game-board-setup').removeClass('hidden');
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
      $("[name='" + regionName + "']").attr("value", regionPoints);
      $('[name="hover-region-value"]').empty();
      $('[name="hover-region-value"]').append($(".poly-selected").attr("value"));
      if (regionPoints == "" || isNaN(regionPoints) == true) {
        alert("Please enter a number for this region!");
      } else {
        $.post('writeRegionPointsToFile.php', {regionName: regionName, regionPoints: regionPoints},
        function(result) {
          console.log(regionPoints + " written to region_data.json!");
        });
        $('.poly-selected').addClass('poly-set');
        checkGameReady();
      }
    });

    // Display point value of currently hovered-on poly
    $('.poly').hover(function() {
        $('[name="hover-region-value"]').empty();
        $('[name="hover-region-value"]').append($(this).attr("value"));
    });

    // PLAY GAME
    var player_1_score = 0;
    var player_2_score = 0;
    $('[name="play-game-btn"]').click(function() {
      $(".game-board-setup").addClass("hidden");
      $('[name="player-2-div"]').addClass("hidden");
      $(".game-board-active").removeClass("hidden");
    });

    // Play/pause functionality - make sure to write to file!
    var scoreMonitoring = "True";
    $('[name="play-btn"]').click(function() {
      $('[name="pause-btn"]').removeClass('hidden');
      $('[name="play-btn"]').addClass('hidden');
      scoreMonitoring = "False";
      $.post('scoreMonitoring.php', {scoreMonitoring: scoreMonitoring}, function(result) {
        console.log("score monitoring: " + scoreMonitoring);
      });
    });
    $('[name="pause-btn"]').click(function() {
      $('[name="play-btn"]').removeClass('hidden');
      $('[name="pause-btn"]').addClass('hidden');
      scoreMonitoring = "True";
      $.post('scoreMonitoring.php', {scoreMonitoring: scoreMonitoring}, function(result) {
        console.log("score monitoring: " + scoreMonitoring);
      });
    });
  });
});


// create the svg from a list of coordinates
function populateSVG(coordsList, id, svgNS) {
  len = coordsList.length;
  for (var i = 0; i < len; i++) {
    var shapeNode = document.createElementNS(svgNS, "polygon");
    shapeNode.setAttribute("name", "polygon_" + i);
    shapeNode.setAttribute("class", "poly poly-unset");
    shapeNode.setAttribute("points", coordsList[i]);
    shapeNode.setAttribute("value", "0");
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
  polys = $('.poly');
  poly_names = []; len = polys.length; zeros = [];
  for (var i = 0; i < len; i++) {
    poly_names.push($(polys[i]).attr("name"));
    zeros.push("0");
  }
  console.log(poly_names);
  $.post('zeroFillRegionData.php', {regionNames: poly_names, regionPoints: zeros},
  function(result) {
    console.log("Zeros written to region_data.json!");
  });
}

// if all poly's values are set, let player start game!
function checkGameReady() {
  if ($("polygon").length == $(".poly-set").length)
    $('[name="play-game-btn"]').removeClass("hidden");
}

function getRegionsData(coordsList, map, svgNS) {
  this.coordsList = null;
  $.getJSON('regions.json', function(json) {
    this.coordsList = json;
    populateSVG(coordsList, map, svgNS);
  }.bind(this));
}
