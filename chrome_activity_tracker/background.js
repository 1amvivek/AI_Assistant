function formatTime(t) {
    var time = new Date(t);
    return time;
}


function isJsonValid(str) {
    try {
        JSON.parse(str);
    } catch (e) {
        return false;
    }
    return true;
}

function getUserID(email, password, postUrl) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", postUrl, true);

    xhr.onreadystatechange = function() {
        if (isJsonValid(xhr.responseText)) {
            var responseContent = JSON.parse(xhr.responseText);

            chrome.storage.sync.get(['userId'], function(storedContent) {
                if (typeof storedContent.userId === 'undefined') {
                    chrome.storage.sync.set({ 'userId': responseContent.id }, function() {
                        // console.log("Usedid is set here " + responseContent.id);
                    });
                } else {
                    if (storedContent.userId != responseContent.id) {
                        chrome.storage.sync.set({ 'userId': responseContent.id }, function() {
                            // console.log("Usedid is set here " + responseContent.id);
                        });
                    }
                }

            });
        }
    }

    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({ "logemail": email, "logpassword": password }));

}

function onSessionStart(session) {
    var postUrl = "http://172.20.10.12:3000/";
    console.log("START");
    getUserID("test1@gmail.com", "test1", postUrl);
    chrome.storage.sync.get(['userId'], function(storedContent) {
        if (typeof storedContent.userId === 'undefined') {
            // console.log("undefined");
        } else {
            // console.log("UserId is " + storedContent.userId);
            var pushUrl = postUrl + "logs";
            pushLogs(pushUrl, session.url, session.startTime, storedContent.userId);
        }
    });
}

function pushLogs(postUrl, url, time, userId, body = '', browsingTime = '', title = '', searchString = '', urlCategory = '') {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", postUrl, true);

    xhr.onreadystatechange = function() {
        console.log("In push logs method");
        console.log(xhr.responseText);
    }
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        "url": url,
        "time": time,
        "user_id": userId
    }));
}

function onSessionEnd(session) {
    console.log("END", formatTime(session.endTime), session.url);
}
var stopTracking = startTrackingActivity(onSessionStart, onSessionEnd);