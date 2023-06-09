function copyToClipboard(feed) {
    var copyText = document.getElementById("feed_url_" + feed);

    copyText.select();
    copyText.setSelectionRange(0, 99999); // For mobile devices 

    navigator.clipboard.writeText(copyText.value);
    console.log(`Copied value to clipboard: ${copyText.value}`)
}

function listFeeds() {
    base_url = "https://sindrel.github.io/nrk-pod-feeds/rss/";
    info_base_url = "https://radio.nrk.no/podkast/";

    feeds.forEach(feed => {
        stateColor = "#338500"
        stateMsg = "⬈"

        if(feed["hidden"]) {
            return;
        }

        if(!feed["enabled"]) {
            stateColor = "#eb8904"
            stateMsg = "⬊"
        }

        if(feed["ignore"]) {
            stateColor = "#333"
            stateMsg = "⏹"
        }

        feed_url = base_url + feed["id"] + ".xml";
        item = `<li><h4><font color="${stateColor}"><sup>${stateMsg}</sup></font> <a href="${info_base_url}${feed["id"]}" target="_blank">${feed["title"]}</a><br/><input type="text" size="40" value="${feed_url}" id="feed_url_${feed["id"]}" disabled> <button onclick="copyToClipboard('${feed["id"]}')">Copy</button><h3></li>`;
        
        document.getElementById("feeds_list").innerHTML += item;
    });
}

function searchFeeds() {
  var input, filter, ul, li, a, i, txtValue;
  input = document.getElementById('searchInput');
  filter = input.value.toUpperCase();
  ul = document.getElementById("feeds_ul");
  li = ul.getElementsByTagName('li');

  // Loop through all list items, and hide those who don't match the search query
  for (i = 0; i < li.length; i++) {
    a = li[i].getElementsByTagName("a")[0];
    txtValue = a.textContent || a.innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      li[i].style.display = "";
    } else {
      li[i].style.display = "none";
    }
  }
}
