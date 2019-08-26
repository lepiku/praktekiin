function hapus_pasien(id, name) {
  console.log('pasien', id)
  if (confirm("Apa kamu yakin mau menghapus pasien '" + name + "'?")) {
    window.location = hapus_pasien_url + '?id=' + id
  }
}
