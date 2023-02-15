const CONTEXT_MENU_ID = "EXPORT_COMMENT";

function exportComment(info, tab) {
  if (info.menuItemId === CONTEXT_MENU_ID) {
    chrome.scripting.executeScript({
      target: {tabId: tab.id, allFrames: false},
      files: [ "jquery-3.6.1.js" ]
    }, function() {
      chrome.scripting.executeScript({
        target: {tabId: tab.id, allFrames: false},
        files: [ "content.js" ]
      });
    });
  }
}

chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    title: "Export Comments",
    documentUrlPatterns: ["*://www.youtube.com/watch?*"],
    contexts: ["all"],
    id: CONTEXT_MENU_ID
  });
});

chrome.contextMenus.onClicked.addListener(exportComment);