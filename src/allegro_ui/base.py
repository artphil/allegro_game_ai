import platform

if platform.system() == "Windows":
	_OS = 'WIN'
	BAR = '\\'

elif platform.system() == "Darwin":
	_OS = 'MAC'
	BAR = '/'
else:
	_OS = 'LINUX'
	BAR = '/'