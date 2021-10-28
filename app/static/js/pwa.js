/**
 * PWA (progressive web app) support
 */
function ready() {
	// Make sure the browser supports service workers
	if ("serviceWorker" in navigator) {
		// Register a new service worker.
		navigator.serviceWorker
			.register("/static/js/sw.js")
			.then((registration) => {
				console.log(
					"[PWA] Service worker registered with scope: ",
					registration.scope
				);
			})
			.catch((error) => {
				console.error("[PWA] Service worker registration failed: ", error);
			});
	}
}

// Load on document load
document.addEventListener("DOMContentLoaded", ready);
