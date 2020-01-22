function changeTheme() {
    // Get the selected theme for the dropdown
    var themes_select = document.getElementById("themes_select");
    var selected_theme = themes_select.options[themes_select.selectedIndex].text;

    // Update the theme cookie
    document.cookie = "theme=" + escape(selected_theme) + "; Path=/;"
    
    // Finally reload the page to let the new theme take effect
    location.reload();
}