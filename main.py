import csv
import datetime
import os
from typing import List

matakuliah_csv = 'matakuliah.csv'
tugas_csv = 'tugas.csv'

hari = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']

def muat_matakuliah() -> List[dict]:
    daftar_matkul = []
    if os.path.exists(matakuliah_csv):
        with open(matakuliah_csv, newline='', encoding='utf-8') as f:
            pembaca = csv.DictReader(f)
            for baris in pembaca:
                # Pastikan tipe data sesuai
                baris['JamMulai'] = baris['JamMulai']
                baris['JamSelesai'] = baris['JamSelesai']
                baris['Hari'] = baris['Hari']
                baris['IDMatakuliah'] = int(baris['IDMatakuliah'])
                baris['NamaMatakuliah'] = baris['NamaMatakuliah']
                daftar_matkul.append(baris)
    return daftar_matkul

def simpan_matkul(daftar_matkul: List[dict]):
    with open(matakuliah_csv, 'w', newline='', encoding='utf-8') as f:
        nama_kolom = ['IDMatakuliah', 'NamaMatakuliah', 'Hari', 'JamMulai', 'JamSelesai']
        penulis = csv.DictWriter(f, fieldnames=nama_kolom)
        penulis.writeheader()
        for matkul in daftar_matkul:
            penulis.writerow(matkul)

def muat_tugas() -> List[dict]:
    daftar_tugas = []
    if os.path.exists(tugas_csv):
        with open(tugas_csv, newline='', encoding='utf-8') as f:
            pembaca = csv.DictReader(f)
            for baris in pembaca:
                baris['IDTugas'] = int(baris['IDTugas'])
                baris['DurasiEstimasi'] = float(baris['DurasiEstimasi'])  # <== disesuaikan
                baris['BatasWaktu'] = baris['BatasWaktu']  # <== disesuaikan
                baris['Status'] = baris['Status']
                baris['NamaTugas'] = baris['NamaTugas']
                daftar_tugas.append(baris)
    return daftar_tugas

def simpan_tugas(daftar_tugas: List[dict]):
    with open(tugas_csv, 'w', newline='', encoding='utf-8') as f:
        nama_kolom = ['IDTugas', 'NamaTugas', 'DurasiEstimasi', 'BatasWaktu', 'Status']  # <== disesuaikan
        penulis = csv.DictWriter(f, fieldnames=nama_kolom)
        penulis.writeheader()
        for tugas in daftar_tugas:
            penulis.writerow(tugas)

def hapus_tugas_selesai():
    daftar_tugas = muat_tugas()
    daftar_tugas = [t for t in daftar_tugas if t['Status'].lower() != 'selesai']
    simpan_tugas(daftar_tugas)

def str_ke_waktu(waktu_str: str) -> datetime.time:
    return datetime.datetime.strptime(waktu_str, '%H:%M').time()

def waktu_ke_str(waktu: datetime.time) -> str:
    return waktu.strftime('%H:%M')

def hari_ini() -> str:
    return datetime.datetime.today().strftime('%A')

def cetak_garis():
    print('-' * 50)

def input_waktu(prompt: str) -> str:
    while True:
        t = input(prompt + " (HH:MM, format 24 jam): ")
        try:
            datetime.datetime.strptime(t, '%H:%M')
            return t
        except ValueError:
            print("Format waktu tidak valid. Masukkan dalam format HH:MM 24 jam.")

def input_hari() -> str:
    while True:
        hari_input = input("Masukkan nama hari (contoh: Senin): ").capitalize()
        if hari_input in hari:
            return hari_input
        print("Hari tidak valid. Masukkan nama hari yang benar, misal: Senin.")

def id_matkul_berikutnya(daftar_matkul):
    if daftar_matkul:
        return max(m['IDMatakuliah'] for m in daftar_matkul) + 1
    return 1

def id_tugas_berikutnya(daftar_tugas):
    if daftar_tugas:
        return max(t['IDTugas'] for t in daftar_tugas) + 1
    return 1

def tumpang_tindih(mulai1, selesai1, mulai2, selesai2) -> bool:
    # semua argumen bertipe datetime.time
    return not (selesai1 <= mulai2 or selesai2 <= mulai1)

def cetak_matkul_hari_ini(daftar_matkul, hari_terpilih):
    print(f"Jadwal Mata Kuliah pada hari {hari_terpilih}:")
    yang_terpilih = [m for m in daftar_matkul if m['Hari'] == hari_terpilih]
    if not yang_terpilih:
        print("  Tidak ada mata kuliah hari ini.")
        return []
    yang_terpilih.sort(key=lambda x: str_ke_waktu(x['JamMulai']))
    for m in yang_terpilih:
        print(f"  [{m['IDMatakuliah']}] {m['NamaMatakuliah']} dari {m['JamMulai']} sampai {m['JamSelesai']}")
    return yang_terpilih

