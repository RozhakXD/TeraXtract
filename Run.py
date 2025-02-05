try:
    import sys, requests, re, json, os, time
    from rich import print as Println
    from rich.panel import Panel
    from rich.console import Console
except (ImportError, ModuleNotFoundError):
    print("Error: Module not found, please install 'requests' and 'rich' module")
    sys.exit(1)

def Banner() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')
    Println(
        Panel(
            r"""[bold blue]   _______            __   ___                  _   
  |__   __|           \ \ / / |                | |  
     | | ___ _ __ __ _ \ V /| |_ _ __ __ _  ___| |_ 
     | |/ _ \ '__/ _` | > < | __| '__/ _` |/ __| __|
     | |  __/ | | (_| |/ . \| |_| | | (_| | (__| |_ 
[bold blue]     |_|\___|_|  \__,_/_/ \_\\__|_|  \__,_|\___|\__|
        [underline red]Terabox Link Converter - Coded by Rozhak""", style="bold medium_purple4", width=60
        )
    )
    return None

def Get_Info(shorturl: str, pwd: str) -> list:
    try:
        TAUTAN = []
        with requests.Session() as session:
            session.headers.update(
                {
                    "Referer": "https://terabox.hnn.workers.dev/",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Accept-Encoding": "gzip, deflate",
                    "Connection": "keep-alive",
                    "Host": "terabox.hnn.workers.dev",
                    "Accept": "*/*",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-origin",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
                }
            )
            response = session.get('https://terabox.hnn.workers.dev/api/get-info?shorturl={}&pwd={}'.format(shorturl, pwd), allow_redirects=False, verify=True)
            if '"ok":true,' in response.text  and '"list":[{"' in response.text:
                json_data = json.loads(response.text)
                shareid, uk, sign, timestamp = json_data['shareid'], json_data['uk'], json_data['sign'], json_data['timestamp']
                finds_filename = re.findall(r'"filename":"(.*?)"', response.text)
                finds_fs_id = re.findall(r'"fs_id":(\d+)', response.text)
                finds_size = re.findall(r'"size":(\d+)', response.text)
                if not (finds_fs_id and finds_filename and finds_size):
                    Println(f"[bold medium_purple4]   ──>[bold red] ERROR: MISSING FS_ID, FILENAME, OR SIZE!         ", end="\r")
                    time.sleep(4.5)
                    return None
                else:
                    for i in range(len(finds_fs_id)):
                        try:
                            filename, fs_id, size = finds_filename[i], finds_fs_id[i], finds_size[i]
                            Get_Download(session, {"shareid": shareid, "uk": uk, "sign": sign, "timestamp": timestamp, "fs_id": fs_id, "filename": filename, "size": size}, TAUTAN)
                        except (IndexError, KeyError):
                            continue
                    return TAUTAN
            else:
                Println(f"[bold medium_purple4]   ──>[bold red] CANNOT FIND FILE INFORMATION!         ", end="\r")
                time.sleep(4.5)
                return None
    except KeyboardInterrupt:
        Println(f"[bold medium_purple4]   ──>[bold red] CANCELLED BY USER!         ", end="\r")
        time.sleep(3.5)
        return TAUTAN

def Get_Download(session: requests.Session, dict_data: dict, TAUTAN) -> bool:
    data = {
        "shareid": dict_data["shareid"],
        "uk": dict_data["uk"],
        "sign": dict_data["sign"],
        "timestamp": dict_data["timestamp"],
        "fs_id": dict_data["fs_id"]
    }
    session.headers.update(
        {
            "Content-Length": "{}".format(len(json.dumps(dict_data))),
            "Origin": "https://terabox.hnn.workers.dev",
            "Content-Type": "application/json"
        }
    )
    response = session.post('https://terabox.hnn.workers.dev/api/get-download', json=data, verify=True, allow_redirects=False)
    if '"downloadLink":"' in response.text:
        json_data = json.loads(response.text)
        size_in_mb = int(dict_data['size']) / (1024 * 1024)
        Println(Panel(f"""[bold white]Status:[bold green] Successfully!
[bold white]Link:[bold green] {str(json_data['downloadLink'])[:48]}
[bold white]Size:[bold green] {size_in_mb:.2f} MB
[bold white]Filename:[bold green] {dict_data['filename']}""", style="bold medium_purple4", width=60, title="[bold medium_purple4]>> [Success] <<", title_align="center"))
        time.sleep(2.5)
        TAUTAN.append(
            {
                "Filename": dict_data['filename'],
                "Link": json_data['downloadLink'],
                "Size": size_in_mb
            }
        )
        return True
    else:
        Println(f"[bold medium_purple4]   ──>[bold red] CANNOT FIND DOWNLOAD LINK!         ", end="\r")
        time.sleep(4.5)
        return False

