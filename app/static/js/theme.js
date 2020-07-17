{
	const COOKIE_THEME = "theme";
	const COOKIE_ATMOSPHERE = "theme_atmosphere";
	const COOKIE_PERFORMANCE = "theme_performance";

	const YEAR = 60 * 60 * 24 * 365;

	const storeCookieAndReload = (name, value) => {
		document.cookie = name + " = " + value + "; Path=/; Max-Age=" + (50 * YEAR);
		location.reload();
	}

	const radio = (name, options, current) => {
		let container = document.createElement("div");

		for (let option in options) {
			if (!options.hasOwnProperty(option)) continue;

			let input = document.createElement("input");
			input.type = "radio";
			input.name = name;
			input.value = option;
			input.id = `${name}-${option}`;
			if (option === current) input.setAttribute("checked", "checked");
			input.addEventListener("change", e => storeCookieAndReload(name, e.currentTarget.value));

			let label = document.createElement("label");
			label.setAttribute("for", `${name}-${option}`);
			label.innerText = options[option];

			let span = document.createElement("span");
			span.append(input, " ", label, " ");
			container.appendChild(span);
		}

		return container;
	};

	const init = () => {
		let cookies = {};
		document.cookie.split('; ')
			.map(cookieDefStr => cookieDefStr.split("=", 2))
			.forEach(cookiePair => { cookies[cookiePair[0]] = cookiePair[1]; });

		if (window.currentTheme === "plain") {
			let a = document.createElement("a");
			a.href = "javascript:void(0)";

			if (cookies[COOKIE_ATMOSPHERE] == "darkmode") {
				a.innerHTML = "Enter light mode"
				a.addEventListener("click", () => storeCookieAndReload(COOKIE_ATMOSPHERE, "lightmode"));
			} else {
				a.innerHTML = "Enter dark mode"
				a.addEventListener("click", () => storeCookieAndReload(COOKIE_ATMOSPHERE, "darkmode"));
			}

			document.getElementById("themeChange").innerHTML = "";
			document.getElementById("themeChange").appendChild(a);
		}


		if (window.currentTheme === "christmas") {
			document.querySelector(".background").innerHTML = '<div class="background_wrapper"><div class="christmas_background"></div><div class="snow layer1 a"></div><div class="snow layer1"></div> <div class="snow layer2 a"></div><div class="snow layer2"></div><div class="snow layer3 a"></div><div class="snow layer3"></div><div class="snowman_wrapper"><div class="snowman_head"></div><div class="snowman_body"></div></div><div class="train_wrapper"><div class="whole_train"><div class="mc_wagon"><div class="wheel_big wheel1"></div><div class="wheel_big wheel2"></div><div class="wheel_big wheel3"></div></div><div class="zeus_wagon"><div class="wheel_big wheel1"></div><div class="wheel_big wheel2"></div><div class="wheel_big wheel3"></div></div><div class="train"><div class="wheel_big wheel1"></div><div class="wheel_big wheel2"></div><div class="wheel_big wheel3"></div><div class="wheel_small wheel4"></div><div class="wheel_small wheel5"></div></div></div></div><input type="checkbox" class="train_button"><div class="merry_christmas"></div><div class="sled_wrapper"><div class="sled"></div></div></div>';
		}


		if (document.querySelector(".changePerformance") && window.currentThemeOptions.includes("performance")) {
			document.querySelector(".changePerformance").appendChild(
				radio(COOKIE_PERFORMANCE, {heavy: "Heavy", lightweight: "Lightweight"}, cookies[COOKIE_PERFORMANCE])
			);
		}

		if (document.getElementById("themes_select")) {
			let themes_select = document.getElementById("themes_select");
			themes_select.value = cookies["theme"] || "";

			themes_select.addEventListener("change", () => storeCookieAndReload(COOKIE_THEME, themes_select.value));
		}
	}

	init();
}