def menu_admin():
    daftar_matkul = muat_matakuliah()
    while True:
        cetak_garis()
        print("MENU ADMIN - Kelola Mata Kuliah")
        print("1. Lihat Jadwal Mata Kuliah per Hari")
        print("2. Tambah Mata Kuliah")
        print("3. Edit Mata Kuliah")
        print("4. Hapus Mata Kuliah")
        print("5. Kembali ke Pilihan Peran")
        pilihan = input("Pilih opsi: ")
        
        if pilihan == '1':
            hari_terpilih = input_hari()
            cetak_matkul_hari_ini(daftar_matkul, hari_terpilih)
        
        elif pilihan == '2':
            nama_matkul = input("Masukkan nama mata kuliah: ").strip()
            hari_input = input_hari()
            jam_mulai = input_waktu("Masukkan waktu mulai")
            jam_selesai = input_waktu("Masukkan waktu selesai")
            if str_ke_waktu(jam_selesai) <= str_ke_waktu(jam_mulai):
                print("Waktu selesai harus setelah waktu mulai. Mata kuliah tidak ditambahkan.")
                continue
            
            # Cek tumpang tindih di hari yang sama
            tumpang_tindih_ada = False
            for m in daftar_matkul:
                if m['Hari'] == hari_input:
                    if tumpang_tindih(str_ke_waktu(jam_mulai), str_ke_waktu(jam_selesai),
                                      str_ke_waktu(m['JamMulai']), str_ke_waktu(m['JamSelesai'])):
                        print(f"Tumpang tindih dengan mata kuliah [{m['IDMatakuliah']}] {m['NamaMatakuliah']} {m['JamMulai']}–{m['JamSelesai']}")
                        tumpang_tindih_ada = True
                        break
            if tumpang_tindih_ada:
                print("Tidak bisa menambahkan mata kuliah yang tumpang tindih.")
                continue
            
            id_baru = id_matkul_berikutnya(daftar_matkul)
            matkul_baru = {
                'IDMatakuliah': id_baru,
                'NamaMatakuliah': nama_matkul,
                'Hari': hari_input,
                'JamMulai': jam_mulai,
                'JamSelesai': jam_selesai
            }
            daftar_matkul.append(matkul_baru)
            simpan_matkul(daftar_matkul)
            print(f"Mata kuliah berhasil ditambahkan dengan ID {id_baru}.")
        
        elif pilihan == '3':
            try:
                id_edit = int(input("Masukkan ID mata kuliah yang akan diedit: "))
            except ValueError:
                print("ID tidak valid.")
                continue
            
            hasil_cari = [m for m in daftar_matkul if m['IDMatakuliah'] == id_edit]
            if not hasil_cari:
                print("Mata kuliah tidak ditemukan.")
                continue
            
            matkul_edit = hasil_cari[0]
            print(f"Mengedit Mata Kuliah [{matkul_edit['IDMatakuliah']}] {matkul_edit['NamaMatakuliah']} {matkul_edit['Hari']} {matkul_edit['JamMulai']}-{matkul_edit['JamSelesai']}")
            
            nama_baru = input(f"Nama mata kuliah baru (kosongkan untuk mempertahankan '{matkul_edit['NamaMatakuliah']}'): ").strip()
            if nama_baru:
                matkul_edit['NamaMatakuliah'] = nama_baru
            
            hari_baru = input(f"Hari baru (kosongkan untuk mempertahankan '{matkul_edit['Hari']}'): ").capitalize().strip()
            if hari_baru:
                if hari_baru not in hari:
                    print("Hari tidak valid. Edit dibatalkan.")
                    continue
                matkul_edit['Hari'] = hari_baru
            
            mulai_baru = input(f"Waktu mulai baru (kosongkan untuk mempertahankan '{matkul_edit['JamMulai']}'): ").strip()
            if mulai_baru:
                try:
                    datetime.datetime.strptime(mulai_baru, '%H:%M')
                    matkul_edit['JamMulai'] = mulai_baru
                except:
                    print("Format waktu tidak valid. Edit dibatalkan.")
                    continue
            
            selesai_baru = input(f"Waktu selesai baru (kosongkan untuk mempertahankan '{matkul_edit['JamSelesai']}'): ").strip()
            if selesai_baru:
                try:
                    datetime.datetime.strptime(selesai_baru, '%H:%M')
                    matkul_edit['JamSelesai'] = selesai_baru
                except:
                    print("Format waktu tidak valid. Edit dibatalkan.")
                    continue
            
            if str_ke_waktu(matkul_edit['JamSelesai']) <= str_ke_waktu(matkul_edit['JamMulai']):
                print("Waktu selesai harus setelah waktu mulai. Edit dibatalkan.")
                continue
            
            # Cek tumpang tindih dengan matkul lain kecuali dirinya sendiri
            tumpang_tindih_ada = False
            for m in daftar_matkul:
                if m['IDMatakuliah'] != matkul_edit['IDMatakuliah'] and m['Hari'] == matkul_edit['Hari']:
                    if tumpang_tindih(str_ke_waktu(matkul_edit['JamMulai']), str_ke_waktu(matkul_edit['JamSelesai']),
                                      str_ke_waktu(m['JamMulai']), str_ke_waktu(m['JamSelesai'])):
                        print(f"Tumpang tindih dengan mata kuliah [{m['IDMatakuliah']}] {m['NamaMatakuliah']} {m['JamMulai']}–{m['JamSelesai']}")
                        tumpang_tindih_ada = True
                        break
            if tumpang_tindih_ada:
                print("Hasil edit menyebabkan tumpang tindih mata kuliah. Edit dibatalkan.")
                continue
            
            simpan_matkul(daftar_matkul)
            print("Mata kuliah berhasil diedit.")
        
        elif pilihan == '4':
            try:
                id_hapus = int(input("Masukkan ID mata kuliah yang akan dihapus: "))
            except ValueError:
                print("ID tidak valid.")
                continue
            
            jumlah_sebelum = len(daftar_matkul)
            daftar_matkul = [m for m in daftar_matkul if m['IDMatakuliah'] != id_hapus]
            
            if len(daftar_matkul) == jumlah_sebelum:
                print("ID mata kuliah tidak ditemukan.")
            else:
                simpan_matkul(daftar_matkul)
                print(f"Mata kuliah dengan ID {id_hapus} berhasil dihapus.")
        
        elif pilihan == '5':
            break
        
        else:
            print("Pilihan tidak valid.")