def Features() -> None:
    Banner()
    Println(Panel(f"[bold white]Silakan Masukkan Tautan Terabox Yang Ingin Diubah Menja\ndi Tautan Unduhan, Contoh:[bold green] https://terabox.com/s/14Cy\nC8E6Gk9vaPa54uLS-YQ[bold white] *[bold red]Hanya Bisa Memasukkan Satu Tautan[bold white]!", style="bold medium_purple4", width=60, title="[bold medium_purple4]>> [Terabox Link] <<", title_align="center", subtitle="[bold medium_purple4]╭──────", subtitle_align="left"))
    terabox_link = Console().input("[bold medium_purple4]   ╰─> ")
    if '/s/' in terabox_link:
        shorturl = re.findall(r'/s/([^/?]*)', terabox_link)[0]
        Println(Panel(f"[bold white]Silakan Masukkan Katasandi Jika File Tersebut Terkunci, Tekan \"[bold green]Enter[bold white]\" Jika Tidak File Tidak Terkunci!", style="bold medium_purple4", width=60, title="[bold medium_purple4]>> [Passwords] <<", title_align="center", subtitle="[bold medium_purple4]╭──────", subtitle_align="left"))
        pwd = Console().input("[bold medium_purple4]   ╰─> ")
        Println(Panel(f"[bold white]Gunakan[bold green] CTRL + C[bold white] Untuk Menghentikan Konversi Tautan, *[bold red]Ingat, Untuk Tidak Menggunakan CTRL + Z[bold white]!", style="bold medium_purple4", width=60, title="[bold medium_purple4]>> [Notes] <<", title_align="center"))
        link = Get_Info(shorturl, pwd)
        if link is not None:
            file_name = f"Temporary/{str(int(time.time()))}.json"
            with open(f"{file_name}", "w+") as f:
                json.dump(link, f, indent=4)
            Println(Panel(f"[bold green]Selamat![bold white] Kami Sudah Berhasil Menyimpan Semua Tautan Ke Dalam File[bold yellow] {file_name}[bold white]!", style="bold medium_purple4", width=60, title="[bold medium_purple4]>> [Completed] <<", title_align="center"))
            sys.exit(0)
        else:
            Println(
                Panel(f"[bold red]Maaf, Tidak Ada Tautan Unduhan Yang Berhasil Ditemukan, Silakan Coba Dengan Tautan Terabox Lain!", style="bold medium_purple4", width=60, title="[bold medium_purple4]>> [Empty Link] <<", title_align="center"))
            sys.exit(1)
    else:
        Println(Panel(f"[bold red]Maaf, Sepertinya Tautan Yang Anda Masukkan Salah, Silaka\nn Coba Lagi Dengan Tautan Yang Berbeda!", style="bold medium_purple4", width=60, title="[bold medium_purple4]>> [Wrong Link] <<", title_align="center"))
        sys.exit(1)

if __name__ == '__main__':
    try:
        os.makedirs("Temporary", exist_ok=True)
        Features()
    except KeyboardInterrupt:
        sys.exit(1)
    except Exception as e:
        Println(Panel(f"[bold red]{str(e).title()}!", style="bold medium_purple4", width=60, title="[bold medium_purple4]>> [Error] <<", title_align="center"))
        sys.exit(1)