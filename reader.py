import sys
objfile = "vuln"
global filecontent
global bit_flag
global bit_order


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
def ret_hex_address(base):
    table=[]
    address=0
    for idx in range(base, base+4*bit_flag):
        table.append(filecontent[idx])
    table = table[::bit_order]
    for power in range(4*bit_flag):
        address = address+table.pop()*2**(power*8)
    return address
h_entry_point=ret_hex_address(base)
print(hex(h_entry_point))
base += 4*bit_flag
h_program_header=ret_hex_address(base)
print(hex(h_program_header))
base += 4*bit_flag
h_section_header=ret_hex_address(base)
print(hex(h_section_header))
base += 4*bit_flag

