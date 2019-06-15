import sys
objfile = "vuln"
global filecontent
global bit_flag
global bit_order
def ret_hex_content(base,offset):
    table=[]
    address=0
    for idx in range(base, base+offset):
        table.append(filecontent[idx])
    table = table[::bit_order]
    for power in range(offset):
        address = address+table.pop()*2**(power*8)
    return address

with open(objfile, mode='rb') as file:
    filecontent = file.read()
EI_Magic = [filecontent[0], filecontent[1],
            filecontent[2], filecontent[3]]  # 0x7F,E,L,F
EI_Class = [filecontent[4]]  # 0:invalid class, 1:32-bit, 2:64-bit
# 0:invalid data encoding, 1:Little-endianness, 2:Big-endianness
EI_Data = [filecontent[5]]
# https://en.wikipedia.org/wiki/Executable_and_Linkable_Format
EI_OSABI = [filecontent[7]]
e_type = [filecontent[16]]
e_machine = [filecontent[18]]
if EI_Class == [1]:
    print("32 bit")
    bit_flag = 1
elif EI_Class == [2]:
    print("64 bit")
    bit_flag = 2
if EI_Data == [1]:
    print("Little Endianness")
    bit_order = -1
elif EI_Data == [2]:
    print("Big Endianness")
    bit_order = 1
base = 24
e_entry=ret_hex_content(base,4*bit_flag)
print(hex(e_entry))
base += 4*bit_flag
e_phoff=ret_hex_content(base,4*bit_flag)
print(hex(e_phoff))
base += 4*bit_flag
e_shoff=ret_hex_content(base,4*bit_flag)
print(hex(e_shoff))
base += 4*bit_flag
e_flags=ret_hex_content(base,4)
print(hex(e_flags))
base+=4
e_ehize=ret_hex_content(base,2)
base+=2
e_phentsize=ret_hex_content(base,2)
base+=2