def user_menu():
    hapus_tugas_selesai()
    courses = muat_matakuliah()
    tasks = muat_tugas()
    today = hari_ini()
    # Filter lectures for today and sort
    today_lectures = [c for c in courses if c['Hari'] == today]
    today_lectures.sort(key=lambda x: str_ke_waktu(x['JamMulai']))
    while True:
        cetak_garis()
        print(f"USER MENU - Manajemen Tugas (Hari ini: {today})")
        print("Jadwal Mata Kuliah Hari Ini:")
        if not today_lectures:
            print("  Tidak ada mata kuliah hari ini.")
        else:
            for c in today_lectures:
                print(f"  {c['NamaMatakuliah']} dari {c['JamMulai']} sampai {c['JamSelesai']}")
        cetak_garis()
        print("1. Lihat semua tugas")
        print("2. Tambah tugas")
        print("3. Edit tugas")
        print("4. Hapus tugas")
        print("5. Tandai tugas selesai")
        print("6. Lihat jadwal hari ini dengan tugas yang dijadwalkan di waktu kosong")
        print("7. Kembali ke Pilihan Peran")
        choice = input("Pilih opsi: ")
        if choice == '1':
            if not tasks:
                print("Tidak ada tugas yang terdaftar.")
            else:
                print("Tugas Terdaftar:")
                for t in tasks:
                    print(f"  [{t['IDTugas']}] {t['NamaTugas']} Durasi:{t['DurasiEstimasi']} jam Batas Waktu:{t['BatasWaktu']} Status:{t['Status']}")
        elif choice == '2':
            task_name = input("Nama tugas: ").strip()
            while True:
                try:
                    est_duration = float(input("Estimasi durasi (jam, misal 1.5): "))
                    if est_duration <= 0:
                        print("Harus berupa angka positif.")
                        continue
                    break
                except:
                    print("Input tidak valid, masukkan angka.")
            deadline = input("Batas waktu (YYYY-MM-DD, kosongkan jika tidak ada): ").strip()
            if deadline:
                try:
                    datetime.datetime.strptime(deadline, '%Y-%m-%d')
                except:
                    print("Format tanggal tidak valid. Tugas tidak ditambahkan.")
                    continue
            else:
                deadline = ''
            new_task_id = id_tugas_berikutnya(tasks)
            tasks.append({'IDTugas': new_task_id, 'NamaTugas': task_name,
                          'DurasiEstimasi': est_duration, 'BatasWaktu': deadline,
                          'Status': 'Pending'})
            simpan_tugas(tasks)
            print(f"Tugas '{task_name}' ditambahkan dengan ID {new_task_id}.")
        elif choice == '3':
            try:
                task_id = int(input("Masukkan ID tugas yang ingin diedit: "))
            except:
                print("ID tidak valid.")
                continue
            matched = [t for t in tasks if t['IDTugas'] == task_id]
            if not matched:
                print("Tugas tidak ditemukan.")
                continue
            t = matched[0]
            print(f"Mengedit Tugas [{t['IDTugas']}] {t['NamaTugas']} Durasi:{t['DurasiEstimasi']} jam Batas Waktu:{t['BatasWaktu']} Status:{t['Status']}")
            new_name = input(f"Nama baru (kosongkan untuk mempertahankan '{t['NamaTugas']}'): ").strip()
            if new_name:
                t['NamaTugas'] = new_name
            new_dur = input(f"Estimasi durasi baru (kosongkan untuk mempertahankan {t['DurasiEstimasi']}): ").strip()
            if new_dur:
                try:
                    d = float(new_dur)
                    if d <= 0:
                        print("Durasi harus positif. Edit dibatalkan.")
                        continue
                    t['DurasiEstimasi'] = d
                except:
                    print("Durasi tidak valid. Edit dibatalkan.")
                    continue
            new_deadline = input(f"Batas waktu baru (YYYY-MM-DD, kosongkan untuk mempertahankan '{t['BatasWaktu']}'): ").strip()
            if new_deadline:
                try:
                    datetime.datetime.strptime(new_deadline, '%Y-%m-%d')
                    t['BatasWaktu'] = new_deadline
                except:
                    print("Format tanggal tidak valid. Edit dibatalkan.")
                    continue
            new_status = input(f"Status (Pending/Completed), kosongkan untuk mempertahankan '{t['Status']}': ").strip().capitalize()
            if new_status:
                if new_status not in ['Pending', 'Completed']:
                    print("Status tidak valid. Edit dibatalkan.")
                    continue
                t['Status'] = new_status
            simpan_tugas(tasks)
            print("Tugas berhasil diedit.")
            hapus_tugas_selesai()  # Hapus tugas selesai segera
        elif choice == '4':
            try:
                task_id = int(input("Masukkan ID tugas yang ingin dihapus: "))
            except:
                print("ID tidak valid.")
                continue
            before_len = len(tasks)
            tasks = [t for t in tasks if t['IDTugas'] != task_id]
            if len(tasks) == before_len:
                print("ID tugas tidak ditemukan.")
            else:
                simpan_tugas(tasks)
                print(f"Tugas dengan ID {task_id} berhasil dihapus.")
        elif choice == '5':
            try:
                task_id = int(input("Masukkan ID tugas yang ingin ditandai selesai: "))
            except:
                print("ID tidak valid.")
                continue
            found = False
            for t in tasks:
                if t['IDTugas'] == task_id:
                    t['Status'] = 'Completed'
                    found = True
                    break
            if not found:
                print("Tugas tidak ditemukan.")
            else:
                simpan_tugas(tasks)
                print(f"Tugas dengan ID {task_id} ditandai selesai dan akan dihapus.")
                hapus_tugas_selesai()
                tasks = muat_tugas()
        elif choice == '6':
            # Tampilkan jadwal hari ini dengan tugas yang dijadwalkan di waktu kosong
            free_intervals = get_free_intervals(today_lectures)

            if not free_intervals:
                print("Tidak ada waktu kosong antara mata kuliah hari ini.")
                continue

            from datetime import date
            today_date = date.today()
            filtered_tasks = []
            for t in tasks:
                if t['Status'].lower() != 'pending':
                    continue
                if t['BatasWaktu']:
                    try:
                        dl = datetime.datetime.strptime(t['BatasWaktu'], '%Y-%m-%d').date()
                        if dl < today_date:
                            continue  # deadline lewat
                    except:
                        pass
                filtered_tasks.append(t)

            if not filtered_tasks:
                print("Tidak ada tugas pending yang dapat dijadwalkan hari ini.")
                continue

            schedule = jadwal_knapsack(free_intervals, filtered_tasks)

            print("Jadwal Hari Ini dengan Tugas:")
            events = []
            for lec in today_lectures:
                start = str_ke_waktu(lec['JamMulai'])
                end = str_ke_waktu(lec['JamSelesai'])
                events.append(('Mata Kuliah', lec['NamaMatakuliah'], start, end))
            for sch in schedule:
                events.append(('Tugas', sch['task']['NamaTugas'], sch['start_time'], sch['end_time']))
            events.sort(key=lambda x: x[2])

            for ev in events:
                st = waktu_ke_str(ev[2])
                et = waktu_ke_str(ev[3])
                print(f"  [{ev[0]}] {ev[1]} dari {st} sampai {et}")

        elif choice == '7':
            break
        else:
            print("Pilihan tidak valid.")


