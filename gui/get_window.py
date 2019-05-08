from __future__ import print_function
from ctypes import *

psapi = windll.psapi
titles = []


# get window title from pid
def gwtfp():
    max_array = c_ulong * 4096
    pProcessIds = max_array()
    pBytesReturned = c_ulong()

    psapi.EnumProcesses(byref(pProcessIds),
                        sizeof(pProcessIds),
                        byref(pBytesReturned))

    # get the number of returned processes
    nReturned = int(pBytesReturned.value/sizeof(c_ulong()))
    pidProcessArray = [i for i in pProcessIds][:nReturned]
    print(pidProcessArray)
    #
    EnumWindows = windll.user32.EnumWindows
    EnumWindowsProc = WINFUNCTYPE(c_bool, POINTER(c_int), POINTER(c_int))
    GetWindowText = windll.user32.GetWindowTextW
    GetWindowTextLength = windll.user32.GetWindowTextLengthW
    IsWindowVisible = windll.user32.IsWindowVisible


    for process in pidProcessArray:
        # print("Process PID %d" % process)
        if True:#IsWindowVisible(process):
            length = GetWindowTextLength(process)
            print(GetWindowText(process))
            buff = create_unicode_buffer(length + 10)
            GetWindowText(process, buff, length + 10)
            titles.append(buff.value)


gwtfp()
print(titles)

