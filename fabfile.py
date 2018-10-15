#!usr/bin/env python
# _*_ coding:utf-8 _*_
import os
import re
from datetime import datetime
from fabric.api import *
env.user = 'root'  # 服务器用户
env.sudo_user = 'root'  # sudo权限用户
env.hosts = ['139.180.193.216']  # 服务器ip地址

db_user = 'pythonuser'  # 数据库用户
db_password = 'pythonuser'  # 数据库密码


_TAR_FILE = 'dist.tar.gz'  # 压缩包名称
_REMOTE_TMP_TAR = '/tmp/%s' % _TAR_FILE  # 服务器存放压缩包路径
_REMOTE_BASE_DIR = '/srv'  # 解压地址
RE_FILES = re.compile('\r?\n')


def _current_path():
	return os.path.abspath('.')


def _now():
	return datetime.now().strftime('%y-%m-%d_%H.%M.%S')


def build():
	includes = ['*.py']  # 压缩文件类型
	excludes = ['test', '.*', '*.pyc', '*.pyo']  # 排除文件类型
	local('rm -f disk/%s' % _TAR_FILE)
	with lcd(os.path.join(os.path.abspath('.'), 'www')):  # 压缩文件夹的根目录www
		cmd = ['bsdtar', '--dereference', '-czvf', '../disk/%s' % _TAR_FILE]
		cmd.extend(['--exclude=\'%s\'' % ex for ex in excludes])
		cmd.extend(includes)
		local(' '.join(cmd))


def deploy():
	newdir = 'www-%s' % datetime.now().strftime('%y-%m-%d_%H.%M.%S')
	run('rm -f %s' % _REMOTE_TMP_TAR)
	put('disk/%s' % _TAR_FILE, _REMOTE_TMP_TAR)
	with cd(_REMOTE_BASE_DIR):
		run('mkdir %s' % newdir)
	with cd('%s/%s' % (_REMOTE_BASE_DIR, newdir)):
		run('tar -xzvf %s' % _REMOTE_TMP_TAR)
	with cd(_REMOTE_BASE_DIR):  # 定义软连接，看自己需求
		run('rm -f www')
		run('ln -s %s www' % newdir)
