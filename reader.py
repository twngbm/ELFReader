import sys
from table import *
import pandas as pd
import time
objfile = "test.bin"
objfile = "vuln"
global filecontent
global bit_flag
global bit_order
pd.option_context('display.max_rows', None, 'display.max_columns', None)
with open(objfile, mode='rb') as file:
    filecontent = file.read()


def ret_hex_value(base, offset):
    table = []
    address = 0
    for idx in range(base, base+offset):
        table.append(filecontent[idx])
    table = table[::bit_order]
    for power in range(offset):
        address = address+table.pop()*2**(power*8)
    return address


def ret_hex_content(base, offset, filecontent=filecontent):
    hex_list = []
    for idx in range(offset):
        hex_list.append(filecontent[base+idx])
    return hex_list


EI_Magic = [filecontent[0], filecontent[1],
            filecontent[2], filecontent[3]]  # 0x7F,E,L,F
if EI_Magic != [0x7F, 0x45, 0x4C, 0x46]:
    print("Wrong ELF file magic number, abort.")
    print(EI_Magic)
    exit()
else:
    print("Read 0x7F,E,L,F,keep prossing.")
EI_Class = [filecontent[4]]  # 0:invalid class, 1:32-bit, 2:64-bit
# 0:invalid data encoding, 1:Little-endianness, 2:Big-endianness
EI_Data = [filecontent[5]]
# https://en.wikipedia.org/wiki/Executable_and_Linkable_Format
EI_OSABI = [filecontent[7]]
e_type = [filecontent[16]]
e_machine = [filecontent[18]]
if EI_Class == [1]:
    print("File's format:\t\t 32 bit")
    bit_flag = 1
elif EI_Class == [2]:
    print("File's format:\t\t 64 bit")
    bit_flag = 2
if EI_Data == [1]:
    print("Bite order:\t\t Little Endianness")
    bit_order = -1
elif EI_Data == [2]:
    print("Bite order:\t\t Big Endianness")
    bit_order = 1
base = 24
e_entry = ret_hex_value(base, 4*bit_flag)
base += 4*bit_flag
e_phoff = ret_hex_value(base, 4*bit_flag)
base += 4*bit_flag
e_shoff = ret_hex_value(base, 4*bit_flag)
base += 4*bit_flag
e_flags = ret_hex_value(base, 4)
# print(hex(e_flags))
base += 4
e_ehsize = ret_hex_value(base, 2)
base += 2
e_phentsize = ret_hex_value(base, 2)
base += 2
e_phnum = ret_hex_value(base, 2)
base += 2
e_shentsize = ret_hex_value(base, 2)
base += 2
e_shnum = ret_hex_value(base, 2)
base += 2
e_shstrndx = ret_hex_value(base, 2)
base += 2
print("Targer Operating System:", EI_OSABI_TABLE[filecontent[7]])
print("Objfile Type:\t\t", e_type_table[filecontent[16]])
print("Target ISR:\t\t", e_machine_table[filecontent[18]])
print("File Header Size:\t", e_ehsize, "Bytes\n")
print("Program header offset:\t", hex(e_phoff))
print("A Program header size:\t", e_phentsize, "Bytes")
print("Count of Program headers:", e_phnum, "\n")
print("Section header offset:\t", hex(e_shoff))
print("A Section header size:\t", e_shentsize, "Bytes")
print("Count of Section header:", e_shnum)
print("Section index that\ncontains section name:\t", e_shstrndx, end="\n\n")

print("Main Entry point:\t", hex(e_entry))
print("End of file header.")

base = e_phoff
pcount = 0
pandas_phdata = []
print("\n\nProgram header:")
while pcount < e_phnum:
    init_base = base
    p_type = ret_hex_value(base, 4)
    base += 4
    if bit_flag == 2:
        p_flags = ret_hex_value(base, 4)
        base += 4
    p_offset = ret_hex_value(base, 4*bit_flag)
    base += 4*bit_flag
    p_vaddr = ret_hex_value(base, 4*bit_flag)
    base += 4*bit_flag
    p_paddr = ret_hex_value(base, 4*bit_flag)
    base += 4*bit_flag
    p_filesz = ret_hex_value(base, 4*bit_flag)
    base += 4*bit_flag
    p_memsz = ret_hex_value(base, 4*bit_flag)
    base += 4*bit_flag
    if bit_flag == 1:
        p_flags = ret_hex_value(base, 4)
        base += 4
    p_align = ret_hex_value(base, 4*bit_flag)
    try:
        p_type_name = p_type_table[p_type]
        pandas_phdata.append([hex(init_base), p_type_name, hex(p_offset), hex(
            p_vaddr), hex(p_paddr), p_filesz, p_memsz, hex(p_flags), hex(p_align)])
    except:
        pandas_phdata.append([hex(init_base), hex(p_type), hex(p_offset), hex(
            p_vaddr), hex(p_paddr), p_filesz, p_memsz, hex(p_flags), hex(p_align)])
    base += 4*bit_flag
    pcount += 1
