{
	var $darkmode = document.querySelector(".enter_darkmode");
	var $customThemes = document.querySelector(".custom__themes");
	const init = () => {
		$darkmode.addEventListener("click", toggleDarkmode);
		if($customThemes){
			$customThemes.addEventListener("click", toggleCustomThemes);
		}
		if(localStorage.getItem("customThemes") == 'true'){
			setThemeHalloween();
		}
	    enableDarkmode();
	}

	const toggleDarkmode = () => {
		localStorage.setItem("darkmodeChanged", 'true');
		var newState = !(localStorage.getItem("darkmode") == 'true');
	    localStorage.setItem("darkmode", newState);
	    enableDarkmode();
	}

	const enableDarkmode = () => {
		if (typeof(Storage) !== "undefined") {
			if(localStorage.getItem("darkmode") == 'true' && localStorage.getItem("darkmodeChanged") == 'true' || (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches && localStorage.getItem("darkmodeChanged") != 'true')){
				document.querySelector('body').classList.remove('lightmode');
				document.querySelector('body').classList.add('darkmode');
			} else {
				document.querySelector('body').classList.remove('darkmode');
				document.querySelector('body').classList.add('lightmode');
			}
		} else {
			console.log('You browser does not support local storage, no darkmode for you!' )
		}
	}

	const toggleCustomThemes = () => {
		if(localStorage.getItem("customThemes") == 'true'){
			localStorage.setItem("customThemes", 'false');
			setThemeDarkMode();
		}else{
			localStorage.setItem("customThemes", 'true');
			localStorage.setItem("darkmodeChanged", 'true');
			localStorage.setItem("darkmode", 'true');
			enableDarkmode();
			setThemeHalloween();
		}
	}

	const setTheme = theme =>{
		switch(theme){
			case "halloween":
				setThemeHalloween();
		}
	}

	const setThemeDarkMode = () => {
		document.querySelector('.enter_darkmode').classList.remove("hidden");
		let root = document.documentElement;
		root.style.setProperty('--dGray6', "#1C1C1E"); //Dark color
		root.style.setProperty('--dGray5', "#2C2C2E");
		root.style.setProperty('--dGray4', "#3A3A3C");
		root.style.setProperty('--dGray3', "#48484A");
		root.style.setProperty('--dGray2', "#636366");
		root.style.setProperty('--dGray1', "#8E8E93");
		root.style.setProperty('--dGray0', "#B0B0B8"); //Light color
		root.style.setProperty('--dBlue', "#0A84FF");
		document.body.style.backgroundImage =  'none';
	}

	const setThemeHalloween = () => {
		document.querySelector('.enter_darkmode').classList.add("hidden");
		let root = document.documentElement;
		root.style.setProperty('--dGray6', "#260101"); //Dark color
		root.style.setProperty('--dGray5', "#260101");
		root.style.setProperty('--dGray4', "#8C3D0F");
		root.style.setProperty('--dGray3', "#F27405");
		root.style.setProperty('--dGray2', "#F25C05");
		root.style.setProperty('--dGray1', "#F28705");
		root.style.setProperty('--dGray0', "#FFEB65"); //Light color
		root.style.setProperty('--dBlue', "#D91604");
		document.body.style.backgroundImage = "url('/static/images/Halloween.jpeg')";
	}
	init();
}