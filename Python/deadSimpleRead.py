from labjack import ljm

#open first labjack
handle = ljm.openS("ANY", "ANY", "ANY")

while True:
    value = ljm.eReadName(handle, "AIN0")

    print(value)