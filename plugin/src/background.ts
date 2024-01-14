// background.ts

function fetchData(year: string) {
    const url = `https://api.github.com/repos/AngusFan-GH/6ren/contents/lunar/data/${year}.json`;
    // 示例：使用 fetch 请求数据
    return fetch(url)
        .then(response => response.json())
        .catch(error => console.error('Error fetching data:', error));
}

// 监听来自 popup 的消息
chrome.runtime.onMessage.addListener(
    (request, sender, sendResponse) => {
        if (request.action === 'fetchData') {
            fetchData(request.data).then(data => sendResponse({ data }));
            return true; // 表示你将异步发送响应
        }
    });

