function copyToClipboard(feed) {
    var copyText = document.getElementById("feed_url_" + feed);

    copyText.select();
    copyText.setSelectionRange(0, 99999); // For mobile devices 

    navigator.clipboard.writeText(copyText.value);
    console.log(`Copied value to clipboard: ${copyText.value}`)
}

function listFeeds() {
    base_url = "https://sindrel.github.io/nrk-pod-feeds/rss/";

    feeds.forEach(feed => {
        if(!feed["enabled"]) {
            return;
        }

        feed_url = base_url + feed["id"] + ".xml";
        item = `<h3>${feed["title"]}<br/><input type="text" size="50" value="${feed_url}" id="feed_url_${feed["id"]}"><button onclick="copyToClipboard('${feed["id"]}')">Copy</button><h3>`;
        
        document.getElementById("feeds_list").innerHTML += item;
    });
}
