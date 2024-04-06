let url = `ws://${window.location.host}/ws/socket-server-clustering/`
const clusSocket = new WebSocket(url)
clusSocket.onmessage = function(e) {
    let data = JSON.parse(e.data)
    console.log('Data:', data)
}

