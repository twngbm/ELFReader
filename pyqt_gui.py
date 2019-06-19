from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import elfparser
import table


class main_windows(QtWidgets.QWidget):

    def __init__(self, w, h, parent=None):
        super().__init__()
        self.create_layout(w, h)
        self.but_open.clicked.connect(self.open_file)
        self.but_analysis.clicked.connect(self.analysis)
        self.but_exit.clicked.connect(self.exit_)

    def do_clear(self):
        self.combobox_ph.clear()
        self.combobox_sh.clear()
        self.text_hex.clear()
        self.text_ph.clear()
        self.table_fh.clear()
        self.table_fh.setVerticalHeaderLabels(table.name_list)
        self.table_fh.setHorizontalHeaderLabels(['Purpos', 'Value', 'Value2'])
        for i in range(17):
            t = QtWidgets.QTableWidgetItem(table.pupros_list[i])
            self.table_fh.setItem(i, 0, t)
        self.text_sh.clear()

    def draw_all_header(self):
        self.text_ph.append("Program Header:")
        self.text_ph.append(
            "#        p_type  offset   vaddr    paddr\tfilesz\tmensz\tflags \talign")
        s = ""
        for key in elfparser.program_header:
            s += format(key,'02')+" "+\
                format(elfparser.program_header[key].p_type,' >12')+"  "+\
                format(elfparser.program_header[key].p_offset,"08x")+" "+\
                format(elfparser.program_header[key].p_vaddr,"08x")+" "+\
                format(elfparser.program_header[key].p_paddr,"08x")+" \t"+\
                str(elfparser.program_header[key].p_filesz)+" \t"+\
                str(elfparser.program_header[key].p_memsz)+" \t"+\
                str(elfparser.program_header[key].p_flags)+" \t"+\
                str(elfparser.program_header[key].p_align)
            self.text_ph.append(s)
            s=""
        self.text_ph.append("\nSection Header:")
        self.text_ph.append("#        sh_name  sh_type      sh_addr sh_offset sh_size sh_entsize sh_flags sh_link")

    def open_file(self):

        doc = QtWidgets.QFileDialog.getOpenFileName()
        self.setWindowTitle(str(doc[0]))
        try:
            with open(doc[0], mode='rb') as file:
                self.elf_file = file.read()
        except:
            self.ln_status.setText("File unable to open.")
        finally:
            file.close()
        self.do_clear()
        self.but_raw_edit.setEnabled(True)
        self.but_analysis.setEnabled(True)
        text = "From file "+str(doc[0])+", read " + \
            str(len(self.elf_file))+" Bytes"
        self.ln_status.setText(text)
        line = ""
        asc = ""
        text = ""
        counter = 0
        for byte in self.elf_file:
            if counter % 16 == 0 and counter != 0:
                text += format(counter-16, "08x")+"  "+line+" "+asc+"\n"
                asc = ""
                line = ""
            elif counter % 8 == 0 and counter != 0:
                line += " "
            if byte >= 32 and byte <= 126:
                asc += str(chr(byte))
            else:
                asc += "."
            line += (format(byte, "02x")+" ")
            counter += 1
        self.text_hex.append(text)
        self.text_hex.setReadOnly(True)

    def analysis(self):
        self.but_analysis.setEnabled(False)
        try:
            error_type = elfparser.elf_file_processer(self.elf_file)
        except:
            w = "Not a legal ELF format.UNKNOW REASON"
            self.ln_status.setText(w)
            return
        if error_type == -1:
            w = "Not a legal ELF format.BAD MAGIC"
            self.ln_status.setText(w)
            return
        for idx in range(17):
            t = QtWidgets.QTableWidgetItem(
                hex(elfparser.file_header.d_list[idx]))
            self.table_fh.setItem(idx, 1, t)
            if idx == 1:
                if elfparser.bit_flag == 1:
                    t = QtWidgets.QTableWidgetItem("32 Bit")
                    self.table_fh.setItem(idx, 2, t)
                elif elfparser.bit_flag == 2:
                    t = QtWidgets.QTableWidgetItem("64 Bit")
                    self.table_fh.setItem(idx, 2, t)
                else:
                    t = QtWidgets.QTableWidgetItem("Unknow")
                    self.table_fh.setItem(idx, 2, t)
            elif idx == 2:
                if elfparser.bit_order == 1:
                    t = QtWidgets.QTableWidgetItem("Big Endianness")
                    self.table_fh.setItem(idx, 2, t)
                elif elfparser.bit_order == -1:
                    t = QtWidgets.QTableWidgetItem("Little Endianness")
                    self.table_fh.setItem(idx, 2, t)
                else:
                    t = QtWidgets.QTableWidgetItem("Unknow")
                    self.table_fh.setItem(idx, 2, t)
            elif idx == 4:
                self.table_fh.setItem(idx, 2, QtWidgets.QTableWidgetItem(
                    table.EI_OSABI_TABLE[elfparser.file_header.EI_Osabi]))
            elif idx == 5:
                self.table_fh.setItem(idx, 2, QtWidgets.QTableWidgetItem(
                    table.e_type_table[elfparser.file_header.e_type]))
            elif idx == 6:
                self.table_fh.setItem(idx, 2, QtWidgets.QTableWidgetItem(
                    table.e_machine_table[elfparser.file_header.e_machine]))
        ph_list = ["()", "Header Info"]
        for key in elfparser.program_header:
            ph_list.append(str(key))
        sh_list = ["()", "Header Info"]
        self.sh_name_key = {}
        for key in elfparser.section_header:
            sh_list.append(elfparser.section_header[key].sh_name)
            self.sh_name_key[elfparser.section_header[key].sh_name] = key

        self.combobox_ph.addItems(ph_list)
        self.combobox_sh.addItems(sh_list)
        self.draw_all_header()

    def exit_(self):
        exit()

    def create_layout(self, w, h):
        main_layout = QtWidgets.QVBoxLayout()
        bottom_layout = QtWidgets.QHBoxLayout()
        info_layout = QtWidgets.QVBoxLayout()
        text_layout = QtWidgets.QHBoxLayout()
        combobox_ph_layout = QtWidgets.QHBoxLayout()
        combobox_sh_layout = QtWidgets.QHBoxLayout()
        lb_layout = QtWidgets.QVBoxLayout()
        rb_layout = QtWidgets.QVBoxLayout()
        b_layout = QtWidgets.QHBoxLayout()
        img_layout = QtWidgets.QVBoxLayout()
        destex_layout=QtWidgets.QVBoxLayout()
        hextext_layout = QtWidgets.QVBoxLayout()
        self.null = QtWidgets.QPushButton()
        f = self.null.font()
        f.setPointSize(16)

        self.combobox_ph = QtWidgets.QComboBox()
        self.combobox_sh = QtWidgets.QComboBox()
        self.but_open = QtWidgets.QPushButton("Open File")
        self.but_raw_edit = QtWidgets.QPushButton("Direct Modify")
        self.but_edit = QtWidgets.QPushButton("ELF Modify")
        self.but_analysis = QtWidgets.QPushButton("Analysis")
        self.but_run = QtWidgets.QPushButton("Run Elf")
        self.but_exit = QtWidgets.QPushButton("Exit")
        self.text_hex = QtWidgets.QTextEdit()
        self.text_sh = QtWidgets.QTableWidget(1,8)
        self.text_ph = QtWidgets.QTableWidget(1,11)
        self.table_fh = QtWidgets.QTableWidget(17, 3)
        self.table_fh.setVerticalHeaderLabels(table.name_list)
        self.table_fh.setHorizontalHeaderLabels(['Purpos', 'Value', 'Value2'])
        for i in range(17):
            t = QtWidgets.QTableWidgetItem(table.pupros_list[i])
            self.table_fh.setItem(i, 0, t)
        self.ln_status = QtWidgets.QLineEdit(
            "Currently no file opened, open one to proceed.")
        self.lb_bcounter = QtWidgets.QLabel()
        self.lb_sh_title = QtWidgets.QLabel("Section Header Name:")
        self.lb_ph_title = QtWidgets.QLabel("Program Header Name:")
        self.ud_linking = QtWidgets.QLabel("Linking Image")
        self.ud_loading = QtWidgets.QLabel("Loading Image")

        info_layout.addWidget(self.text_ph)
        
        combobox_ph_layout.addWidget(self.lb_ph_title)
        combobox_ph_layout.addWidget(self.combobox_ph)

        combobox_sh_layout.addWidget(self.lb_sh_title)
        combobox_sh_layout.addWidget(self.combobox_sh)
        destex_layout.addWidget(self.text_sh)
        destex_layout.addLayout(combobox_sh_layout)
        info_layout.addLayout(combobox_ph_layout)
        hextext_layout.addWidget(self.lb_bcounter)
        hextext_layout.addWidget(self.text_hex)
        text_layout.addLayout(hextext_layout, 3)
        text_layout.addLayout(destex_layout, 2)
        text_layout.addLayout(info_layout, 2)

        lb_layout.addWidget(self.but_open)
        lb_layout.addWidget(self.but_analysis)
        lb_layout.addWidget(self.but_run)
        rb_layout.addWidget(self.but_raw_edit)
        rb_layout.addWidget(self.but_edit)
        rb_layout.addWidget(self.but_exit)
        b_layout.addLayout(lb_layout)
        b_layout.addLayout(rb_layout)
        img_layout.addWidget(self.ln_status)
        img_layout.addWidget(self.ud_linking)
        img_layout.addWidget(self.ud_loading)
        bottom_layout.addLayout(img_layout, 3)
        bottom_layout.addWidget(self.table_fh, 2)
        bottom_layout.addLayout(b_layout, 1)
        main_layout.addLayout(text_layout, 3)
        main_layout.addLayout(bottom_layout, 2)
        self.setLayout(main_layout)
        self.but_analysis.setEnabled(False)
        self.but_raw_edit.setEnabled(False)
        self.but_edit.setEnabled(False)
        self.but_run.setEnabled(False)
        self.ln_status.setReadOnly(True)
        
        self.text_hex.setFont(f)
        self.table_fh.setFont(f)
        
        self.ln_status.setFont(f)
        self.but_analysis.setFont(f)
        self.but_edit.setFont(f)
        self.but_raw_edit.setFont(f)
        self.but_run.setFont(f)
        self.but_open.setFont(f)
        self.but_exit.setFont(f)
        self.combobox_ph.setFont(f)
        self.combobox_sh.setFont(f)
        self.lb_ph_title.setFont(f)
        self.lb_sh_title.setFont(f)
        f = QtGui.QFont("Monospace")
        f.setStyleHint(QtGui.QFont.TypeWriter)
        f.setPointSize(13)
        self.lb_bcounter.setFont(f)
        self.lb_bcounter.setText(
            "addr(HEX) 00 01 02 03 04 05 06 07  08 09 0A 0B 0C 0D 0E 0F                    ")
        self.text_sh.setFont(f)
        self.text_ph.setFont(f)
        self.text_hex.setCurrentFont(f)
        
        
