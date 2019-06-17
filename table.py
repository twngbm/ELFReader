EI_OSABI_TABLE = {
    0x00:   "System V , usually means this ELF file doesn't use any OS specific extension",
    0x01:	"HP-UX",
    0x02:	"NetBSD",
    0x03:	"Linux",
    0x04:	"GNU Hurd",
    0x06:	"Solaris",
    0x07:	"AIX",
    0x08:	"IRIX",
    0x09:	"FreeBSD",
    0x0A:	"Tru64",
    0x0B:	"Novell Modesto",
    0x0C:	"OpenBSD",
    0x0D:	"OpenVMS",
    0x0E:	"NonStop Kernel",
    0x0F:	"AROS",
    0x10:	"Fenix OS",
    0x11:	"CloudABI"
}

e_type_table = {
    0x00:	"NONE",
    0x01:	"REL",
    0x02:	"EXEC",
    0x03:	"DYN",
    0x04:	"CORE",
    0xfe00:	"LOOS",
    0xfeff:	"HIOS",
    0xff00:	"LOPROC",
    0xffff:	"HIPROC"
}

e_machine_table = {
    0x00:	"No specific instruction set",
    0x02:	"SPARC",
    0x03:	"x86",
    0x08:	"MIPS",
    0x14:	"PowerPC",
    0x16:	"S390",
    0x28:	"ARM",
    0x2A:	"SuperH",
    0x32:	"IA-64",
    0x3E:	"x86-64",
    0xB7:	"AArch64",
    0xF3:	"RISC-V"
}

p_type_table = {
    0x00000000:	"NULL",
    0x00000001:	"LOAD",
    0x00000002:	"DYNAMIC",
    0x00000003:	"INTERP",
    0x00000004:	"NOTE",
    0x00000005:	"SHLIB",
    0x00000006:	"PHDR",
    0x60000000:	"LOOS",
    0x6FFFFFFF:	"HIOS",
    0x70000000:	"LOPROC",
    0x7FFFFFFF:	"HIPROC",
    0x6474e550: "GNU_EH_FRAME",
    0x6474e551: "GNU_STACK",
    0x6474e552: "GNU_RELRO"
}

sh_type_table = {
    0x0:	"NULL",
    0x1:	"PROGBITS",
    0x2:	"SYMTAB",
    0x3:	"STRTAB",
    0x4:	"RELA",
    0x5:	"HASH",
    0x6:	"DYNAMIC",
    0x7:	"NOTE",
    0x8:	"NOBITS",
    0x9:	"REL",
    0x0A:	"SHLIB",
    0x0B:	"DYNSYM",
    0x0E:	"INIT_ARRAY",
    0x0F:	"FINI_ARRAY",
    0x10:	"PREINIT_ARRAY",
    0x11:	"GROUP",
    0x12:	"SYMTAB_SHNDX",
    0x13:	"NUM",
    0x60000000:	"LOOS",
    0x6fffffff: "HIOS",
    0x6ffffff6: "GNU_HASH",
    0x6ffffffe: "VERNEED"
}

sh_flags_table = {
    0x0:    " ",
    0x1:	"WRITE",
    0x2:	"ALLOC",
    0x3:    "WRITE/ALLOC",
    0x4:	"EXECINSTR",
    0x6:    "ALLOC/EXEC",
    0x10:	"MERGE",
    0x20:	"STRINGS",
    0x30:   "MERGE/STRINGS",
    0x40:	"INFO_LINK",
    0x42:   "ALLOC/INFO",
    0x80:	"LINK_ORDER",
    0x100:	"OS_NONCONFORMING",
    0x200:	"GROUP",
    0x400:	"TLS",
    0x0ff00000:	"MASKOS",
    0xf0000000:	"MASKPROC",
    0x4000000:	"ORDERED",
    0x8000000:	"EXCLUDE"
    

}
