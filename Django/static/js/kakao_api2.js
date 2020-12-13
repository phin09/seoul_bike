
var map = new kakao.maps.Map(document.getElementById('map'), { // 지도를 표시할 div
    center : new kakao.maps.LatLng(37.566680, 126.9784147), // 지도의 중심좌표
    level : 4 // 지도의 확대 레벨
    });

var positions =[];
var lat_temp_max = 0;
var lat_temp_min = 999;
var lng_temp_max = 0;
var lng_temp_min = 999;

var center_lat = (lat_temp_max + lat_temp_min) / 2
var center_lng = (lng_temp_max + lng_temp_min) / 2
var centerPosition = new kakao.maps.LatLng(center_lat, center_lng)


// 지도에 마커와 인포윈도우를 표시하는 함수
function displayMarker(locPosition) {

    // 마커를 생성합니다
    var marker = new kakao.maps.Marker({
        map: map,
        position: locPosition
    });

    // 지도 중심좌표를 권역 현재 위치로 변경
    map.setCenter(centerPosition);
};

function StationColor(parked, lat ) {
    var content
    var redSt = 
    [
        {
            content:'<button onclick="clickStationMarker(this.id);" class="redSt" id={{ value.dataId }}>{{ pred }}</button>',
            latlng: new kakao.maps.LatLng({{ station.stationLatitude }}, {{ station.stationLongitude }}),
            title: '<div style="font-size:1.2em;font-weight: bold;color: #5E5B55;font-family:Roboto;">{{ station.dataId }}</div>'
        },
    ];

    var yellowSt = 
        [
            {
                content:'<button onclick="clickStationMarker(this.id);" class="yellowSt" id={{ value.stationCode }}>{{ pred }}</button>',
                latlng: new kakao.maps.LatLng({{ station.stationLatitude }}, {{ station.stationLongitude }}),
                title: '<div style="font-size:1.2em;font-weight: bold;color: #5E5B55; font-family:Roboto;">{{ station.dataId }}</div>'
            },
        ];

    var blueSt = 
        [
            {
                content:'<button onclick="clickStationMarker(this.id);" class="blueSt" id={{ value.stationCode }}>{{ pred }}</button>',
                latlng: new kakao.maps.LatLng({{ station.stationLatitude }}, {{ station.stationLongitude }}),
                title: '<div style="font-size:1.2em;font-weight: bold;color: #5E5B55; font-family:Roboto;">{{ station.dataId }}</div>'
            },
        ];

    if (num < 0){return redSt} 
    else if ((num >= 0) && (num <= 2)){ return yellowSt}
    else {return blueSt}
};



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