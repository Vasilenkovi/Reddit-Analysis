let url = `ws://${window.location.host}/ws/socket-server-clustering/`
const clusSocket = new WebSocket(url)
var isRecieving = false;
var startedRecievingData = false;
clusSocket.onmessage = function(e) {
    let data = JSON.parse(e.data)
    let jsonString = JSON.stringify(data)
    console.log('Data:', jsonString)
    
    if (data.type == "point message")
    {
        console.log(jsonString);
        if (!startedRecievingData) 
        {
            gameInstance.SendMessage('FrontendConnector', 'StartRecievingData');
            startedRecievingData = true;
        }
        gameInstance.SendMessage('FrontendConnector', 'RecieveDotData', jsonString);
    }

    if (data.type == "end")
    {
        if (startedRecievingData)
        {
            gameInstance.SendMessage('FrontendConnector', 'StopRecievingData', jsonString);
            startedRecievingData = false;
            isRecieving = false;
        }
        else 
        {
            console.log("ending connection without beginning it");
        }
    }
}

function createString() {
    const formId = "vis-app-form"
    const form = document.getElementById(formId)
    const formData = new FormData(form);

    var messageDict = {}
    var i = 0
    for (var pair of formData.entries()) {
        if (i == 6) continue;
        messageDict[pair[0]] = pair[1];
        i += 1;
    }
    isRecieving = true;
    clusSocket.send(JSON.stringify(messageDict))
}

function createStringNoJSON() {
    const formId = "vis-app-form"
    const form = document.getElementById(formId)
    const formData = new FormData(form);

    var message = ""
    var i = 0
    for (var pair of formData.entries()) {    
        if (i == 6) continue;
        message += pair[1];
        if (i != 5)
            message += " ";
        i += 1;
    }
    
    clusSocket.send(JSON.stringify({
        'message': message
    }))
}