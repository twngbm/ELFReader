from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import elfparser
import table


class main_windows(QtWidgets.QWidget):

    def __init__(self, w, h, parent=None):
        super().__init__()
        self.create_layout(w, h)
        self.but_open.clicked.connect(self.openfile)
        self.but_analysis.clicked.connect(self.analysis)
        self.but_exit.clicked.connect(self.exit_)

    def do_clear(self):
        self.combobox_ph.clear()
        self.combobox_sh.clear()
        self.text_hex.clear()
        self.table_ph.clear()
        self.table_sh.clear()
        self.table_fh.clear()
        self.table_fh.setVerticalHeaderLabels(table.fileheader_name_list)
        self.table_fh.setHorizontalHeaderLabels(['Purpos', 'Value', 'Value2'])
        for i in range(17):
            t = QtWidgets.QTableWidgetItem(table.pupros_list[i])
            t.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            self.table_fh.setItem(i, 0, t)
        self.table_ph.setHorizontalHeaderLabels(table.programheader_name_list)
        self.table_ph.setVerticalHeaderLabels(["0"])
        self.table_sh.setHorizontalHeaderLabels(table.sectionheader_name_list)
        self.table_sh.setVerticalHeaderLabels(["0"])

    def do_set_hextext(self, focus_base=0, fosuc_size=0):
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

    def do_update_shtable(self):
        for r_idx in elfparser.section_header:
            for c_idx in range(11):
                item=QtWidgets.QTableWidgetItem(
                    str(elfparser.section_header[r_idx].sh_dict[c_idx]))
                item.setFlags(QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
                self.table_sh.setItem(r_idx, c_idx, item)
                row = self.table_sh.rowCount()
            self.table_sh.insertRow(row)

    def do_update_phtable(self):
        for r_idx in elfparser.program_header:
            for c_idx in range(9):
                item=QtWidgets.QTableWidgetItem(
                    str(elfparser.program_header[r_idx].ph_dict[c_idx]))
                item.setFlags(QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
                self.table_ph.setItem(r_idx, c_idx, item)
                row = self.table_ph.rowCount()
            self.table_ph.insertRow(row)

    def do_open_file(self):
        self.doc = QtWidgets.QFileDialog.getOpenFileName()
        self.setWindowTitle(str(self.doc[0]))
        try:
            with open(self.doc[0], mode='rb') as file:
                self.elf_file = file.read()
            file.close()
        except:
            self.ln_status.setText("File unable to open.")
            return -1
            
    def do_update_phmenu(self):
        self.ph_list = ["()"]
        for key in elfparser.program_header:
            self.ph_list.append(str(key))
        self.combobox_ph.addItems(self.ph_list)

    def do_update_shmenu(self):
        sh_list = ["()"]
        self.sh_name_key = {}
        for key in elfparser.section_header:
            sh_list.append(elfparser.section_header[key].sh_name)
            self.sh_name_key[elfparser.section_header[key].sh_name] = key
        self.combobox_sh.addItems(sh_list)

    def do_update_fhtable(self):
        for idx in range(17):
            t = QtWidgets.QTableWidgetItem(
                hex(elfparser.file_header.fh_dict[idx]))
            t.setFlags(QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            self.table_fh.setItem(idx, 1, t)
            if idx == 1:
                if elfparser.bit_flag == 1:
                    t = QtWidgets.QTableWidgetItem("32 Bit")
                    
                elif elfparser.bit_flag == 2:
                    t = QtWidgets.QTableWidgetItem("64 Bit")
                    
                else:
                    t = QtWidgets.QTableWidgetItem("Unknow")
                    
            elif idx == 2:
                if elfparser.bit_order == 1:
                    t = QtWidgets.QTableWidgetItem("Big Endianness")
                    
                elif elfparser.bit_order == -1:
                    t = QtWidgets.QTableWidgetItem("Little Endianness")
                    
                else:
                    t = QtWidgets.QTableWidgetItem("Unknow")
                    
            elif idx == 4:
                t=QtWidgets.QTableWidgetItem(
                    table.EI_OSABI_TABLE[elfparser.file_header.EI_Osabi])
            elif idx == 5:
                t=QtWidgets.QTableWidgetItem(
                    table.e_type_table[elfparser.file_header.e_type])
            elif idx == 6:
                t=QtWidgets.QTableWidgetItem(
                    table.e_machine_table[elfparser.file_header.e_machine])
            t.setFlags(QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            self.table_fh.setItem(idx, 2, t)
    def do_error_handling(self):
        try:
            self.error_type = elfparser.elf_file_processer(self.elf_file)
        except:
            w = "Not a legal ELF format.UNKNOW REASON"
            self.ln_status.setText(w)
            self.error_type = -99
            return
        if self.error_type == -1:
            w = "Not a legal ELF format.BAD MAGIC"
            self.ln_status.setText(w)
            return

    def openfile(self):

        if self.do_open_file()==-1:
            return
        self.do_clear()
        self.do_set_hextext()
        text = "From file "+str(self.doc[0])+", read " + \
            str(len(self.elf_file))+" Bytes"
        self.ln_status.setText(text)
        self.but_raw_edit.setEnabled(True)
        self.but_analysis.setEnabled(True)
        self.but_run.setEnabled(False)
        self.but_edit.setEnabled(False)

    def analysis(self):

        self.do_error_handling()
        if self.error_type != 0:
            return
        self.do_update_fhtable()
        self.do_update_phmenu()
        self.do_update_shmenu()
        self.do_update_phtable()
        self.do_update_shtable()
        self.but_analysis.setEnabled(False)
        self.but_run.setEnabled(True)
        self.but_edit.setEnabled(True)

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
        destex_layout = QtWidgets.QVBoxLayout()
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
        self.table_sh = QtWidgets.QTableWidget(1, 11)
        self.table_ph = QtWidgets.QTableWidget(1, 9)
        self.table_fh = QtWidgets.QTableWidget(17, 3)
        self.ln_status = QtWidgets.QLineEdit(
            "Currently no file opened, open one to proceed.")
        self.lb_bcounter = QtWidgets.QLabel()
        self.lb_sh_title = QtWidgets.QLabel("Section Header Name:")
        self.lb_ph_title = QtWidgets.QLabel("Program Header Name:")
        self.ud_linking = QtWidgets.QLabel("Linking Image")
        self.ud_loading = QtWidgets.QLabel("Loading Image")

        info_layout.addWidget(self.table_ph)
        combobox_ph_layout.addWidget(self.lb_ph_title)
        combobox_ph_layout.addWidget(self.combobox_ph)
        combobox_sh_layout.addWidget(self.lb_sh_title)
        combobox_sh_layout.addWidget(self.combobox_sh)
        destex_layout.addWidget(self.table_sh)
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
        self.table_sh.setFont(f)
        self.table_ph.setFont(f)
        self.table_fh.setFont(f)
        self.text_hex.setCurrentFont(f)
        self.do_clear()
