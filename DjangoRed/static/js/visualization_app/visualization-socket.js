let url = `ws://${window.location.host}/ws/socket-server-clustering/`
const favSocket = new WebSocket(url)
var isRecieving = false;
var startedRecievingData = false;
favSocket.onmessage = function(e) {
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

function getDatasetsIds()
{
    const checkedDatasets = []
    const datasetIds = document.getElementsByClassName("dataset_id")
    for (let datasetId of datasetIds)
    {
        if (datasetId.checked)
        {
            checkedDatasets.push(datasetId.name)
        }
    }

    return checkedDatasets
}

function createString() {
    const checkedDatasets = getDatasetsIds()
    const formId = "vis-app-form"
    const form = document.getElementById(formId)
    const formData = new FormData(form);

    // var messageDict = {"datasets": checkedDatasets}
    var messageDict = {"datasets": checkedDatasets}

    const clasterizationParameters = document.getElementsByClassName("clasterization_params")
    for (let clasterizationParam of clasterizationParameters)
    {
        messageDict[clasterizationParam.name] = clasterizationParam.value
    }
    
    isRecieving = true;
    console.log(messageDict)
    favSocket.send(JSON.stringify(messageDict))
}

var comments = ['keke', 'best thing ever', 'you are not ready', 'C# is the best programming language ever']

function getRandom (list) {
    return list[Math.floor((Math.random()*list.length))];
}
const sleep = ms => new Promise(res => setTimeout(res, ms));

async function ImitateDotTextProcess() {
    if (isRecieving)
    {
        alert("Already recieving data");
        return;
    }
    if (!startedRecievingData) 
    {
        gameInstance.SendMessage('FrontendConnector', 'StartRecievingDotText');
        startedRecievingData = true;
    }
    isRecieving = true;
    let messageDict = {}
    await sleep(2000);
    messageDict['text'] = getRandom(comments);
    let jsonString = JSON.stringify(messageDict);
    console.log(jsonString);
    gameInstance.SendMessage('FrontendConnector', 'DotTextRecieved', jsonString);
    startedRecievingData = false;
    isRecieving = false;
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
    
    favSocket.send(JSON.stringify({
        'message': message
    }))
}