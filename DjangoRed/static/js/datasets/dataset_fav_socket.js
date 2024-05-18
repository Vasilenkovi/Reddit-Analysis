let url = `ws://${window.location.host}/ws/socket-server-favorite/`
const favSocket = new WebSocket(url)
favSocket.onmessage = function(e) {
    let data = JSON.parse(e.data)
    let jsonString = JSON.stringify(data)
    console.log('Data:', jsonString)
    
    if (data.type == "connection_success")
    {
        console.log(jsonString);
    }

    else if (data.type = "error_message")
    {
        console.log(data.error)   
    }

    // if (data.type == "end")
    // {
    //     if (startedRecievingData)
    //     {
    //         gameInstance.SendMessage('FrontendConnector', 'StopRecievingData', jsonString);
    //         startedRecievingData = false;
    //         isRecieving = false;
    //     }
    //     else 
    //     {
    //         console.log("ending connection without beginning it");
    //     }
    // }
}


function send_data(obj) {
    // let data_id = obj.id.toString();
    // var cookies = document.cookie
    // console.log(cookies)
    // let message = JSON.stringify({
    //     "cookies": cookies,
    //     "dataset_id": data_id.substring(4, data_id.length),
    // });
    // // const user_id = JSON.parse(document.getElementById('user_id').textContent);
    
    // favSocket.send(message)

    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    console.log(cookieValue);
}
