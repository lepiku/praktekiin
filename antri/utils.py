from calendar import HTMLCalendar
from .models import Hari

class Calendar(HTMLCalendar):
    def __init__(self, hari=Hari):
        super().__init__(firstweekday=6)
        self.hari = hari

    def formatday(self, day, weekday):
        """Return a day as a table cell."""
        if self.hari.objects.filter(tanggal__year=self.year,
                tanggal__month=self.month, tanggal__day=day):
            banyak = len(self.hari.objects.get(tanggal__year=self.year,
                tanggal__month=self.month, tanggal__day=day)
                    .pendaftaran_set.all())
        else:
            banyak = 0

        if day == 0:
            return '<td class="%s greyed"> \
            <span class="date">%s</span>\
                    <span class="data">%s</span></td>' % \
                    (self.cssclasses[weekday], day, banyak)
        else:
            return '''
            <td class="%s">
            <a onclick="render('%s', '%s', '%s')">
            <div>
                <span class="date">%s</span>
                <span class="data">%s</span>
            </div>
            </a>
            </td>
            ''' % \
                    (self.cssclasses[weekday], day, self.month, self.year,
                            day, banyak)

    def formatweek(self, week):
        """Return a complete week as a table row."""
        s = ''.join(self.formatday(d, wd) for (d, wd) in week)
        return '<tr>%s</tr>' % s

    def formatweekheader(self):
        nama_bulan = ["",
                "Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli",
                "Agustus", "September", "Oktober", "November", "Desember"]
        nama_hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]

        header_html = '<tr><th colspan="7" class="bulan">%s %s</th></tr><tr>' % \
                (nama_bulan[self.month], self.year)
        for x in range(7):
            num = (x + self.firstweekday) % 7
            header_html += '<th class="%s">%s</th>' % (
                    self.cssclasses[num], nama_hari[num])
        return header_html + '</tr>'

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super().formatmonth(year, month)
