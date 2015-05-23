var map;

    function initialize() {

        var mapOptions = {
              zoom: 8,
              center: new google.maps.LatLng(37, -122)
            };

            map = new google.maps.Map(
                document.getElementById('map'),
                mapOptions);

        }

    google.maps.event.addDomListener(window, 'load', initialize);

var LatLng

// map.setCenter
/*
     * Creates a marker for the given business and point
     */
    function createMarker(biz, point, markerNum) {
        var infoWindowHtml = generateInfoWindowHtml(biz)
        var marker = new GMarker(point, icon);
        map.addOverlay(marker);
        GEvent.addListener(marker, "click", function() {
            marker.openInfoWindowHtml(infoWindowHtml, {maxWidth:400});
        });
        // automatically open first marker
        if (markerNum == 0)
            marker.openInfoWindowHtml(infoWindowHtml, {maxWidth:400});
    }