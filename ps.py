#!/usr/bin/python3

import ctypes, ctypes.wintypes
import time
import os

OpenProcess = ctypes.windll.kernel32.OpenProcess
OpenProcess.restype = ctypes.wintypes.BOOL
EnumProcess = ctypes.windll.psapi.EnumProcesses
EnumProcess.restype = ctypes.wintypes.BOOL
EnumProcessModules = ctypes.windll.psapi.EnumProcessModules
EnumProcessModules.restype = ctypes.wintypes.BOOL
GetModuleBaseName = ctypes.windll.psapi.GetModuleBaseNameA
GetModuleBaseName.restype = ctypes.wintypes.BOOL

print(os.getlogin(), os.getppid())
arr = 1024
print("")
while True:
	pidProcess = (ctypes.wintypes.DWORD*arr)()
	bytesReturned = ctypes.wintypes.DWORD()
	print("Enumerating All Processes...\n")
	time.sleep(1)

	if EnumProcess(ctypes.byref(pidProcess), ctypes.sizeof(pidProcess), ctypes.byref(bytesReturned)):
		if bytesReturned.value<ctypes.sizeof(pidProcess):
			print("Enumerate Done!\n")
			print("List of Active Processes\n")
			time.sleep(2)
			break
		else:
			print("Increasing the Array...\n")
			arr *= 2
			print("Done!\n")

	else:
		print("Enumerate Processes Failed\n")
		break

suc = 0
fail = 0

for i in range(bytesReturned.value // ctypes.sizeof(ctypes.wintypes.DWORD)):
	if pidProcess[i]:
		PROCESS_QUERY_INFORMATION = 0x0400
		PROCESS_VM_READ = 0x0010
		hProcess = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, pidProcess[i])
		if hProcess != None:
			hmodule = ctypes.wintypes.HMODULE()
			bytesRequired = ctypes.wintypes.DWORD()

			if EnumProcessModules(hProcess, ctypes.byref(hmodule), ctypes.sizeof(hmodule), ctypes.byref(bytesRequired)):

				ProcessesName = (ctypes.c_buffer(30))
				if GetModuleBaseName(hProcess, hmodule, ctypes.byref(ProcessesName), ctypes.sizeof(ProcessesName)):
					suc += 1

					Name = ProcessesName.value
					if os.getppid() == pidProcess[i]:
						print("================== Where the Code Executed")
						print("{0}. {1} = PID {2}".format(suc, Name.decode("utf-8"), pidProcess[i]))
						print("==================")
					else:
						print("{0}. {1} = PID {2}".format(suc, Name.decode("utf-8"), pidProcess[i]))
						time.sleep(0.1)

					ctypes.windll.kernel32.CloseHandle(hmodule)
				else:
					print("Last Error: {0}".format(ctypes.GetLastError()))
					ctypes.windll.kernel32.CloseHandle(hmodule)
			else:
				print("Last Error: {0}".format(ctypes.GetLastError()))
				fail += 1

#print("----------\nSuccess = {0} \nFailed = {1}".format(suc, fail))
