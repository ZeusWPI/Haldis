
{
	const init = () =>{
		document.cookie.split('; ').forEach(itCookie = cookie =>{
			if(cookie.split("=")[0] == "theme" && cookie.split("=")[1] == "darkmode"){
				document.querySelector(".toggleDarkmode").innerHTML = "<a>Enter lightmode</a>"
				document.querySelector(".toggleDarkmode").id = "lightmode"
			}
		});
		document.querySelectorAll('.changeThemeButton').forEach(changeThemeButton= e => {e.addEventListener(`click`, handleClickChangeTheme)});
	}

	const handleClickChangeTheme = e =>{
		document.cookie = "theme = "+e.currentTarget.id+";path=/"; 
		location.reload();
	}
	


	init();
}