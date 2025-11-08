# coding = utf-8
import requests
import asyncio
import aiohttp
import os
import sys
from urllib.parse import urlparse
from pathlib import Path

class Print_Controler():
    def prt(self):
        print("1.python3")
        print("2.C++")
        print("3.VisualStudioCode")
        print("4..NET")
        print("")

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
        url = input("请输入要下载的链接: ").strip()
        if not url:
            print("未输入链接，退出。")
            return

        filename = self._guess_filename(url)
        dest_dir = self._default_download_dir()
        dest_path = dest_dir / filename

        print(f"准备下载到: {dest_path}")
        try:
            asyncio.run(self._download_async(url, dest_path))
            print(f"下载完成: {dest_path}")
        except aiohttp.ClientResponseError as e:
            print(f"HTTP 错误: {e.status} - {e.message if hasattr(e,'message') else str(e)}")
        except Exception as e:
            print(f"下载失败: {e}")

PRINT = Print_Controler()
PRINT.prt()
control01 = int(input("输入要选择部署的环境:"))

if control01 == 1:
    deploy = Python_Deploy()
    deploy.Download_Installer()
