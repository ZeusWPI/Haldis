var haldisCountdownStart = new Date();
$.ready(function(){
	$(".time").each(function() {
		var timeEl = $(this);

		var delta = parseInt(timeEl.data("seconds"), 10);
		var end = new Date(haldisCountdownStart.getTime() + delta * 1000);

		var now = new Date();
		var delta = Math.floor((end - now) / 1000);

		console.log("delta", delta)
		if (delta <= 0) {
			eval(timeEl.data("onfinish"))
			timeEl.html("closed");
			return;
		}

		function zeroPad(value) {
			return ("0" + value).slice(-2)
		}

		var intervalId;

		function update() {
			var now = new Date();
			var delta = Math.floor((end - now) / 1000);
			if (delta <= 0) {
				window.clearInterval(intervalId);
				console.log("Reload completed");

				if (timeEl.data("onfinish")) {
					eval(timeEl.data("onfinish"))
				}
				// if (timeEl.data("reload") === "yes") {
				// 	$("#form").slideUp();
				// 	timeEl.html("closed, refreshing page...");
				// 	window.setTimeout(function () {
				// 		window.location.reload();
				// 	}, 2000);
				// } else {
					timeEl.html("closed");
				// }
				return;
			}

			var seconds = delta % 60;
			var carry   = Math.floor(delta / 60);
			var minutes = carry % 60;
			carry       = Math.floor(carry / 60);
			var hours = carry % 24;
			var days  = Math.floor(carry / 24);

			var text = "";
			if (days) text = days + " days, ";
			text += zeroPad(hours) + ":" + zeroPad(minutes) + ":" + zeroPad(seconds);
			text += " left";

			timeEl.html(text);
		}
		intervalId = window.setInterval(update, 1000);
		update();
	});
}());


function finish_timer() {
	console.log("finishing timer thing thing")
}
