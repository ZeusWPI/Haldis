{
	const init = () => {
		const $darkmode = document.querySelector(".enter_darkmode");
		if($darkmode) $darkmode.addEventListener("click", ()=>toggleBetween("lightmode", "darkmode"));
		const $customThemes = document.querySelector(".custom__themes");
		if($customThemes) $customThemes.addEventListener("click", ()=>toggleBetween("darkmode", "sinterklaas")); //TODO: Create automatic custom team selector

		reloadTheme();
	}

	const toggleBetween = (first, second) => {
		if(localStorage.getItem("theme") == second){
			localStorage.setItem("theme", first)
		}else{
			localStorage.setItem("theme", second)
		}
		reloadTheme();
	}

	const reloadTheme = () => {
			if (typeof(Storage) !== "undefined") {
				if(localStorage.getItem("theme") !== null){
					setTheme();
				}else if((window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches)){
					document.querySelector('body').classList.remove('lightmode');
					document.querySelector('body').classList.add('darkmode');
				}
			} else {
				console.log('You browser does not support local storage, no darkmode for you!' )
			}
	}

	const setTheme = () =>{
		document.querySelector('body').classList.add('darkmode');
		switch(localStorage.getItem("theme")){
			case "halloween":
				setThemeHalloween();
				break;
			case "sinterklaas":
				setThemeSinterklaas();
				break;
			case "darkmode":
				setThemeDarkMode();
				break;
			case "lightmode":
			default:
				setThemeLightMode();
				break;
		}
	}

	//TODO: Use an external file to load themes
	//TODO: Darkness and blur variables

	const setThemeLightMode = () => {
		let root = document.documentElement;
		root.style.setProperty('--dGray6', "#ffffff"); //Dark color
		root.style.setProperty('--dGray5', "#ffffff");
		root.style.setProperty('--dGray4', "#f9f9f9");
		root.style.setProperty('--dGray3', "#ffffff");
		root.style.setProperty('--dGray2', "#212121");
		root.style.setProperty('--dGray1', "#666666");
		root.style.setProperty('--dGray0', "#444444"); //Light color
		root.style.setProperty('--dBlue', "#0A84FF");
		root.style.setProperty('--FontFamily', '"Roboto","Helvetica Neue",Helvetica,Arial,sans-serif"');
		root.style.setProperty('--FontSize', '13px');
		document.querySelector('.background').style.backgroundImage =  'none';
	}

	const setThemeDarkMode = () => {
		let root = document.documentElement;
		root.style.setProperty('--dGray6', "#1C1C1E"); //Dark color
		root.style.setProperty('--dGray5', "#2C2C2E");
		root.style.setProperty('--dGray4', "#3A3A3C");
		root.style.setProperty('--dGray3', "#48484A");
		root.style.setProperty('--dGray2', "#636366");
		root.style.setProperty('--dGray1', "#8E8E93");
		root.style.setProperty('--dGray0', "#E0E0E8"); //Light color
		root.style.setProperty('--dBlue', "#0A84FF");
		root.style.setProperty('--FontFamily', '"Roboto","Helvetica Neue",Helvetica,Arial,sans-serif"');
		root.style.setProperty('--FontSize', '13px');
		document.querySelector('.background').style.backgroundImage =  'none';
	}

	const setThemeHalloween = () => {
		let root = document.documentElement;
		root.style.setProperty('--dGray6', "#260101"); //Dark color
		root.style.setProperty('--dGray5', "#260101");
		root.style.setProperty('--dGray4', "#8C3D0F");
		root.style.setProperty('--dGray3', "#F27405");
		root.style.setProperty('--dGray2', "#F25C05");
		root.style.setProperty('--dGray1', "#F28705");
		root.style.setProperty('--dGray0', "#FFEB65"); //Light color
		root.style.setProperty('--dBlue', "#D91604");
		root.style.setProperty('--FontFamily', '"Roboto","Helvetica Neue",Helvetica,Arial,sans-serif"');
		root.style.setProperty('--FontSize', '13px');
		document.querySelector('.background').backgroundImage = "url('/static/images/Halloween.jpeg')";
	}

	const setThemeSinterklaas = () => {
		let root = document.documentElement;
		root.style.setProperty('--dGray6', "#F50B00"); //Dark color
		root.style.setProperty('--dGray5', "#F20505");
		root.style.setProperty('--dGray4', "#0C6AA6");
		root.style.setProperty('--dGray3', "#177EBF");
		root.style.setProperty('--dGray2', "#F2EF05");
		root.style.setProperty('--dGray1', "#F2EF05");
		root.style.setProperty('--dGray0', "#F2EB80"); //Light color
		root.style.setProperty('--dBlue', "#35F546");
		root.style.setProperty('--FontFamily', "cursive");
		root.style.setProperty('--FontSize', "20px");
		document.body.style.background =  "#000000";
		document.querySelector('.background').style.backgroundImage = "url('/static/images/Sinterklaas.jpg')";
	}
	init();
}
