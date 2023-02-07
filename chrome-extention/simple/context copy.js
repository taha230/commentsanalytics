var CONTEXT_MENU_ID = "EXPORT_COMMENT";

function exportComment(a, b) {
    a.menuItemId === CONTEXT_MENU_ID && chrome.tabs.executeScript(null, {
        file: "jquery-3.4.1.min.js"
    }, function() {
        chrome.tabs.executeScript(null, {
            file: "content.js"
        })
    })
}
chrome.contextMenus.create({
    title: "Export Comments",
    documentUrlPatterns: ["*://www.youtube.com/watch?*"],
    contexts: ["all"],
    id: CONTEXT_MENU_ID
});
chrome.contextMenus.onClicked.addListener(exportComment);