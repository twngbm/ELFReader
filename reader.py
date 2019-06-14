import sys
objfile = "vuln"


with open(objfile, mode='rb') as file:
    filecontent = file.read()
EI_Magic = [filecontent[0], filecontent[1],
            filecontent[2], filecontent[3]]  # 0x7F,E,L,F
EI_Class = [filecontent[4]]  # 0:invalid class, 1:32-bit, 2:64-bit
EI_Data = [filecontent[5]] # 0:invalid data encoding, 1:Little-endianness, 2:Big-endianness
EI_OSABI=[filecontent[7]] #https://en.wikipedia.org/wiki/Executable_and_Linkable_Format
e_type=[filecontent[16]]
e_machine=[filecontent[18]]
if EI_Class==[1]:
    print("32 bit")
    bit_flag=1
elif EI_Class==[2]:
    print("64 bit")
    bit_flag=2
if EI_Data==[1]:
    print("Little Endianness")
    bit_order=-1
elif EI_Data==[2]:
    print("Big Endianness")
    bit_order=1
base=24
entry_point=[]
program_header_table=[]
section_header_table=[]
for idx in range(base,base+4*bit_flag):
    entry_point.append(filecontent[idx])
entry_point=entry_point[::-1]
print(entry_point)