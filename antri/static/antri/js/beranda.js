function antri() {
  $.ajax({
    url: get_antri_url,
    method: 'GET',
    data: {},
    success: function(result) {
      console.log(result)
      var table = document.getElementById('antri')
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

        for (var x = 0; x < result.data.length; x++) {
          var tr = document.createElement('tr')
          tbody.appendChild(tr)

          for (y in result.data[x]) {
            var td = document.createElement('td')
            td.appendChild(document.createTextNode(result.data[x][y]))
            tr.appendChild(td)
          }
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

