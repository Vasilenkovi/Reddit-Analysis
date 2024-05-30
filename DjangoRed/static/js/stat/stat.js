let url = `ws://${window.location.host}/ws/socket-server-stat/`
const statSocket = new WebSocket(url)


statSocket.onopen = function(e) { // on load
    console.log("JS: Connection established")
    createString();
    
}

statSocket.onmessage = function(e) { 
    let data = JSON.parse(e.data);
    let jsonString = JSON.stringify(data);
    console.log('Data:', jsonString);
    if (data.type == "info"){
        //test_message_back = {type:info : [data64, data64]}
        giveOutimages(data["info"]);
    }
}

statSocket.onclose = function(e) {
    console.log("JS: Connection terminated. I'm sorry to interupt you...")
}

statSocket.onerror = function(e) {
    console.log("JS: Error something went wrong")
}

function getSubmissionsNames(){
    const submissons = [];
    const submissionsNames = document.getElementsByClassName("containsName");
    for (let submissonName of submissionsNames){
        submissons.push(submissonName.id);
    }
    return submissons;
}

function createString() { //message to back
    const submissons = getSubmissionsNames();
    //const job_id = document.getElementById("job_id_info").name;
    const job_id = document.getElementById("job_id_info").getAttribute("name");
    var messageDict = {"names": submissons, "job_id": job_id};

    console.log(messageDict);
    statSocket.send(JSON.stringify(messageDict));
}

function giveOutimages(recivedMessageList){ //after reciveing message from back
    // recivedMessageList = {"base64 of image", "next base64 of image"}
    ids = getSubmissionsNames();
    for (var i = 0; i < recivedMessageList.length; i++){
        document.getElementById(ids[i]).src = "data:image/png;base64," + recivedMessageList[i];
    }
}