def get_free_intervals(lectures: list) -> list:
    import datetime
    DAY_START = datetime.time(6, 0)
    DAY_END = datetime.time(22, 0)
    if not lectures:
        return [(DAY_START, DAY_END)]
    free_intervals = []
    lectures_sorted = sorted(lectures, key=lambda x: str_ke_waktu(x['JamMulai']))
    if str_ke_waktu(lectures_sorted[0]['JamMulai']) > DAY_START:
        free_intervals.append((DAY_START, str_ke_waktu(lectures_sorted[0]['JamMulai'])))
    for i in range(len(lectures_sorted) - 1):
        end_prev = str_ke_waktu(lectures_sorted[i]['JamSelesai'])
        start_next = str_ke_waktu(lectures_sorted[i + 1]['JamMulai'])
        if start_next > end_prev:
            free_intervals.append((end_prev, start_next))
    if str_ke_waktu(lectures_sorted[-1]['JamSelesai']) < DAY_END:
        free_intervals.append((str_ke_waktu(lectures_sorted[-1]['JamSelesai']), DAY_END))
    return free_intervals


import datetime
from typing import List, Tuple

def durasi_dalam_jam(mulai: datetime.time, selesai: datetime.time) -> float:
    dt1 = datetime.datetime.combine(datetime.date.today(), mulai)
    dt2 = datetime.datetime.combine(datetime.date.today(), selesai)
    selisih = dt2 - dt1
    return selisih.total_seconds() / 3600

