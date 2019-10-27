$(document).ready(function () {  
    if(res != null) {
        data = JSON.parse(res);  
        var encoding = {
            "anger": "#ad0505",
            "joy": "#ffd500",
            "happy": "#ffd500",
            "excited": "#ffd500",
            "neutral": "#77777a",
            "distgust": "#2b0505"
        };

        createTextProfile($("#textAnalysis"), data["text"], encoding);
        createAudioProfile($("#audioAnalysis"), data["audio"], encoding);
    } else {
        console.log("Error")
    }
});

function createTextProfile(paragraphObj, text, encoding) {
    var html = "";
    for (const [key, value] of Object.entries(text)) {
        if(value[0] in encoding) {
            html += "<span style=\"color: " + encoding[value[0]] + "\">" + key + "</span>";
        } else {
            html += "<span>" + key + "</span>";
        }
    }

    paragraphObj.html(html);
}

function createAudioProfile(paragraphObj, text, encoding) {
    var html = "";
    for (const [key, value] of Object.entries(text)) {
        if(value in encoding) {
            html += "<span style=\"color: " + encoding[value] + "\">" + key + "</span>";
        } else {
            html += "<span>" + key + "</span>";
        }
    }

    paragraphObj.html(html);
}