phdf = pd.DataFrame(pandas_phdata, columns=["TableAddr", "Type", "Offset", "VirtAddr",
                                     "PhysAddr", "FileSiz(Bytes)", "MemSiz(Bytes)", "Flag", "Align"])
print(phdf)
scount = 0
base = e_shoff
pandas_shdata = []
shdata = []
print("\n\nSection Header")
while scount < e_shnum:
    init_base = base
    sh_name = ret_hex_value(base, 4)
    base += 4
    sh_type = ret_hex_value(base, 4)
    base += 4
    sh_flags = ret_hex_value(base, 4*bit_flag)
    base += 4*bit_flag
    sh_addr = ret_hex_value(base, 4*bit_flag)
    base += 4*bit_flag
    sh_offset = ret_hex_value(base, 4*bit_flag)
    base += 4*bit_flag
    sh_size = ret_hex_value(base, 4*bit_flag)
    base += 4*bit_flag
    sh_link = ret_hex_value(base, 4)
    base += 4
    sh_info = ret_hex_value(base, 4)
    base += 4
    sh_addralign = ret_hex_value(base, 4*bit_flag)
    base += 4*bit_flag
    sh_entize = ret_hex_value(base, 4*bit_flag)
    try:
        sh_type_name = sh_type_table[sh_type]
    except:
        sh_type_name = str(hex(sh_type))
    try:
        sh_flags_name = sh_flags_table[sh_flags]
    except:
        sh_flags_name = str(hex(sh_flags))
    pandas_shdata.append([hex(init_base), hex(sh_name), sh_type_name, hex(sh_addr), hex(
        sh_offset), sh_size, sh_entize, sh_flags_name, sh_link, sh_info, sh_addralign])
    shdata.append([init_base, sh_name, sh_type_name, sh_addr, sh_offset,
                   sh_size, sh_entize, sh_flags_name, sh_link, sh_info, sh_addralign])
    base += 4*bit_flag
    scount += 1


shstrtab_index = e_shstrndx
base = shdata[shstrtab_index][4]
offset = shdata[shstrtab_index][5]
s = ""
count = 0
global section_name
section_name = {}
for idx in range(offset):
    inp = filecontent[base+idx]
    if inp == 0x00:
        s = s[1:]
        section_name[hex(idx-count+1)] = s
        s = ""
        count = 0
    s += str(chr(filecontent[base+idx]))
    count += 1
# print(section_name)
for data in pandas_shdata:
    id = data.pop(1)
    try:
        data.insert(1, section_name[id])
    except:
        data.insert(1, id)
shdf = pd.DataFrame(pandas_shdata, columns=[
                    "TableAddr", "S_Name", "Type", "Addr", "Offset", "Size(Bytes)", "ES(Bytes)", "Flag", "Link", "Info", "Al"])
print(shdf)

while True:
    print("Input index to dump section context, enter -l or --list to list all section name")
    print("Or enter exit to exit.")
    try:
        data = input(":")
    except KeyboardInterrupt:
        break
    if data == "exit":
        print("Exit")
        break
    elif data == "-l" or data == "--list":
        print(shdf)
        continue
    try:
        data = shdata[int(data)]
    except:
        print("Input Error.Retry")
        continue
    try:
        print("Section Name:\t", section_name[hex(data[1])])
    except:
        print("Section Name:\t", hex(data[1]))

    print("Section Offset:\t", hex(data[4]))
    print("Section Size:\t", data[5])
    print("Section Content:")
    print(" Offset(h)  00 01 02 03 04 05 06 07  08 09 0A 0B 0C 0D 0E 0F\n")
    cont = ret_hex_content(data[4], data[5])
    c = 0
    for word in cont:
        if c % 16 == 0:
            print(format(c, '010x'), " ", end="")
        print(format(word, '02x'), end=" ")
        if (c+1) % 8 == 0:
            print(" ", end="")
        if (c+1) % 16 == 0:
            print("")
        c += 1
    print("\n")

