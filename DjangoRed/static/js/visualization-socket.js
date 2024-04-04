let url = `ws://${window.location.host}/ws/socket-server-clustering/`
const clusSocket = new WebSocket(url)
clusSocket.onmessage = function(e)
{
    let data = JSON.parse(e.data)
    console.log('Data:', data)
}

function createString() {
    const formId = "vis-app-form"
    const form = document.getElementById(formId)
    const formData = new FormData(form);

    var output = ""
    var i = 0
    for (var pair of formData.entries()) {
        
        if (i == 5) continue;
        output += pair[1] + " ";
        i += 1;
    }

    console.log(output)
    
    }