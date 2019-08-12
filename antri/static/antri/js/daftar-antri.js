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
            var fx = "get_dates(" + j[x]['id'] + ", '" + key + "', this)"
            waktu_table += '<td class="cell c-waktu" onclick="' + fx + '">' + j[x]['jam'] + '</td>'
          }
          waktu_table += '</tr>'
        }

        waktu_table += '</tbody></table>'
        hide('tanggal')
        $('#td-waktu').html(waktu_table)
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

function get_dates(id_jadwal, waktu, element) {
  $('.c-waktu').css('background-color', '#39B0A3')
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
      result.tanggal_list.forEach(function(value, _) {
        var fx = "get_pasien('" + value['tanggal'] + "', this)"
        tanggal_table += '<td class="cell c-tanggal" onclick="' + fx + '">' + value['repr'] + '</td>'
      })

      tanggal_table += '</tr></tbody></table>'
      hide('pasien')
      $('#td-tanggal').html(tanggal_table)
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

