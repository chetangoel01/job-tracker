async function sendCurrentTabToServer(tab) {
  try {
    const url = tab.url || '';
    const title = tab.title || '';
    let hostname = '';
    try { hostname = new URL(url).hostname.replace(/^www\./, ''); } catch {}

    const body = {
      company: hostname,
      role: title,
      url,
      source: 'extension'
    };

    const ports = [8765, 8766, 8787, 8888];
    let ok = false, lastErr;
    for (const p of ports) {
      try {
        const resp = await fetch(`http://127.0.0.1:${p}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(body)
        });
        if (resp.ok) { ok = true; break; }
        lastErr = new Error('HTTP ' + resp.status);
      } catch (e) { lastErr = e; }
    }
    if (!ok) throw lastErr || new Error('No server found');
    chrome.action.setBadgeText({ text: '✓', tabId: tab.id });
    chrome.action.setBadgeBackgroundColor({ color: '#10B981', tabId: tab.id });
    const originalTitle = tab.title || '';
    chrome.action.setTitle({ title: 'Saved to Inbox ✅' });
    setTimeout(() => chrome.action.setBadgeText({ text: '', tabId: tab.id }), 1200);
    setTimeout(() => chrome.action.setTitle({ title: 'Add job to Markdown' }), 1500);
    try {
      chrome.notifications.create({
        type: 'basic',
        iconUrl: 'icon-128.png',
        title: 'Job saved to Inbox',
        message: hostname ? `${hostname}` : 'Saved current tab',
        priority: 1,
        silent: true
      });
    } catch (_) {}
  } catch (e) {
    chrome.action.setBadgeText({ text: '!', tabId: tab.id });
    chrome.action.setBadgeBackgroundColor({ color: '#EF4444', tabId: tab.id });
    chrome.action.setTitle({ title: 'Capture failed ❌' });
    setTimeout(() => chrome.action.setBadgeText({ text: '', tabId: tab.id }), 1500);
    setTimeout(() => chrome.action.setTitle({ title: 'Add job to Markdown' }), 1800);
    try {
      chrome.notifications.create({
        type: 'basic',
        iconUrl: 'icon-128.png',
        title: 'Job capture failed',
        message: (e && e.message) ? e.message : 'Could not reach capture server',
        priority: 2
      });
    } catch (_) {}
    console.error('Job Tracker capture failed', e);
  }
}

chrome.action.onClicked.addListener(async (tab) => {
  if (!tab || !tab.url) return;
  sendCurrentTabToServer(tab);
});


