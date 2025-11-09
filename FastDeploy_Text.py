# coding = utf-8
import requests
import asyncio
import aiohttp
import os
import sys
from urllib.parse import urlparse
from pathlib import Path
import platform
import subprocess

#以下是Python各版本安装包的地址
PYTHON_V2716_32 = 'https://www.python.org/ftp/python/2.7.16/python-2.7.16.msi'
PYTHON_V2716_64 = 'https://www.python.org/ftp/python/2.7.16/python-2.7.16.amd64.msi'
PYTHON_V3810_32 = 'https://www.python.org/ftp/python/3.8.10/python-3.8.10.exe'
PYTHON_V3810_64 = 'https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe'
PYTHON_V3907_32 = 'https://www.python.org/ftp/python/3.9.7/python-3.9.7.exe'
PYTHON_V3907_64 = 'https://www.python.org/ftp/python/3.9.7/python-3.9.7-amd64.exe'
PYTHON_V3114_32 = 'https://www.python.org/ftp/python/3.11.4/python-3.11.4.exe'
PYTHON_V3114_64 = 'https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe'
PYTHON_V3130_32 = 'https://www.python.org/ftp/python/3.13.0/python-3.13.0.exe'
PYTHON_V3130_64 = 'https://www.python.org/ftp/python/3.13.0/python-3.13.0-amd64.exe'

#########################################################################################
#
#dengmuzhi09104@outlook.com 版权所有2
#
#########################################################################################
class Print_Controler():
    def prt(self):
        print("1.python3")
        print("2.C++")
        print("3.VisualStudioCode")
        print("4..NET")
        print("5.")

class Python_Deploy():
    def _default_download_dir(self) -> Path:
        # 常见平台的默认下载目录：~/Downloads
        dl = Path.home() / "Downloads"
        try:
            dl.mkdir(parents=True, exist_ok=True)
        except Exception:
            # 如果无法创建，回退到当前工作目录
            dl = Path.cwd()
        return dl

    async def _download_async(self, url: str, dest: Path):
        await asyncio.sleep(0.1)
        timeout = aiohttp.ClientTimeout(total=None)  # 不设总超时
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as resp:
                resp.raise_for_status()
                total = resp.headers.get('Content-Length')
                total = int(total) if total and total.isdigit() else None

                downloaded = 0
                chunk_size = 64 * 1024
                with open(dest, "wb") as f:
                    while True:
                        chunk = await resp.content.read(chunk_size)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total:
                            percent = downloaded / total * 100
                            print(f"\r已下载 {downloaded}/{total} 字节 ({percent:5.1f}%)", end="", flush=True)
                        else:
                            print(f"\r已下载 {downloaded} 字节", end="", flush=True)
                print()  # 换行

    def _guess_filename(self, url: str) -> str:
        path = urlparse(url).path
        name = os.path.basename(path)
        if not name:
            name = "downloaded_file"
        return name

    def Download_Installer(self):
        def check_system_architecture():
            architecture = platform.architecture()[0]
            if "64" in architecture:
                return 64
            else:
                return 32
        
        print("1. Python3.7")
        print("2. Python3.8")
        print("3. Python3.9")
        print("4. Python3.11")
        print("5. Python3.13")
        VersionSelection = input("请选择要下载的版本:").strip()    

        if VersionSelection == "1":
            if check_system_architecture() == 32:
                url = PYTHON_V2716_32
            if check_system_architecture() == 64:
                url = PYTHON_V2716_64

        if VersionSelection == "2":
            if check_system_architecture() == 32:
                url = PYTHON_V3810_32
            if check_system_architecture() == 64:
                url = PYTHON_V3810_64

        if VersionSelection == "3":
            if check_system_architecture() == 32:
                url = PYTHON_V3907_32
            if check_system_architecture() == 64:
                url = PYTHON_V3907_64

        if VersionSelection == "4":
            if check_system_architecture() == 32:
                url = PYTHON_V3114_32
            if check_system_architecture() == 64:
                url = PYTHON_V3114_64
        
        if VersionSelection == "5":
            if check_system_architecture() == 32:
                url = PYTHON_V3130_32
            if check_system_architecture() == 64:
                url = PYTHON_V3130_64
        if  VersionSelection not in ["1","2","3","4","5"]:
            print("无效的选择。请重新运行程序并选择有效的选项。")
        
            
            
            
        filename = self._guess_filename(url)
        dest_dir = self._default_download_dir()
        dest_path = dest_dir / filename

        print(f"准备下载到: {dest_path}")
        try:
            asyncio.run(self._download_async(url, dest_path))
            print(f"下载完成: {dest_path}")
            input("按回车键退出...")
        except aiohttp.ClientResponseError as e:
            print(f"HTTP 错误: {e.status} - {e.message if hasattr(e,'message') else str(e)}")
            input("按回车键退出...")
        except Exception as e:
            print(f"下载失败: {e}")
            input("按回车键退出...")



class CPlus_Deploy():
    def Get_System_Version(self):
        if platform.system() == 'Windows':
            Version = platform.version()

        if '10' or '11' in Version:
            Version = "NEW"

        if not '10' or '11' in Version:
            Version = "OLD"


    def Download_Mingw_Installer(self, url: str, dest: Path|str):
    
        pass

PRINT = Print_Controler()
PRINT.prt()
control01 = int(input("输入要选择部署的环境:"))

if control01 == 1:
    deploy = Python_Deploy()
    deploy.Download_Installer()

if control01 == 2:

