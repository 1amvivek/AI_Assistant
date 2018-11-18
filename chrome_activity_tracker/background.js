function getPostURL() {
    return "http://18.222.204.247:3000/"; // IP_Address of EC2 Instance.
}

function getUserID(email, password) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", getPostURL(), true);
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


function login() {
    var user = document.getElementById("firstname").value;
    var pass = document.getElementById("password").value;

    var bkg = chrome.extension.getBackgroundPage();
    bkg.getUserID(user, pass);
    var redirectURL = "https://www.google.com/"; // Edit this to S3 static page
    chrome.tabs.create({ url: redirectURL });
    return false; //To prevent it from going into next page.
}

document.addEventListener('DOMContentLoaded', function() {
    var link = document.getElementById('link');
    link.addEventListener('click', function() {
        login();
    });
});


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

function onSessionStart(session) {
    console.log("START");
    chrome.storage.sync.get(['userId'], function(storedContent) {
        if (typeof storedContent.userId === 'undefined') {
            // console.log("undefined");
        } else {
            // console.log("UserId is " + storedContent.userId);
            var pushUrl = getPostURL() + "logs";
            pushLogs(pushUrl, session.url, session.startTime, storedContent.userId);
        }
    });
}

function pushLogs(pushUrl, url, time, userId, body = '', browsingTime = '', title = '', searchString = '', urlCategory = '') {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", pushUrl, true);

    xhr.onreadystatechange = function() {
        console.log("Pushing Logs");
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