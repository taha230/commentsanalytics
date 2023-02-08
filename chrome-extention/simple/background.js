const CONTEXT_MENU_ID = "EXPORT_COMMENT";

function exportComment(info, tab) {
  if (info.menuItemId === CONTEXT_MENU_ID) {
    chrome.tabs.executeScript({
      file: "jquery-3.4.1.min.js"
    }, function() {
      chrome.tabs.executeScript({
        file: "content.js"
      });
    });
  }
}


chrome.contextMenus.create({
  title: "Export Comments",
  documentUrlPatterns: ["*://www.youtube.com/watch?*"],
  contexts: ["all"],
  id: CONTEXT_MENU_ID
});

chrome.contextMenus.onClicked.addListener(exportComment);