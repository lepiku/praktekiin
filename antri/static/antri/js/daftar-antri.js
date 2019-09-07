var times_cache = {}
var dates_cache = {}
var pasien_cache = {}

function escapeHTML(unsafe) {
  return unsafe
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;")
}

function hide(name) {
  switch (name) {
    case 'waktu':
      $('#tr-waktu').css('display', 'none')
    case 'tanggal':
      $('#tr-tanggal').css('display', 'none')
    case 'pasien':
      $('#tr-pasien').css('display', 'none')
      $('input[value="Pesan"]').prop('type', 'hidden')
  }
}

function set_times(result) {
  hide('tanggal')
  $('#td-waktu').html(result.html)
  $('#tr-waktu').css('display', 'table-row')
}
function set_dates(result, element) {
  hide('pasien')
  $('#td-tanggal').html(result.html)
  $('#tr-tanggal').css('display', 'table-row')
  element.style.backgroundColor = '#20857A'
}
function set_pasien(result, element) {
  $('input[name="pasien_set"]').prop('checked', false)
  result.pasien_set.forEach(function (value, _) {
    $('input[name="pasien_set"][value="' + value + '"]').prop('checked', true)
  })
  $('#tr-pasien').css('display', 'table-row')
  $('input[value="Simpan"]').prop('type', 'submit')
  element.style.backgroundColor = '#20857A'
}

var tempat = document.getElementById('id_tempat')
function get_times() {
  var id_tempat = tempat.value
  if (id_tempat === '') {
    hide('waktu')
  } else if (!(id_tempat in times_cache)) {
    $.ajax({
      url: get_times_url,
      method: 'GET',
      data: {'id_tempat': id_tempat},
      success: function(result) {
        console.log(result)
        set_times(result)
        times_cache[id_tempat] = result
      },
      error: function(a, b) {
        console.log(a)
        console.log(b)
      }
    })
  } else {
    set_times(times_cache[id_tempat])
  }
}

function get_dates(id_jadwal, element) {
  $('.c-waktu').css('background-color', '#39B0A3')
  $('#id_jadwal').val(id_jadwal)
  if (!(id_jadwal in dates_cache)) {
    $.ajax({
      url: get_dates_url,
      method: 'GET',
      data: {'id_jadwal': id_jadwal},
      success: function(result) {
        console.log(result)
        set_dates(result, element)
        dates_cache[id_jadwal] = result
      },
      error: function(a, b) {
        console.log(a)
        console.log(b)
      }
    })
  } else {
    set_dates(dates_cache[id_jadwal], element)
  }
}

function get_pasien(tanggal, element) {
  $('.c-tanggal').css('background-color', '#39B0A3')
  $('#id_tanggal').val(tanggal)
  if (!(tanggal in pasien_cache)) {
    $.ajax({
      url: get_pasien_url,
      method: 'GET',
      data: {'tanggal': tanggal},
      success: function(result) {
        console.log(result)
        set_pasien(result, element)
        pasien_cache[tanggal] = result
      },
      error: function(a, b) {
        console.log(a)
        console.log(b)
      }
    })
  } else {
    set_pasien(pasien_cache[tanggal], element)
  }
}

tempat.onchange = function() {get_times()}
if (tempat.value !== '') {
  get_times()
}
