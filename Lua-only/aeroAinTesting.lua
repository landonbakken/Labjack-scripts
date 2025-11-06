-- LabJack T7 Pro Lua Script to read MUX80 Pin 44 every second

--configure inputs
MB.W(43900, 3, 0)
MB.W(43902, 0, 199)
MB.W(43903, 0, 0)
MB.W(43904, 3, 0)

startAddress = 96 -- AIN48
endAddress = 176 -- AIN88
stepAddress = 2 -- 2 addresses per AIN


currentAddress = startAddress
while true do
  --read address (AIN, Float32)
  local val = MB.R(currentAddress, 3)
  
  --print (maybe)
  if math.floor((currentAddress-96)/2+48) == 48 or math.floor((currentAddress-96)/2+48) == 49 then
    print("Pin", math.floor((currentAddress-96)/2+48),"value:", val)
  end

  -- small pause
  --LJ.IntervalConfig(0, 10)
  --while not LJ.CheckInterval(0) do end
  
  -- increment address
  currentAddress = currentAddress + 2
  if currentAddress > endAddress then
    currentAddress = startAddress
    print()
  end
end
