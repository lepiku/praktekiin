from calendar import HTMLCalendar
from .models import Hari
from django.utils import timezone

class Calendar(HTMLCalendar):
    nama_bulan = ("", "Januari", "Februari", "Maret", "April", "Mei",
       "Juni", "Juli", "Agustus", "September", "Oktober", "November",
       "Desember")
    nama_hari = ("Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu",
       "Minggu")
    cssclass_month = "calendar"

    def __init__(self, hari=Hari):
        super().__init__(firstweekday=6)
        self.hari = hari

    def formatday(self, day, weekday):
        """Return a day as a table cell."""
        try:
            banyak = self.hari.objects.get(tanggal__year=self.year,
                tanggal__month=self.month, tanggal__day=day).jumlah_pendaftar()
        except:
            banyak = 0

        # if day is not in the month
        if day == 0:
            return '''
<td class="%s" />
            ''' % (self.cssclasses[weekday])
        # if day is in the month
        else:
            data = ''
            if banyak > 0:
                data = '<span class="amount">%s</span>' % banyak

            now = timezone.now()
            today = ""
            if now.year == self.year and now.month == self.month and \
                    now.day == day:
                today = " today"
            return '''
<td class="{0}"><a onclick="render('{1}', '{2}', '{3}')" title="{1} {4} {3}">
<div class="cell{6}"><span class="date">{1}</span>{5}</div></a></td>'''.format(
        self.cssclasses[weekday], day, self.month, self.year,
        self.nama_bulan[self.month], data, today)

    def formatweek(self, week):
        """Return a complete week as a table row."""
        s = ''.join(self.formatday(d, wd) for (d, wd) in week)
        return '<tr>%s</tr>' % s

    def formatweekheader(self):
        """add week header with Indonesian language"""

        # current month and year
        header_html = '''
<tr><th colspan="7"><div class="bulan">%s %s</div></th></tr>
<tr class="hari">''' % (
        self.nama_bulan[self.month], self.year)

        # name of days
        for x in range(7):
            num = (x + self.firstweekday) % 7
            header_html += '<th class="%s"><div class="cell nohover">%s</div></th>' % (
                    self.cssclasses[num], self.nama_hari[num])
        return header_html + '</tr>'

    def formatmonth(self, year, month):
        """Display the calendar in a month"""
        self.year, self.month = year, month

        return super().formatmonth(year, month)

    def formatmonthname(self, year, month, withyear=False):
        return ''
