// Service worker for PWA support

// Install Hook
// Triggered when the PWA is installed by the browser.
self.addEventListener("install", () => {
	console.log("[Service Worker] Installed");
});

// Activate Hook
// Triggered when the PWA is activated by the browser.
self.addEventListener("activate", () => {
	console.log("[Service Worker] Activated");
});
