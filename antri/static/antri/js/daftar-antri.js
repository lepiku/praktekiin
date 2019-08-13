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

var tempat = document.getElementById('id_tempat')
function get_times() {
  $.ajax({
    url: get_times_url,
    method: 'GET',
    data: {'id_tempat': tempat.value},
    success: function(result) {
      console.log(result)
      if (result.html !== null) {
        hide('tanggal')
        $('#td-waktu').html(result.html)
        $('#tr-waktu').css('display', 'table-row')
      } else {
        hide('waktu')
      }
    },
    error: function(a, b) {
      console.log(a)
      console.log(b)
    }
  })
}
tempat.onchange = function() {get_times()}

function get_dates(id_jadwal, element) {
  $('.c-waktu').css('background-color', '#39B0A3')
  $.ajax({
    url: get_dates_url,
    method: 'GET',
    data: {'id_jadwal': id_jadwal},
    success: function(result) {
      console.log(result)
      $('#id_jadwal').val(id_jadwal)

      hide('pasien')
      $('#td-tanggal').html(result.html)
      $('#tr-tanggal').css('display', 'table-row')
      element.style.backgroundColor = '#20857A'
    },
    error: function(a, b) {
      console.log(a)
      console.log(b)
    }
  })
}

function get_pasien(tanggal, element) {
  $('.c-tanggal').css('background-color', '#39B0A3')
  $.ajax({
    url: get_pasien_url,
    method: 'GET',
    data: {'tanggal': tanggal},
    success: function(result) {
      console.log(result)
      $('input[name="pasien_set"]').prop('checked', false)
      result.pasien_set.forEach(function (value, _) {
        $('input[name="pasien_set"][value="' + value + '"]').prop('checked', true)
      })
      $('#id_tanggal').val(tanggal)
      $('#tr-pasien').css('display', 'table-row')
      $('input[value="Pesan"]').prop('type', 'submit')
      element.style.backgroundColor = '#20857A'
    },
    error: function(a, b) {
      console.log(a)
      console.log(b)
    }
  })
}

if (tempat.value !== '') {
  get_times()
}

