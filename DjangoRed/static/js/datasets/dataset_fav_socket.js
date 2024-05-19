let url = `ws://${window.location.host}/ws/socket-server-favorite/`
const favSocket = new WebSocket(url)
favSocket.onmessage = function(e) {
    let data = JSON.parse(e.data)
    let jsonString = JSON.stringify(data)
    console.log('Data:', jsonString)
    switch (data.type) {
        case "connection_success":
            console.log(jsonString);
            break;
        case "error_message":
            console.log(data.error)
            break;
        default:
            alert(data.message)
    }

}


function send_data(obj) {
    let data_id = obj.id.toString()
    let user_id = JSON.parse(document.getElementById('user_id').textContent)
 
    let message = JSON.stringify({
        "user_id": user_id,
        "dataset_id": data_id.substring(4, data_id.length),
    });
    favSocket.send(message)
}
