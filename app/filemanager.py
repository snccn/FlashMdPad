# coding:utf-8
import os
import platform
import sys

class FileManager(object):
    """ 文件管理: 默认路径 win: data 文件安装路径 macos: ~/.flashpad/"""
    FileList = []
    path = ""
    def __init__(self, basepath=""):
        if os.name == "nt":
            if getattr(sys, 'frozen', False):
                self.path = os.path.join(os.path.dirname(sys.argv[-1]),"data")
            else:
                self.path = os.path.join(os.path.dirname(__file__),"data")
        else:
            self.path = os.path.expanduser("~/.flashpad/")
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.GetFileList()
        pass

    def list_files(self,path):
        for entry in os.scandir(path):
            if entry.is_file():
                yield entry.path
            elif entry.is_dir(follow_symlinks=False):  # Avoid symlink loops
                yield from self.list_files(entry.path)

    def GetFileList(self):
        for file_path in self.list_files(self.path):
            if file_path.split(".")[-1] == 'db':
                pass
            else:
                self.FileList.append(file_path)
    def delete_file(self, path):
        return delete_file_by_name(path=path)


from pathlib import Path

def delete_file_by_name(path):
    file_path = Path(path)

    if file_path.exists() and file_path.is_file():
        try:
            file_path.unlink()  # 删除文件
            print(f"文件 '{file_path}' 已成功删除")
            return True
        except OSError as e:
            print(f"删除失败: {e.strerror}")
            return False
    else:
        print(f"文件 '{file_path}' 不存在")
        return False

def rename_with_pathlib(old_path, new_path):
    """
    使用 pathlib 重命名文件（更现代化的方法）
    
    参数:
        old_path (str): 原始文件路径
        new_path (str): 新文件路径
    """
    try:
        old_file = Path(old_path)
        new_file = Path(new_path)
        
        if not old_file.exists():
            print(f"错误: 文件 {old_path} 不存在")
            return False
            
        if new_file.exists():
            print(f"错误: 文件 {new_path} 已存在")
            return False
            
        old_file.rename(new_file)
        print(f"文件已重命名: {old_path} -> {new_path}")
        return True
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return False

if __name__ == "__main__":
    f = FileManager()
    print(f.FileList)