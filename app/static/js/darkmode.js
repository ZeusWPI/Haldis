{
	var $darkmode = document.querySelector(".enter_darkmode");
	const init = () => {
	    $darkmode.addEventListener("click", toggleDarkmode);
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
	init();
}