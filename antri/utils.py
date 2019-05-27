from calendar import HTMLCalendar
from .models import Hari

class Calendar(HTMLCalendar):
    def __init__(self, hari=Hari):
        super().__init__(firstweekday=6)
        self.hari = hari

    def formatday(self, day, weekday):
        """Return a day as a table cell."""
        if self.hari.objects.filter( tanggal__year=self.year,
                tanggal__month=self.month, tanggal__day=day):
            banyak = len(self.hari.objects.get(tanggal__year=self.year,
                tanggal__month=self.month, tanggal__day=day)
                    .pendaftaran_set.all())
        else:
            banyak = 0

        if day == 0:
            # return '<td class="noday">&nbsp;</td>'  # day outside month
            return '<td class="%s"><span style="color:grey">%s</span></td>' % \
                    (self.cssclasses[weekday], banyak)
        else:
            return '<td class="%s">%s</td>' % (self.cssclasses[weekday],
                    banyak)

    def formatweek(self, week):
        """Return a complete week as a table row."""
        s = ''.join(self.formatday(d, wd) for (d, wd) in week)
        return '<tr>%s</tr>' % s

    def formatweekheader(self):
        nama_hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
        header_html = '<tr>'
        for x in range(7):
            num = (x + self.firstweekday) % 7
            header_html += '<td class="%s">%s</td>' % (
                    self.cssclasses[num], nama_hari[num])
        return header_html + '</tr>'

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super().formatmonth(year, month)
