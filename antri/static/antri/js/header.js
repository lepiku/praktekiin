var menu = document.getElementById('menu-content')
var menu_cover = document.getElementById('menu-cover')
var bar = document.getElementById('bar')

function show_menu() {
  if (menu.classList.contains('show')) {
    hide_menu()
  } else {
    menu.classList.add('show')
    menu_cover.classList.add('show-cover')
    bar.classList.add('close')
  }
}
function hide_menu() {
  if (menu.classList.contains('show')) {
    menu.classList.remove('show')
    menu_cover.classList.remove('show-cover')
    bar.classList.remove('close')
  }
}
document.getElementById('container').addEventListener('click', hide_menu);