def tambah_jam(mulai: datetime.time, jam: float) -> datetime.time:
    dt = datetime.datetime.combine(datetime.date.today(), mulai)
    delta = datetime.timedelta(hours=jam)
    waktu_akhir = dt + delta
    return waktu_akhir.time()

def jadwal_knapsack(interval_kosong: List[Tuple[datetime.time, datetime.time]], tugas_list: List[dict]) -> List[dict]:
    """
    Menjadwalkan tugas ke interval kosong menggunakan pendekatan greedy:
    Mengutamakan tugas dengan DurasiEstimasi terbesar masuk ke slot waktu yang tersedia.
    """
    # Urutkan tugas berdasarkan DurasiEstimasi secara menurun
    tugas_urut = sorted(tugas_list, key=lambda x: x['DurasiEstimasi'], reverse=True)

    jadwal = []
    slot_kosong = [(mulai, selesai, durasi_dalam_jam(mulai, selesai)) for (mulai, selesai) in interval_kosong]

    for tugas in tugas_urut:
        durasi_tugas = tugas['DurasiEstimasi']
        for idx, (mulai, selesai, durasi_slot) in enumerate(slot_kosong):
            if durasi_slot >= durasi_tugas:
                # Jadwalkan tugas mulai dari waktu mulai slot kosong
                mulai_tugas = mulai
                selesai_tugas = tambah_jam(mulai, durasi_tugas)
                jadwal.append({
                    'tugas': tugas,
                    'waktu_mulai': mulai_tugas,
                    'waktu_selesai': selesai_tugas
                })

                # Update slot kosong, kurangi waktu yang sudah dipakai tugas
                mulai_baru = selesai_tugas
                selesai_baru = selesai
                durasi_baru = durasi_dalam_jam(mulai_baru, selesai_baru)
                if durasi_baru > 0:
                    slot_kosong[idx] = (mulai_baru, selesai_baru, durasi_baru)
                else:
                    slot_kosong.pop(idx)
                break
    return jadwal

def pemilihan_role():
    hapus_tugas_selesai()
    while True:
        cetak_garis()
        print("Selamat datang di Sistem Manajemen Kuliah dan Tugas (Versi Console)")
        print("Pilih Role:")
        print("1. Admin (Kelola Matakuliah/Kuliah)")
        print("2. User (Kelola Tugas)")
        print("3. Keluar")
        pilihan = input("Pilih role: ")
        if pilihan == '1':
            menu_admin()
        elif pilihan == '2':
            user_menu()
        elif pilihan == '3':
            print("Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    pemilihan_role()