if (navigator.geolocation){
    navigator.geolocation.getCurrentPosition(function(position){
        const url = '/users/home';
        const params = new URLSearchParams({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
        });
        const xhr = new XMLHttpRequest();
        xhr.open('GET', `${url}?${params}`, true);
        xhr.onload = function() {
            if (xhr.status === 200) {
                console.log(position.coords.latitude);
                console.log(position.coords.longitude)
            } else {
                console.error('Request failed. Returned status of ' + xhr.status);
            }
        };
        xhr.onerror = function() {
            console.error('Request failed. Network error');
        };
        xhr.send();

    })
}