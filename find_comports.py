from serial.tools.list_ports import comports as list_comports


print([comport.device for comport in list_comports()])