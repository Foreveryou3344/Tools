#!usr/bin/env python
# _*_ coding:utf-8 _*_
import sys
def delete(filepath):
	f = open(filepath, 'a+')
	fnew = open(filepath.split('.')[0]+'_new.txt', 'wb')
	for line in f.readlines():
		data = line.strip()
		if len(data)!=0:
			fnew.write(data)
			fnew.write('\n')
	f.close()
	fnew.close()


if __name__ == '__main__':
	if len(sys.argv) == 1:
		print u'输入文件路径'
	else:
		delete(sys.argv[1])
