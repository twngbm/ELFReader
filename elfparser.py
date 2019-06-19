from table import *


def ret_dec_value(base, offset, filecontent):
    table = []
    value = 0
    for idx in range(base, base+offset):
        table.append(filecontent[idx])
    table = table[::bit_order]
    for power in range(offset):
        value = value+table.pop()*2**(power*8)
    return value


def ret_hex_content(base, offset, filecontent):
    hex_list = []
    for idx in range(offset):
        hex_list.append(filecontent[base+idx])
    return hex_list


def elf_file_processer(filecontent):
    global file_header
    global program_header
    global section_header
    global section_name
    global section
    file_header = Elf_file_header(filecontent)
    if hex(file_header.EI_Magic) != "0x7f454c46":
        return -1
    pcount = 0
    program_header = {}
    base = file_header.e_phoff
    while pcount < file_header.e_phnum:
        ph = Elf_program_header(filecontent, base)
        program_header[pcount] = ph
        try:
            program_header[pcount].p_type=p_type_table[program_header[pcount].p_type]
        except:
            pass
        base += file_header.e_phentsize
        pcount += 1
    scount = 0
    section_header = {}
    section = {}
    base = file_header.e_shoff
    while scount < file_header.e_shnum:
        sh = Elf_section_header(filecontent, base)
        s = Elf_section(filecontent, sh)
        section_header[scount] = sh
        section[scount] = s
        base += file_header.e_shentsize
        scount += 1

    shstrtab_index = file_header.e_shstrndx
    shstrtab_base = section_header[shstrtab_index].sh_offset
    shstrtab_size = section_header[shstrtab_index].sh_size
    s = ""
    count = 0

    section_name = {}
    for idx in range(shstrtab_size):
        inp = filecontent[shstrtab_base+idx]
        if inp == 0x00:
            s = s[1:]
            section_name[hex(idx-count+1)] = s
            s = ""
            count = 0
        s += str(chr(filecontent[shstrtab_base+idx]))
        count += 1
    for sh_key in section_header:
        section_offset = section_header[sh_key].sh_name
        try:
            section_header[sh_key].sh_name = section_name[hex(section_offset)]
        except:
            section_header[sh_key].sh_name = hex(section_offset)
        try:
            section_header[sh_key].sh_type = sh_type_table[section_header[sh_key].sh_type]
        except:
            pass
        try:
            section_header[sh_key].sh_flags = sh_flags_table[section_header[sh_key].sh_flags]
        except:
            pass


class Elf_file_header():
    def __init__(self, elf_file):
        global bit_order
        global bit_flag
        bit_order=1
        self.EI_Magic = ret_dec_value(0, 4, elf_file)
        self.EI_Class = ret_dec_value(4, 1, elf_file)
        bit_flag = 1 if self.EI_Class == 1 else 2
        self.EI_Data = ret_dec_value(5, 1, elf_file)
        bit_order = -1 if self.EI_Data == 1 else 1
        self.EI_Version = ret_dec_value(6, 1, elf_file)
        self.EI_Osabi = ret_dec_value(7, 1, elf_file)
        self.e_type = ret_dec_value(16, 2, elf_file)
        self.e_machine = ret_dec_value(18, 2, elf_file)
        base = 24
        self.e_entry = ret_dec_value(base, 4*bit_flag, elf_file)
        base += 4*bit_flag
        self.e_phoff = ret_dec_value(base, 4*bit_flag, elf_file)
        base += 4*bit_flag
        self.e_shoff = ret_dec_value(base, 4*bit_flag, elf_file)
        base += 4*bit_flag
        self.e_flags = ret_dec_value(base, 4, elf_file)
        base += 4
        self.e_ehsize = ret_dec_value(base, 2, elf_file)
        base += 2
        self.e_phentsize = ret_dec_value(base, 2, elf_file)
        base += 2
        self.e_phnum = ret_dec_value(base, 2, elf_file)
        base += 2
        self.e_shentsize = ret_dec_value(base, 2, elf_file)
        base += 2
        self.e_shnum = ret_dec_value(base, 2, elf_file)
        base += 2
        self.e_shstrndx = ret_dec_value(base, 2, elf_file)
        self.d_list = [self.EI_Magic, self.EI_Class,
                       self.EI_Data, self.EI_Version,
                       self.EI_Osabi, self.e_type, self.e_machine, 
                       self.e_entry, self.e_phoff, self.e_shoff, 
                       self.e_flags, self.e_ehsize, self.e_phentsize, 
                       self.e_phnum,self.e_shentsize,self.e_shnum,self.e_shstrndx]



class Elf_program_header():
    def __init__(self, elf_file, base):
        self.init_base = base
        self.p_type = ret_dec_value(base, 4, elf_file)
        base += 4
        if bit_flag == 2:
            self.p_flags = ret_dec_value(base, 4, elf_file)
            base += 4
        self.p_offset = ret_dec_value(base, 4*bit_flag, elf_file)
        base += 4*bit_flag
        self.p_vaddr = ret_dec_value(base, 4*bit_flag, elf_file)
        base += 4*bit_flag
        self.p_paddr = ret_dec_value(base, 4*bit_flag, elf_file)
        base += 4*bit_flag
        self.p_filesz = ret_dec_value(base, 4*bit_flag, elf_file)
        base += 4*bit_flag
        self.p_memsz = ret_dec_value(base, 4*bit_flag, elf_file)
        base += 4*bit_flag
        if bit_flag == 1:
            self.p_flags = ret_dec_value(base, 4, elf_file)
            base += 4
        self.p_align = ret_dec_value(base, 4*bit_flag, elf_file)
        


class Elf_section_header():
    def __init__(self, elf_file, base):
        self.init_base = base
        self.sh_name = ret_dec_value(base, 4, elf_file)
        base += 4
        self.sh_type = ret_dec_value(base, 4, elf_file)
        base += 4
        self.sh_flags = ret_dec_value(base, 4*bit_flag, elf_file)
        base += 4*bit_flag
        self.sh_addr = ret_dec_value(base, 4*bit_flag, elf_file)
        base += 4*bit_flag
        self.sh_offset = ret_dec_value(base, 4*bit_flag, elf_file)
        base += 4*bit_flag
        self.sh_size = ret_dec_value(base, 4*bit_flag, elf_file)
        base += 4*bit_flag
        self.sh_link = ret_dec_value(base, 4, elf_file)
        base += 4
        self.sh_info = ret_dec_value(base, 4, elf_file)
        base += 4
        self.sh_addralign = ret_dec_value(base, 4*bit_flag, elf_file)
        base += 4*bit_flag
        self.sh_entize = ret_dec_value(base, 4*bit_flag, elf_file)


class Elf_section():
    def __init__(self, elf_file, section_header):
        self.offset = section_header.sh_offset
        self.size = section_header.sh_size
        self.section_name = section_header.sh_name
        self.content = ret_hex_content(
            section_header.sh_offset, self.size, elf_file)
