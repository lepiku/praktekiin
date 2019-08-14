function antri() {
  $.ajax({
    url: get_antri_url,
    method: 'GET',
    data: {},
    success: function(result) {
      console.log(result)
      var table = document.getElementsByClassName('table')[0]
      var tbody = document.createElement('tbody')
      table.appendChild(tbody)

      var tr = document.createElement('tr')
      tbody.appendChild(tr)

      if (result.data !== null) {
        for (var head of result.table_head) {
          var th = document.createElement('th')
          th.className = head.toLowerCase().replace(/ /g, '-').replace('.', '')
          th.appendChild(document.createTextNode(head))
          tr.appendChild(th)
        }

        for (var x in result.data) {
          var tr = document.createElement('tr')
          tbody.appendChild(tr)

          for (var y in result.data[x]) {
            if (y === 'pasien_url') {
              continue
            }
            var td = document.createElement('td')
            tr.appendChild(td)
            if (result.staff && y === 'nama') {
              anchor = document.createElement('a')
              anchor.href = result.data[x]['pasien_url']
              anchor.appendChild(document.createTextNode(result.data[x][y]))
              td.appendChild(anchor)
            } else {
              td.appendChild(document.createTextNode(result.data[x][y]))
            }
          }
        }

        $('input[name="pasien_set"]').prop('checked', false)
        result.pasien_set.forEach(function (value, index) {
          $('input[name="pasien_set"][value="' + value + '"]').prop('checked', true)
        })

        if (result.pasien_set.length > 0) {
          $('#hari-ini').css('background-color', '#D458FF')
          $('#hari-ini').html('Ubah Antri Hari ini')
          $('input[name="antri"]').css('background-color', '#D458FF')
          $('input[name="antri"]').val('Ubah Antri Hari ini')
        }
      } else {
        var td = document.createElement('td')
        td.appendChild(document.createTextNode('Belum ada yang mendaftar'))
        tr.appendChild(td)
      }
    },
    error: function(a, b) {
      console.log(a)
      console.log(b)
    }
  })
}

antri()

function show_popup() {
  $('#popup').css('display', 'block')
}
function hide_popup() {
  $('#popup').css('display', 'none')
}
