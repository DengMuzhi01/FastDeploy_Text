using System;
using System.IO;
using System.Net.Http;
using System.Runtime.InteropServices;
using System.Diagnostics;
using System.Threading.Tasks;

class Program
{
    static async Task<int> Main(string[] args)
    {
        Console.WriteLine("1. Python3.7");
        Console.WriteLine("2. Python3.8");
        Console.WriteLine("3. Python3.9");
        Console.WriteLine("4. Python3.11");
        Console.WriteLine("5. Python3.13");
        Console.Write("请选择要下载的版本: ");
        var selection = Console.ReadLine()?.Trim();

        string url = GetUrl(selection);
        if (url == null)
        {
            Console.WriteLine("无效的选择。请重新运行程序并选择有效的选项。");
            return 1;
        }

        var destDir = GetDefaultDownloadDir();
        var filename = Path.GetFileName(new Uri(url).LocalPath);
        if (string.IsNullOrEmpty(filename)) filename = "downloaded_file";
        var destPath = Path.Combine(destDir, filename);

        Console.WriteLine($"准备下载到: {destPath}");
        try
        {
            await DownloadWithProgress(url, destPath);
            Console.WriteLine($"\n下载完成: {destPath}");
            TryOpenFile(destPath);
        }
        catch (HttpRequestException hre)
        {
            Console.WriteLine($"HTTP 错误: {hre.Message}");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"下载失败: {ex.Message}");
        }

        Console.WriteLine("按回车键退出...");
        Console.ReadLine();
        return 0;
    }

    static string GetUrl(string selection)
    {
        bool is64 = Environment.Is64BitOperatingSystem;
        return selection switch
        {
            "1" => is64
                    ? "https://www.python.org/ftp/python/2.7.16/python-2.7.16.amd64.msi"
                    : "https://www.python.org/ftp/python/2.7.16/python-2.7.16.msi",
            "2" => is64
                    ? "https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe"
                    : "https://www.python.org/ftp/python/3.8.10/python-3.8.10.exe",
            "3" => is64
                    ? "https://www.python.org/ftp/python/3.9.7/python-3.9.7-amd64.exe"
                    : "https://www.python.org/ftp/python/3.9.7/python-3.9.7.exe",
            "4" => is64
                    ? "https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe"
                    : "https://www.python.org/ftp/python/3.11.4/python-3.11.4.exe",
            "5" => is64
                    ? "https://www.python.org/ftp/python/3.13.0/python-3.13.0-amd64.exe"
                    : "https://www.python.org/ftp/python/3.13.0/python-3.13.0.exe",
            _ => null,
        };
    }

    static string GetDefaultDownloadDir()
    {
        try
        {
            var userProfile = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
            var dl = Path.Combine(userProfile, "Downloads");
            Directory.CreateDirectory(dl);
            return dl;
        }
        catch
        {
            return Directory.GetCurrentDirectory();
        }
    }

    static async Task DownloadWithProgress(string url, string destPath)
    {
        using var http = new HttpClient();
        using var resp = await http.GetAsync(url, HttpCompletionOption.ResponseHeadersRead);
        resp.EnsureSuccessStatusCode();

        var total = resp.Content.Headers.ContentLength;
        using var contentStream = await resp.Content.ReadAsStreamAsync();
        using var fileStream = new FileStream(destPath, FileMode.Create, FileAccess.Write, FileShare.None, 64 * 1024, useAsync: true);

        var buffer = new byte[64 * 1024];
        long totalRead = 0;
        int read;
        while ((read = await contentStream.ReadAsync(buffer, 0, buffer.Length)) > 0)
        {
            await fileStream.WriteAsync(buffer, 0, read);
            totalRead += read;
            if (total.HasValue)
            {
                double percent = (double)totalRead / total.Value * 100;
                Console.Write($"\r已下载 {totalRead}/{total} 字节 ({percent:5.1f}%)");
            }
            else
            {
                Console.Write($"\r已下载 {totalRead} 字节");
            }
        }
    }

    static void TryOpenFile(string path)
    {
        try
        {
            if (RuntimeInformation.IsOSPlatform(OSPlatform.Windows))
            {
                Process.Start(new ProcessStartInfo(path) { UseShellExecute = true });
            }
            else if (RuntimeInformation.IsOSPlatform(OSPlatform.OSX))
            {
                Process.Start(new ProcessStartInfo("open", $"\"{path}\"") { UseShellExecute = false });
            }
            else // Linux / others
            {
                Process.Start(new ProcessStartInfo("xdg-open", $"\"{path}\"") { UseShellExecute = false });
            }
            Console.WriteLine($"已尝试打开: {path}");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"无法自动打开文件: {ex.Message}");
        }
    }
}
