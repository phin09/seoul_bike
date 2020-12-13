
        


{% for station in stations %}

    var num = {{.parkingBikeTotCnt}} - {{pred}};
    var colorStation = StationColor(num, station)
    positions = positions.concat(positionsRed);
}

// 권역 내 중심좌표 만들기
var lat_value = {{ fixed.stationLatitude }};
if (lat_value > lat_temp_max) {
    lat_temp_max = lat_value
}else if (lat_value < lat_temp_min) {
    lat_temp_min = lat_value
}

var lng_value = {{ fixed.stationLongitude }};
if (lng_value > lng_temp_max) {
    lng_temp_max = lng_value
}else if (lng_value < lng_temp_min) {
    lng_temp_min = lng_value
}

{% endfor %}

var center_lat = (lat_temp_max + lat_temp_min) / 2
var center_lng = (lng_temp_max + lng_temp_min) / 2
var centerPosition = new kakao.maps.LatLng(center_lat, center_lng)

// HTML5의 geolocation으로 사용할 수 있는지 확인
if (navigator.geolocation) {

    // GeoLocation을 이용해서 접속 위치를 얻어옴
    navigator.geolocation.getCurrentPosition(function(position) {

        var lat = position.coords.latitude; // 위도
        var lon = position.coords.longitude; // 경도
        var locPosition = new kakao.maps.LatLng(lat, lon)

        // 마커와 인포윈도우를 표시합니다
        displayMarker(locPosition);
        // 주소-좌표 변환 객체를 생성합니다
        var geocoder = new kakao.maps.services.Geocoder();

        var result = geocoder.coord2RegionCode(lon, lat,  displayCenterInfo);

        // 지도 좌측상단에 지도 중심좌표에 대한 주소정보를 표출하는 함수
        function displayCenterInfo(result, status) {
            if (status === kakao.maps.services.Status.OK) {
                var infoDiv = document.getElementById('centerAddr1');

                for(var i = 0; i < result.length; i++) {
                    // 행정동의 region_type 값은 'H' 이므로
                    if (result[i].region_type === 'H') {
                        infoDiv.innerHTML = result[i].address_name;
                        break;
                    }
                }
            }
        }

        });

} else { // HTML5의 GeoLocation을 사용할 수 없을 때 마커 표시 위치와 인포윈도우 내용을 설정

    var locPosition = new kakao.maps.LatLng(33.450701, 126.570667)


    displayMarker(locPosition);
}

for (var i = 0; i < positions.length; i ++) {
        var customOverlay1 = new kakao.maps.CustomOverlay({
                    content: positions[i].content,
                    position: positions[i].latlng,
                    map: map
        });

        var customOverlay2 = new kakao.maps.CustomOverlay({
            content: positions[i].title,
            position: positions[i].latlng,
            yAnchor: 1,
            xAnchor: 0.2,
            map: map
        });
}

