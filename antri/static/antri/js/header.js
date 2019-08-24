var menu = document.getElementById('menu-content')
var menu_cover = document.getElementById('menu-cover')

function show_menu() {
  if (menu.classList.contains('show')) {
    hide_menu()
  } else {
    menu.classList.add('show')
    menu_cover.classList.add('show-cover')
  }
}
function hide_menu() {
  if (menu.classList.contains('show')) {
    menu.classList.remove('show')
    menu_cover.classList.remove('show-cover')
  }
}
document.getElementById('container').addEventListener('click', hide_menu);
