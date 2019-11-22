
{
	const init = () =>{
		document.cookie.split('; ').forEach(itCookie = cookie =>{
			if(cookie.split("=")[0] == "theme" && cookie.split("=")[1] == "darkmode"){
				document.querySelector(".toggleDarkmode").innerHTML = "<a>Enter lightmode</a>"
				document.querySelector(".toggleDarkmode").id = "lightmode"
			}
			if(cookie.split("=")[0] == "theme" && cookie.split("=")[1] == "kerstmis"){
				document.querySelector(".background").innerHTML = '<div class="background_wrapper"><div class="christmas_background"></div><div class="snow layer1 a"></div><div class="snow layer1"></div> <div class="snow layer2 a"></div><div class="snow layer2"></div><div class="snow layer3 a"></div><div class="snow layer3"></div><div class="snowman_wrapper"><div class="snowman_head"></div><div class="snowman_body"></div></div><div class="train_wrapper"><div class="whole_train"><div class="mc_wagon"><div class="wheel_big wheel1"></div><div class="wheel_big wheel2"></div><div class="wheel_big wheel3"></div></div><div class="zeus_wagon"><div class="wheel_big wheel1"></div><div class="wheel_big wheel2"></div><div class="wheel_big wheel3"></div></div><div class="train"><div class="wheel_big wheel1"></div><div class="wheel_big wheel2"></div><div class="wheel_big wheel3"></div><div class="wheel_small wheel4"></div><div class="wheel_small wheel5"></div></div></div></div><input type="checkbox" class="train_button"><div class="merry_christmas"></div><div class="sled_wrapper"><div class="sled"></div></div></div>'; 
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