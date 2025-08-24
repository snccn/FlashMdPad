# coding:utf-8
# author: snccn

import configparser
import os

class SingletonMeta(type):
    _instances = {}  # 用于存储类的实例
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        
        return cls._instances[cls]

class config(metaclass=SingletonMeta):
    def __init__(self, cfg_path:str):
        self.file_path = cfg_path
        self.config = configparser.ConfigParser()
        if os.path.exists(self.file_path):
            self.config.read(self.file_path, encoding='utf-8')
        pass

    def set(self, section, key, value):
        """
        设置配置项
        
        :param section: 配置节名
        :param key: 配置项键名
        :param value: 配置项值
        """
        # 如果节不存在则创建
        if not self.config.has_section(section):
            self.config.add_section(section)
        
        # 设置键值对
        self.config.set(section, key, str(value))
    
    def get(self, section, key, fallback=None):
        """
        获取配置项的值
        
        :param section: 配置节名
        :param key: 配置项键名
        :param fallback: 当配置项不存在时的默认返回值
        :return: 配置项的值，不存在时返回fallback
        """
        if not self.config.has_section(section) or not self.config.has_option(section, key):
            return fallback
        
        return self.config.get(section, key)
    
    def get_int(self, section, key, fallback=None):
        """获取整数类型的配置值"""
        try:
            return self.config.getint(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            return fallback
    
    def get_bool(self, section, key, fallback=None):
        """获取布尔类型的配置值"""
        try:
            return self.config.getboolean(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            return fallback
    
    def save(self):
        """保存配置到文件"""
        # 创建父目录（如果不存在）
        dir_path = os.path.dirname(self.file_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        
        # 写入文件
        with open(self.file_path, 'w', encoding='utf-8') as f:
            self.config.write(f)
        return True
    
    def has_section(self, section):
        """检查是否存在指定的配置节"""
        return self.config.has_section(section)
    
    def has_option(self, section, key):
        """检查指定配置节中是否存在指定的配置项"""
        return self.config.has_option(section, key)
    
    def remove_section(self, section):
        """删除指定的配置节"""
        if self.config.has_section(section):
            return self.config.remove_section(section)
        return False
    
    def remove_option(self, section, key):
        """删除指定配置节中的配置项"""
        if self.config.has_section(section) and self.config.has_option(section, key):
            return self.config.remove_option(section, key)
        return False
    def generate_new_config(self):
        
        pass

