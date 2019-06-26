from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import elfparser
import table
import os


class main_windows(QtWidgets.QWidget):

    def __init__(self, w, h, parent=None):
        super().__init__()
        self.create_layout(w, h)
        self.but_open.clicked.connect(self.openfile)
        self.but_analysis.clicked.connect(self.analysis)
        self.but_exit.clicked.connect(self.exit_)
        self.but_run.clicked.connect(self.run)
        self.but_raw_edit.clicked.connect(self.rawmodify)
        self.combobox_sh.activated.connect(self.shcomboboxChange)
        self.combobox_ph.activated.connect(self.phcomboboxChange)
        self.table_fh.itemSelectionChanged.connect(self.fhitemselect)
        self.table_sh.itemSelectionChanged.connect(self.shitemselect)
        self.table_ph.itemSelectionChanged.connect(self.phitemselect)
        self.pervious_focus_section_base = 0  # for combobox (table_hex)
        self.pervious_focus_section_size = 0  # for combobox (table_hex)
        self.pervious_focus_fht_base = 0  # for fh table (table_hex)
        self.pervious_focus_fht_size = 0  # for fh table (table_hex)
        self.pervious_focus_fht_entity = 0  # for fh table (table_fh)
        self.pervious_focus_section_entity = 0  # for combobox (table_sh)
        self.pervious_focus_program_entity = 0  # for combobox (table_ph)

        self.pervious_focus_sh_base = 0  # for table_sh->table_hex
        self.pervious_focus_sh_size = 0  # for table_sh->table_hex

        self.pervious_focus_ph_base = 0  # for table_ph->table_hex
        self.pervious_focus_ph_size = 0  # for table_ph->table_hex

    def do_clear(self):
        self.combobox_ph.clear()
        self.combobox_sh.clear()
        self.table_hex.clearSelection()
        self.table_ph.clearSelection()
        self.table_sh.clearSelection()
        self.table_fh.clearSelection()
        t_rc = self.table_hex.rowCount()
        for r in range(t_rc-1):
            self.table_hex.removeRow(0)
        ph_rc = self.table_ph.rowCount()
        for r in range(ph_rc):
            self.table_ph.removeRow(0)
        sh_rc = self.table_sh.rowCount()
        for r in range(sh_rc):
            self.table_sh.removeRow(0)
        self.table_fh.clear()
        self.table_fh.setVerticalHeaderLabels(table.fileheader_name_list)
        self.table_fh.setHorizontalHeaderLabels(['Purpos', 'Value', 'Value2'])
        for i in range(17):
            t = QtWidgets.QTableWidgetItem(table.pupros_list[i])
            t.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.table_fh.setItem(i, 0, t)
        self.table_hex.setHorizontalHeaderLabels(["00", "01", "02", "03", "04",
                                                  "05", "06", "07",  "08", "09", "0A", "0B",
                                                  "0C", "0D", "0E", "0F", "ASCII Code"])
        self.table_hex.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.table_hex.resizeColumnsToContents()
        self.table_hex.setVerticalHeaderLabels(["00000000"])
        self.table_ph.setHorizontalHeaderLabels(table.programheader_name_list)
        self.table_ph.setVerticalHeaderLabels(["1"])
        self.table_sh.setHorizontalHeaderLabels(table.sectionheader_name_list)
        self.table_sh.setVerticalHeaderLabels(["1"])

    def do_update_hextable(self, focus_base, focus_size, Rcolor=0, Gcolor=0, Bcolor=0, bRcolor=150, bGcolor=150, bBcolor=150):
        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(Rcolor, Gcolor, Bcolor))
        for idx in range(focus_base, focus_base+focus_size):
            item = self.table_hex.item(int(idx/16), idx % 16)
            try:
                item.setForeground(brush)
                if Rcolor != 0 or Gcolor != 0 or Bcolor != 0:
                    item.setBackground(QtGui.QColor(bRcolor, bGcolor, bBcolor))
                else:
                    item.setBackground(QtGui.QColor(255, 255, 255))
            except:
                pass
        self.table_hex.scrollToItem(self.table_hex.item(
            int(focus_base/16), focus_base % 16), 3)

    def do_update_htable_single(self, table, row, column, Rcolor=0, Gcolor=0, Bcolor=0, bRcolor=150, bGcolor=150, bBcolor=150):
        table.setStyleSheet('selection-background-color:rgb('+str(bRcolor)+','+str(bGcolor)+','+str(
            bBcolor)+');''selection-color: rgb('+str(Rcolor)+','+str(Gcolor)+','+str(Bcolor)+');')
        table.scrollToItem(table.item(row, column), 3)

    def do_update_htable(self, table, focus_entity, Rcolor=0, Gcolor=0, Bcolor=0):
        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(Rcolor, Gcolor, Bcolor))
        columncount = table.columnCount()
        for idx in range(columncount):
            try:
                item = table.item(focus_entity, idx)
                item.setForeground(brush)
                if Rcolor != 0 or Gcolor != 0 or Bcolor != 0:
                    item.setBackground(QtGui.QColor(150, 150, 150))
                else:
                    item.setBackground(QtGui.QColor(255, 255, 255))
            except:
                pass
        table.scrollToItem(table.item(focus_entity, 0), 3)

    def do_pop_up(self, message, message_type="Warning"):
        pop_up = QtWidgets.QMessageBox.question(
            self, message_type, message, QtWidgets.QMessageBox.Ok)

    def do_pop_up_confirm(self, message, message_type="Warning"):
        pop_up = QtWidgets.QMessageBox.question(
            self, message_type, message, QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if pop_up == QtWidgets.QMessageBox.Yes:
            return 1
        else:
            return 0

    def do_init_hextable(self, textcontent):
        current_row = 0
        ascii_s = ""
        for idx, byte in enumerate(textcontent):
            if byte >= 32 and byte <= 126:
                ascii_s += chr(byte)
            else:
                ascii_s += "."
            text = QtWidgets.QTableWidgetItem(format(byte, '02x'))
            text.setFlags(QtCore.Qt.ItemIsSelectable |
                          QtCore.Qt.ItemIsEnabled)

            self.table_hex.setItem(current_row, idx % 16, text)
            if (idx+1) % 16 == 0:
                text = QtWidgets.QTableWidgetItem(ascii_s)
                ascii_s = ""
                text.setFlags(QtCore.Qt.ItemIsSelectable |
                              QtCore.Qt.ItemIsEnabled)
                self.table_hex.setItem(current_row, 16, text)
                current_row += 1
                self.table_hex.insertRow(current_row)
                self.table_hex.setVerticalHeaderItem(
                    current_row, QtWidgets.QTableWidgetItem(format(idx+1, '08x')))
        self.table_hex.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.table_hex.resizeColumnsToContents()

    def do_init_shtable(self):
        for r_idx in elfparser.section_header:
            row = self.table_sh.rowCount()
            self.table_sh.insertRow(row)
            for c_idx in range(11):
                item = QtWidgets.QTableWidgetItem(
                    str(elfparser.section_header[r_idx].sh_dict[c_idx]))
                item.setFlags(QtCore.Qt.ItemIsSelectable |
                              QtCore.Qt.ItemIsEnabled)
                self.table_sh.setItem(r_idx, c_idx, item)
        self.table_sh.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.table_sh.resizeColumnsToContents()

    def do_init_phtable(self):
        for r_idx in elfparser.program_header:
            row = self.table_ph.rowCount()
            self.table_ph.insertRow(row)
            for c_idx in range(9):
                item = QtWidgets.QTableWidgetItem(
                    str(elfparser.program_header[r_idx].ph_dict[c_idx]))
                item.setFlags(QtCore.Qt.ItemIsSelectable |
                              QtCore.Qt.ItemIsEnabled)
                self.table_ph.setItem(r_idx, c_idx, item)
        self.table_ph.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.table_ph.resizeColumnsToContents()

    def do_init_fhtable(self):
        for idx in range(17):
            t = QtWidgets.QTableWidgetItem(
                hex(elfparser.file_header.fh_dict[idx]))
            t.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
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
                t = QtWidgets.QTableWidgetItem(
                    table.EI_OSABI_TABLE[elfparser.file_header.EI_Osabi])
            elif idx == 5:
                t = QtWidgets.QTableWidgetItem(
                    table.e_type_table[elfparser.file_header.e_type])
            elif idx == 6:
                t = QtWidgets.QTableWidgetItem(
                    table.e_machine_table[elfparser.file_header.e_machine])
            if idx == 1 or idx == 2 or idx == 4 or idx == 5 or idx == 6:
                t.setFlags(QtCore.Qt.ItemIsSelectable |
                           QtCore.Qt.ItemIsEnabled)
                self.table_fh.setItem(idx, 2, t)

    def do_init_phmenu(self):
        ph_list = []
        for key in elfparser.program_header:
            ph_list.append(str(key))
        self.combobox_ph.addItems(ph_list)

    def do_init_shmenu(self):
        sh_list = []
        self.sh_name_key = {}
        for key in elfparser.section_header:
            sh_list.append(elfparser.section_header[key].sh_name)
            self.sh_name_key[elfparser.section_header[key].sh_name] = key
        self.combobox_sh.addItems(sh_list)

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

    def do_error_handling(self):
        try:
            self.error_type = elfparser.elf_file_processer(self.elf_file)
        except:
            w = "Not a legal ELF format.UNKNOW REASON"
            self.do_pop_up("Not a legal ELF format.UNKNOW REASON")
            self.ln_status.setText(w)
            self.error_type = -99
            return
        if self.error_type == -1:
            self.do_pop_up("Not a legal ELF format.BAD MAGIC")
            w = "Not a legal ELF format.BAD MAGIC"
            self.ln_status.setText(w)
            return

    def openfile(self):
        if self.do_open_file() == -1:
            return
        self.do_clear()
        self.do_init_hextable(self.elf_file)
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
        self.do_init_fhtable()
        self.do_init_phmenu()
        self.do_init_shmenu()
        self.do_init_phtable()
        self.do_init_shtable()
        self.but_analysis.setEnabled(False)
        self.but_run.setEnabled(True)
        self.but_edit.setEnabled(True)

    def run(self):
        if 'linux' not in sys.platform:
            self.ln_status.setText(
                "Currently only support Linux system. sys.platform return:"+str(sys.platform))
            return
        else:
            return
        os.system('cd / && "."'+self.doc[0]+' > /tmp/tmp.log')
        with open("/tmp/tmp.log", 'r') as file:
            run_dump = file.read()
            self.table_hex.clear()
            self.table_hex.append(run_dump)
        self.ln_status.setText('command : cd / && "."' +
                               self.doc[0]+' > /tmp/tmp.log')

        os.system('rm /tmp/tmp.log')

    def fhitemselect(self):
        try:
            idx = self.table_fh.selectionModel().selectedRows()[0].row()
            #self.do_update_htable(self.table_fh, self.pervious_focus_fht_entity, 0)
            #self.do_update_htable(self.table_fh, idx, 255)
            self.do_update_hextable(
                self.pervious_focus_fht_base, self.pervious_focus_fht_size, 0)
            base_size = elfparser.file_header.fh_basesize_dict[idx]
            self.do_update_hextable(
                base_size[0], base_size[1], 255, 255, 255, 0, 120, 215)
            self.pervious_focus_fht_entity = idx
            self.pervious_focus_fht_base = base_size[0]
            self.pervious_focus_fht_size = base_size[1]
        except:
            pass

    def shitemselect(self):
        try:
            model_index = self.table_sh.selectedIndexes()[0]
            row = model_index.row()
            column = model_index.column()
            self.do_update_htable_single(
                self.table_sh, row, column, 0, 109, 0, 255, 199, 199)
            self.do_update_hextable(
                self.pervious_focus_sh_base, self.pervious_focus_sh_size)
            sh_base_size = elfparser.section_header[row].sh_basesize_dict[column]
            self.do_update_hextable(
                sh_base_size[0], sh_base_size[1], 0, 109, 0, 255, 199, 199)
            self.pervious_focus_sh_base = sh_base_size[0]
            self.pervious_focus_sh_size = sh_base_size[1]
        except:
            pass

    def phitemselect(self):
        try:
            model_index = self.table_ph.selectedIndexes()[0]
            row = model_index.row()
            column = model_index.column()
            self.do_update_htable_single(
                self.table_ph, row, column, 117, 0, 99, 204, 233, 95)
            self.do_update_hextable(
                self.pervious_focus_ph_base, self.pervious_focus_ph_size)
            ph_base_size = elfparser.program_header[row].ph_basesize_dict[column]
            self.do_update_hextable(
                ph_base_size[0], ph_base_size[1], 117, 0, 99, 204, 233, 95)
            self.pervious_focus_ph_base = ph_base_size[0]
            self.pervious_focus_ph_size = ph_base_size[1]
        except:
            pass

    def phcomboboxChange(self):
        chosen_index = self.combobox_ph.currentIndex()
        self.do_update_htable(
            self.table_ph, self.pervious_focus_program_entity, 0)
        self.do_update_htable(self.table_ph, chosen_index, 255)
        self.pervious_focus_program_entity = chosen_index

    def shcomboboxChange(self):
        chosen_idx = self.combobox_sh.currentIndex()
        focus_entity = chosen_idx
        focus_base = elfparser.section_header[chosen_idx].sh_offset
        focus_size = elfparser.section_header[chosen_idx].sh_size
        self.do_update_hextable(self.pervious_focus_section_base,
                                self.pervious_focus_section_size, 0)
        self.do_update_htable(
            self.table_sh, self.pervious_focus_section_entity, 0)
        self.do_update_hextable(focus_base, focus_size, 255)
        self.do_update_htable(self.table_sh, focus_entity, 255)
        self.pervious_focus_section_base = focus_base
        self.pervious_focus_section_size = focus_size
        self.pervious_focus_section_entity = focus_entity

    def do_open_editor(self):
        self.editor_window = Editor(self.elf_file)
        self.editor_window.show()

    def rawmodify(self):
        if self.do_pop_up_confirm("This will corrupted the elf file. Are you sure?") == 0:
            return
        self.do_open_editor()

    def exit_(self):
        exit()

    def create_layout(self, w, h):
        main_layout = QtWidgets.QHBoxLayout()
        left_layout = QtWidgets.QVBoxLayout()
        middle_layout = QtWidgets.QVBoxLayout()
        right_layout = QtWidgets.QVBoxLayout()
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

        self.painter=QtGui.QPainter()
        self.combobox_ph = QtWidgets.QComboBox()
        self.combobox_sh = QtWidgets.QComboBox()
        self.but_open = QtWidgets.QPushButton("Open File")
        self.but_raw_edit = QtWidgets.QPushButton("Direct Modify")
        self.but_edit = QtWidgets.QPushButton("Useless Button")
        self.but_analysis = QtWidgets.QPushButton("Analysis")
        self.but_run = QtWidgets.QPushButton("Run Elf")
        self.but_exit = QtWidgets.QPushButton("Exit")
        self.table_hex = QtWidgets.QTableWidget(1, 17)
        self.table_sh = QtWidgets.QTableWidget(1, 11)
        self.table_ph = QtWidgets.QTableWidget(1, 9)
        self.table_fh = QtWidgets.QTableWidget(17, 3)
        self.ln_status = QtWidgets.QLineEdit(
            "Currently no file opened, open one to proceed.")
        self.lb_bcounter = QtWidgets.QLabel()
        self.lb_sh_title = QtWidgets.QLabel("Section Header Name:")
        self.lb_sht_title = QtWidgets.QLabel("Section Header Table")
        self.lb_ph_title = QtWidgets.QLabel("Program Header Name:")
        self.lb_pht_title = QtWidgets.QLabel("Program Header Table")
        self.ud_linking = QtWidgets.QLabel("Linking Image")
        self.ud_loading = QtWidgets.QLabel("Loading Image")


        lb_layout.addWidget(self.but_open)
        lb_layout.addWidget(self.but_analysis)
        lb_layout.addWidget(self.but_run)
        rb_layout.addWidget(self.but_raw_edit)
        rb_layout.addWidget(self.but_edit)
        rb_layout.addWidget(self.but_exit)
        b_layout.addLayout(lb_layout)
        b_layout.addLayout(rb_layout)
        combobox_ph_layout.addWidget(self.lb_ph_title)
        combobox_ph_layout.addWidget(self.combobox_ph)
        combobox_sh_layout.addWidget(self.lb_sh_title)
        combobox_sh_layout.addWidget(self.combobox_sh)

        right_layout.addLayout(b_layout)
        right_layout.addWidget(self.table_fh)
        right_layout.addWidget(self.lb_pht_title)
        right_layout.addWidget(self.table_ph)
        right_layout.addLayout(combobox_ph_layout)
        
        

        middle_layout.addWidget(self.lb_sht_title)
        middle_layout.addWidget(self.table_sh)
        middle_layout.addLayout(combobox_sh_layout)

        left_layout.addWidget(self.lb_bcounter)
        left_layout.addWidget(self.table_hex)
        left_layout.addWidget(self.ln_status)

        main_layout.addLayout(left_layout,7)
        main_layout.addLayout(middle_layout,4)
        main_layout.addLayout(right_layout,3)
        
        self.setLayout(main_layout)
        self.but_analysis.setEnabled(False)
        self.but_raw_edit.setEnabled(False)
        self.but_edit.setEnabled(False)
        self.but_run.setEnabled(False)
        self.ln_status.setReadOnly(True)

        self.table_hex.setFont(f)
        self.lb_pht_title.setFont(f)
        self.lb_sht_title.setFont(f)
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
        self.lb_bcounter.setFont(f)
        f = QtGui.QFont("Monospace")
        f.setStyleHint(QtGui.QFont.TypeWriter)
        f.setPointSize(16)

        self.lb_bcounter.setText("Hex Plan Text")
        f.setBold(True)
        f.setWeight(65)
        self.table_hex.setFont(f)

        self.table_sh.setFont(f)
        self.table_ph.setFont(f)
        self.table_fh.setFont(f)

        self.table_fh.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.table_fh.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        self.table_sh.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        self.table_ph.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        self.do_clear()





















































class Editor(QtWidgets.QWidget):
    def __init__(self, text_data):
        super().__init__()
        self.createlayout()
        self.elf_file = text_data
        self.do_create_temp()
        self.tableinit()
        self.setMinimumSize(QtCore.QSize(720, 640))
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.but_exit.clicked.connect(self.exit_)
        self.but_undo.clicked.connect(self.undo)
        self.but_save.clicked.connect(self.save)
        self.but_insert.clicked.connect(self.insert)
        self.table.itemSelectionChanged.connect(self.itemselect)
        self.table.cellChanged.connect(self.itemmodify)
        self.history = {}
        self.dirty_byte = []
        self.insert_byte = []
        self.row=0
        self.column=0

    def do_create_temp(self):
        self.temp_bytearray = bytearray(self.elf_file)

    def do_update_hextable(self, row, column, Rcolor=0, Gcolor=0, Bcolor=0, bRcolor=150, bGcolor=150, bBcolor=150):
        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(Rcolor, Gcolor, Bcolor))
        item = self.table.item(row, column)
        try:
            item.setForeground(brush)
            if Rcolor != 0 or Gcolor != 0 or Bcolor != 0:
                item.setBackground(QtGui.QColor(bRcolor, bGcolor, bBcolor))
            else:
                item.setBackground(QtGui.QColor(255, 255, 255))
        except:
            pass

    def do_pop_up(self, message, message_type="Warning"):
        pop_up = QtWidgets.QMessageBox.question(
            self, message_type, message, QtWidgets.QMessageBox.Ok)

    def do_pop_up_confirm(self, message, message_type="Warning"):
        pop_up = QtWidgets.QMessageBox.question(
            self, message_type, message, QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if pop_up == QtWidgets.QMessageBox.Yes:
            return 1
        else:
            return 0

    def save(self):
        save_file=QtWidgets.QFileDialog.getSaveFileName()
        if save_file[0]!='':
            with open(save_file[0],mode='wb') as file:
                file.write(self.temp_bytearray)
            file.close()

    def undo(self):
        self.table.blockSignals(True)
        if (self.row, self.column) in self.dirty_byte:
            self.history[(self.row, self.column)].pop()
            self.do_undo()
            self.do_update_temp(1)
            if (self.row,self.column) in self.insert_byte:
                self.do_table_recolor(self.row,self.column,3)
            else:
                self.do_table_recolor(self.row,self.column,0)
            
            if len(self.history[(self.row, self.column)]) == 1:
                self.dirty_byte.remove((self.row, self.column))
                if (self.row,self.column) in self.insert_byte:
                    self.do_table_recolor(self.row,self.column,2)
                else:
                    self.do_table_recolor(self.row,self.column,1)

        elif (self.row, self.column) in self.insert_byte:
            self.undo_insert()
        else:
            self.do_pop_up("No need to undo, byte is clean.")
        self.table.blockSignals(False)

    def itemselect(self):
        model_index = self.table.selectedIndexes()[0]
        self.row = model_index.row()
        self.column = model_index.column()
        try:
            if (self.row, self.column) not in self.history:
                self.history[(self.row, self.column)] = [self.table.itemFromIndex(model_index).text()]
        except:
            pass

    def itemmodify(self):
        self.table.blockSignals(True)
        self.new_hex = self.table.item(self.row, self.column).text()
        if self.do_error_check() == -1:
            self.do_pop_up(self.error_message)
            self.do_undo()
            self.table.blockSignals(False)
            return
        if (self.row, self.column) not in self.dirty_byte:
            self.dirty_byte.append((self.row, self.column))
        self.history[(self.row, self.column)].append(self.new_hex)
        self.do_update_temp()
        if (self.row,self.column) in self.insert_byte:
            self.do_table_recolor(self.row,self.column,3)
        else:
            self.do_table_recolor(self.row,self.column,0)
        self.table.blockSignals(False)

    def insert(self):
        self.table.blockSignals(True)
        self.do_update_temp(2)
        self.tableinit(1)
        self.do_update_history()
        self.do_update_dirty_byte()
        self.do_update_insert_byte()
        self.insert_byte.append((self.row,self.column))
        for key in self.insert_byte:
            self.do_table_recolor(key[0],key[1],2)
        for key in self.dirty_byte:
            self.do_table_recolor(key[0],key[1],0)
            if key in self.insert_byte:
                self.do_table_recolor(key[0],key[1],3)
        self.table.scrollToItem(self.table.item(self.row,self.column),3)
        self.table.blockSignals(False)

    def undo_insert(self):
        self.table.blockSignals(True)
        self.do_update_temp(3)
        self.tableinit(1)
        self.history.pop((self.row,self.column))
        self.do_update_history(-1)
        self.do_update_dirty_byte(-1)
        self.insert_byte.remove((self.row,self.column))
        self.do_update_insert_byte(-1)
        for key in self.insert_byte:
            self.do_table_recolor(key[0],key[1],2)
        for key in self.dirty_byte:
            self.do_table_recolor(key[0],key[1],0)
            if key in self.insert_byte:
                self.do_table_recolor(key[0],key[1],3)
        self.table.scrollToItem(self.table.item(self.row,self.column),3)
        self.table.blockSignals(False)

    def do_update_history(self,shift=1):
        temp_history={}
        self.insert_point=self.row*16+self.column
        for key in self.history:
            org_pos=key[0]*16+key[1]
            if org_pos>= self.insert_point:
                temp_history[org_pos+1*shift]=self.history[key]
            else:
                temp_history[org_pos]=self.history[key]
        self.history={}
        for key in temp_history:
            self.history[(int(key/16),(key%16))]=temp_history[key]
                
    
    def do_update_dirty_byte(self,shift=1):
        for idx,item in enumerate(self.dirty_byte):
            org_pos=item[0]*16+item[1]
            if org_pos>=self.insert_point:
                self.dirty_byte[idx]=(int((org_pos+1*shift)/16),(org_pos+1*shift)%16)

    def do_update_insert_byte(self,shift=1):
        for idx,item in enumerate(self.insert_byte):
            org_pos=item[0]*16+item[1]
            if org_pos>=self.insert_point:
                self.insert_byte[idx]=(int((org_pos+1*shift)/16),(org_pos+1*shift)%16)
    
    def do_undo(self, mode=0):
        if mode == 0:  # error and inplace undo
            self.old_hex = self.history[(self.row, self.column)][-1]
        self.table.setItem(self.row, self.column,
                           QtWidgets.QTableWidgetItem(self.old_hex))

    def do_table_recolor(self, row,column,mode=0):
        if mode == 0:  # modify mode
            self.do_update_hextable(row, column, 255)
        elif mode == 1:  # undo to clear
            self.do_update_hextable(
                row, column, 0, 0, 0, 255, 255, 255)
        elif mode==2: # insert mode
            self.do_update_hextable(row, column, 0,109,0,255,199,199)
        elif mode==3: # insert and modify mode
            self.do_update_hextable(row, column, 255,0,0,255,199,199)
    def do_update_temp(self, mode=0):
        idx=self.row*16+self.column
        if mode == 0:  # inplace modify mode
            self.temp_bytearray[idx] = int(self.new_hex, 16)
        elif mode == 1:  # inplace modify undo
            self.temp_bytearray[idx] = int(self.old_hex, 16)
        elif mode == 2: # insert mode
            self.temp_bytearray.insert(idx,0)
        elif mode==3:
            self.temp_bytearray.pop(idx)

    def do_error_check(self):
        if len(self.new_hex) != 2:
            self.error_message = "Length error, must be 2"
            return -1
        try:
            int(self.new_hex, 16)
        except:
            self.error_message = "Not a Hexadecimal format. Out of range"
            return -1
        return 0

    def exit_(self):
        if self.do_pop_up_confirm("Are you sure to close? Any unsave change will be discarded.") == 1:
            self.close()
        return

    def tableinit(self,mode=0):
        if mode==1:
            t_rc=self.table.rowCount()
            for r in range(t_rc):
                self.table.removeRow(0)
        current_row = 0
        for idx, byte in enumerate(self.temp_bytearray):
            if idx % 16 == 0:
                self.table.insertRow(current_row)
                self.table.setVerticalHeaderItem(
                    current_row, QtWidgets.QTableWidgetItem(format(current_row*16, '08x')))
            byte_text = QtWidgets.QTableWidgetItem(format(byte, '02x'))
            self.table.setItem(current_row, idx % 16, byte_text)
            if (idx+1) % 16 == 0:
                current_row += 1
        self.table.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.table.resizeColumnsToContents()

    def createlayout(self):
        self.table = QtWidgets.QTableWidget(0, 16)
        self.table.setHorizontalHeaderLabels(["00", "01", "02", "03", "04",
                                              "05", "06", "07",  "08", "09", "0A", "0B",
                                              "0C", "0D", "0E", "0F"])
        self.table.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.table.resizeColumnsToContents()
        self.but_save = QtWidgets.QPushButton("Save")
        self.but_undo = QtWidgets.QPushButton("Undo")
        bf = self.but_save.font()
        bf.setPointSize(16)
        self.but_save.setFont(bf)
        self.but_undo.setFont(bf)
        self.but_exit = QtWidgets.QPushButton("Exit")
        self.but_exit.setFont(bf)
        self.but_insert = QtWidgets.QPushButton("Insert 0x00")
        self.but_insert.setFont(bf)
        self.but_layout = QtWidgets.QHBoxLayout()
        self.main_layout = QtWidgets.QVBoxLayout()
        self.but_layout.addWidget(self.but_insert)
        self.but_layout.addWidget(self.but_undo)
        self.but_layout.addWidget(self.but_save)
        self.but_layout.addWidget(self.but_exit)
        self.main_layout.addWidget(self.table)
        self.main_layout.addLayout(self.but_layout)
        self.setLayout(self.main_layout)
        f = QtGui.QFont("Monospace")
        f.setStyleHint(QtGui.QFont.TypeWriter)
        f.setPointSize(16)
        f.setBold(True)
        self.table.setFont(f)
        self.table.setSelectionMode(QtWidgets.QTableView.SingleSelection)
