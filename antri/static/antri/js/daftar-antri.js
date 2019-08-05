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
  }
}

var tempat = document.getElementById('id_tempat')
function get_time() {
  $.ajax({
    url: get_times_url,
    method: 'GET',
    data: {'id_tempat': tempat.value},
    success: function(result) {
      console.log(result)
      if (result.hari !== null) {
        var waktu_table = '<table id="in-table"><tbody><tr><td></td>'

        for (var x = 0; x < result.hari.length; x++) {
          waktu_table += '<td class="hari">' + result.hari[x] + '</td>'
        }
        waktu_table += '</tr>'

        for (var key in result.jadwal) {
          waktu_table += '<tr><td class="waktu">' + key + '</td>'
          var j = result.jadwal[key]
          for (var x in j) {
            var fx = "get_dates(" + j[x]['id'] + ", '" + key + "')"
            waktu_table += '<td class="cell" onclick="' + fx + '">' + j[x]['jam'] + '</td>'
          }
          waktu_table += '</tr>'
        }

        waktu_table += '</tbody></table>'
        $('#td-waktu').html(waktu_table)
        $('#tr-waktu').css('display', 'table-row')
        hide('tanggal')

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
tempat.onchange = function() {get_time()}

function get_dates(id_jadwal, waktu) {
  $.ajax({
    url: get_dates_url,
    method: 'GET',
    data: {'id_jadwal': id_jadwal},
    success: function(result) {
      console.log(result)
      var id_waktu = '2'
      switch (waktu) {
        case 'Pagi': id_waktu = 'PG'; break;
        case 'Siang': id_waktu = 'SG'; break;
        case 'Sore': id_waktu = 'SR'; break;
      }
      $('#id_waktu').val(id_waktu)
      $('#id_hari').val(result.hari)

      var tanggal_table = '<table id="in-table"><tbody><tr>'
      for (var tanggal in result.tanggal) {
        var fx = "show_pasien('" + result.tanggal[tanggal]['tanggal'] + "')"
        tanggal_table += '<td class="cell" onclick=' + fx + '>' + result.tanggal[tanggal]['tanggal'] + '</td>'
      }

      tanggal_table += '</tr></tbody></table>'
      $('#td-tanggal').html(tanggal_table)
      $('#tr-tanggal').css('display', 'table-row')
      hide('pasien')
    },
    error: function(a, b) {
      console.log(a)
      console.log(b)
    }
  })
}

function show_pasien(tanggal) {
  $('#id_tanggal').val(tanggal)
  $('#tr-pasien').css('display', 'table-row')
}

if (tempat.value !== '') {
  get_time()
}

