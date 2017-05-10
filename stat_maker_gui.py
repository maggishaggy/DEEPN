import osimport reimport sysimport threadimport globimport cPickleimport timeimport jsonimport subprocessimport cStringIO, tracebackfrom datetime import datetimefrom libraries.pyper import *import functions.fileio_gui as fimport functions.structures as strtfrom PyQt4 import QtCore, QtGui, uicapp = QtGui.QApplication(sys.argv)form_class, base_class = uic.loadUiType(os.path.join('ui', 'Stat_Maker.ui'))class MyListWidgetItem(QtGui.QListWidgetItem):    def __init__(self, *args):        super(MyListWidgetItem, self).__init__(*args)        self.data = ''    def GetData(self):        return self.dataclass Stat_Maker_Gui(QtGui.QMainWindow, form_class):    def __init__(self, *args):        super(Stat_Maker_Gui, self).__init__(*args)        self.setupUi(self)        self.connect(self.vec_sel_list, QtCore.SIGNAL("dropped"), self.vec_sel_fileDropped)        self.connect(self.vec_nonsel_list, QtCore.SIGNAL("dropped"), self.vec_nonsel_fileDropped)        self.connect(self.bait1_sel_list, QtCore.SIGNAL("dropped"), self.bait1_sel_fileDropped)        self.connect(self.bait1_nonsel_list, QtCore.SIGNAL("dropped"), self.bait1_nonsel_fileDropped)        self.connect(self.bait2_sel_list, QtCore.SIGNAL("dropped"), self.bait2_sel_fileDropped)        self.connect(self.bait2_nonsel_list, QtCore.SIGNAL("dropped"), self.bait2_nonsel_fileDropped)        self.connect(self.vec_sel_list_2, QtCore.SIGNAL("dropped"), self.vec_sel_fileDropped_2)        self.connect(self.vec_nonsel_list_2, QtCore.SIGNAL("dropped"), self.vec_nonsel_fileDropped_2)        self.connect(self.bait1_sel_list_2, QtCore.SIGNAL("dropped"), self.bait1_sel_fileDropped_2)        self.connect(self.bait1_nonsel_list_2, QtCore.SIGNAL("dropped"), self.bait1_nonsel_fileDropped_2)        self.connect(self.bait2_sel_list_2, QtCore.SIGNAL("dropped"), self.bait2_sel_fileDropped_2)        self.connect(self.bait2_nonsel_list_2, QtCore.SIGNAL("dropped"), self.bait2_nonsel_fileDropped_2)        self.connect(self.vec_sel_list, QtCore.SIGNAL("deleted"), self.file_deleted)        self.connect(self.vec_nonsel_list, QtCore.SIGNAL("deleted"), self.file_deleted)        self.connect(self.bait1_sel_list, QtCore.SIGNAL("deleted"), self.file_deleted)        self.connect(self.bait1_nonsel_list, QtCore.SIGNAL("deleted"), self.file_deleted)        self.connect(self.bait2_sel_list, QtCore.SIGNAL("deleted"), self.file_deleted)        self.connect(self.bait2_nonsel_list, QtCore.SIGNAL("deleted"), self.file_deleted)        self.connect(self.vec_sel_list_2, QtCore.SIGNAL("deleted"), self.file_deleted)        self.connect(self.vec_nonsel_list_2, QtCore.SIGNAL("deleted"), self.file_deleted)        self.connect(self.bait1_sel_list_2, QtCore.SIGNAL("deleted"), self.file_deleted)        self.connect(self.bait1_nonsel_list_2, QtCore.SIGNAL("deleted"), self.file_deleted)        self.connect(self.bait2_sel_list_2, QtCore.SIGNAL("deleted"), self.file_deleted)        self.connect(self.bait2_nonsel_list_2, QtCore.SIGNAL("deleted"), self.file_deleted)        # self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)        # QThread for processes        self.process = None        # self.run_btn.setEnabled(False)        self.set_interaction_state(False)        self.verify_installation_btn.setEnabled(True)        self.data = {}        self.directory = '~/'        self.jags_path = None        self.r_path = None        self.started = 0        self.r = None        self.fileio = f.fileio()        self.stats = {}    def load_test(self):        self.on_verify_installation_btn_clicked()        self.directory = '/Users/piperlab/Documents/Deepn_Test'        self.fileDropped(self.vec_sel_list,                         '/Users/piperlab/Documents/Deepn_Test/gene_count_summary/EXP14_B_Vector_SEL_summary.csv',                         'Vector_Selected_1')        self.fileDropped(self.vec_nonsel_list,                         '/Users/piperlab/Documents/Deepn_Test/gene_count_summary/EXP14_A_Vector_NON_summary.csv',                         'Vector_Non-Selected_1')        self.fileDropped(self.vec_sel_list_2,                         '/Users/piperlab/Documents/Deepn_Test/gene_count_summary/EXP15_B_Vector_SEL_summary.csv',                         'Vector_Selected_2')        self.fileDropped(self.vec_nonsel_list_2,                         '/Users/piperlab/Documents/Deepn_Test/gene_count_summary/EXP15_A_Vector_NON_summary.csv',                         'Vector_Non-Selected_2')        self.fileDropped(self.bait1_sel_list,                         '/Users/piperlab/Documents/Deepn_Test/gene_count_summary/EXP14_E_RhoATN_SEL_summary.csv',                         "Bait1_Selected_1")        self.fileDropped(self.bait1_nonsel_list,                         '/Users/piperlab/Documents/Deepn_Test/gene_count_summary/EXP14_D_RhoATN_NON_summary.csv',                         "Bait1_Non-Selected_1")        self.load_gene_summary_files()        self.on_run_btn_clicked()    def initialize_folders(self, directory):        self.fileio.create_new_folder(directory, "stat_maker_output")    def pair_check(self, list1, list2):        if list1.count() > 0 and list2.count() > 0:            return True        else:            return False    def either_check(self, list1, list2):        if (list1.count() > 0 and list2.count() > 0) or (list1.count() == 0 and list2.count() == 0):            return True        else:            return False    def monitor_files(self):        if self.pair_check(self.vec_sel_list, self.vec_nonsel_list) and \                self.pair_check(self.bait1_sel_list, self.bait1_nonsel_list) and \                self.pair_check(self.vec_sel_list_2, self.vec_nonsel_list_2):            if self.either_check(self.bait2_sel_list, self.bait2_nonsel_list) and \                    self.either_check(self.vec_sel_list_2, self.vec_nonsel_list_2) and \                    self.either_check(self.bait1_sel_list_2, self.bait1_nonsel_list_2) and \                    self.either_check(self.bait2_sel_list_2, self.bait2_nonsel_list_2):                self.run_btn.setEnabled(True)            else:                self.run_btn.setEnabled(False)                # if not self.process == None:                #     try:                #         os.kill(self.process.pid + 1, 0)                #     except OSError:                #         self.statusbar.showMessage("Finished Installation", 8000)                #         self.started = 0                # if not os.path.exists('/usr/local/bin/jags') and self.started == 0:                #     self.process = subprocess.Popen('open statistics/JAGS.pkg', shell=True)                #     self.started = 1                # if not os.path.exists('/usr/local/bin/R') and self.started == 0:                #     self.process = subprocess.Popen('open statistics/R.pkg', shell=True)                #     self.started = 1    @QtCore.pyqtSlot()    def on_verify_installation_btn_clicked(self):        self.fileio.verify_statmaker_installations(self)        self.set_interaction_state(True)        self.run_btn.setEnabled(False)        self.verify_installation_btn.setEnabled(False)        self.verify_installation_btn.setText("Installations are Correct")        self.statusbar.showMessage("R, JAGS, and DEEPN Installations is Correct")    def which(self, program):        try:            cmd = "which " + program            ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)            output = ps.communicate()[0]            if len(output) > 0:                return True        except OSError:            return False        return False    def get_path(self, program):        try:            cmd = "which " + program            ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)            output = ps.communicate()[0]            if len(output) > 0:                return output.rstrip().split()[0]        except OSError:            return None    def file_deleted(self, path):        for key in self.data.keys():            if self.data[key] == path:                self.data.__delitem__(key)    def fileDropped(self, list, url, key):        if os.path.exists(url) and self.check_uniqueness(url):            iconProvider = QtGui.QFileIconProvider()            fileInfo = QtCore.QFileInfo(url)            icon = iconProvider.icon(fileInfo)            item = MyListWidgetItem()            item.data = url            item.setIcon(icon)            item.setText(os.path.basename(os.path.normpath(url)))            list.clear()            list.addItem(item)            self.data[key] = url        self.monitor_files()    def check_uniqueness(self, path):        for url in self.data.values():            if path == url:                return False        return True    @QtCore.pyqtSlot()    def on_quit_btn_clicked(self):        app.quit()        sys.exit()    @QtCore.pyqtSlot()    def on_folder_choice_btn_clicked(self):        directory = str(QtGui.QFileDialog.getExistingDirectory(QtGui.QFileDialog(), "Locate Work Folder",                                                               os.path.expanduser("~"),                                                               QtGui.QFileDialog.ShowDirsOnly))        self.directory = directory        self.load_gene_summary_files()        sys.excepthook = self.excepthook    def excepthook(self, excType, excValue, tracebackobj):        """        Global function to catch unhandled exceptions.        @param excType exception type        @param excValue exception value        @param tracebackobj traceback object        """        separator = '-' * 80        logFile = self.directory + "/gene_count_error.log"        timeString = time.strftime("%Y-%m-%d, %H:%M:%S")        tbinfofile = cStringIO.StringIO()        traceback.print_tb(tracebackobj, None, tbinfofile)        tbinfofile.seek(0)        tbinfo = tbinfofile.read()        errmsg = '%s: \n%s' % (str(excType), str(excValue))        sections = [separator, timeString, separator, errmsg, separator, tbinfo]        msg = '\n'.join(sections)        try:            f = open(logFile, "w")            f.write(msg)            f.close()        except IOError:            pass    def load_gene_summary_files(self):        self.initialize_folders(self.directory)        try:            dirlist = os.listdir(os.path.join(self.directory, 'gene_count_summary'))            self.file_list.clear()            for file in dirlist:                if not re.match('^\.', file) and re.match('.+summary\.csv', file):                    path = os.path.join(self.directory, 'gene_count_summary', file)                    fileInfo = QtCore.QFileInfo(path)                    iconProvider = QtGui.QFileIconProvider()                    icon = iconProvider.icon(fileInfo)                    item = MyListWidgetItem()                    item.data = path                    item.setIcon(icon)                    item.setText(file)                    self.file_list.addItem(item)        except OSError:            pass    def vec_sel_fileDropped(self, path):        path = str(path)        if os.path.exists(path):            self.fileDropped(self.vec_sel_list, path, 'Vector_Selected_1')    def vec_nonsel_fileDropped(self, path):        path = str(path)        if os.path.exists(path):            self.fileDropped(self.vec_nonsel_list, path, "Vector_Non-Selected_1")    def bait1_sel_fileDropped(self, path):        path = str(path)        if os.path.exists(path):            self.fileDropped(self.bait1_sel_list, path, "Bait1_Selected_1")    def bait1_nonsel_fileDropped(self, path):        path = str(path)        if os.path.exists(path):            self.fileDropped(self.bait1_nonsel_list, path, "Bait1_Non-Selected_1")    def bait2_sel_fileDropped(self, path):        path = str(path)        if os.path.exists(path):            self.fileDropped(self.bait2_sel_list, path, "Bait2_Selected_1")    def bait2_nonsel_fileDropped(self, path):        path = str(path)        if os.path.exists(path):            self.fileDropped(self.bait2_nonsel_list, path, "Bait2_Non-Selected_1")    def vec_sel_fileDropped_2(self, path):        path = str(path)        if os.path.exists(path):            self.fileDropped(self.vec_sel_list_2, path, "Vector_Selected_2")    def vec_nonsel_fileDropped_2(self, path):        path = str(path)        if os.path.exists(path):            self.fileDropped(self.vec_nonsel_list_2, path, "Vector_Non-Selected_2")    def bait1_sel_fileDropped_2(self, path):        path = str(path)        if os.path.exists(path):            self.fileDropped(self.bait1_sel_list_2, path, "Bait1_Selected_2")    def bait1_nonsel_fileDropped_2(self, path):        path = str(path)        if os.path.exists(path):            self.fileDropped(self.bait1_nonsel_list_2, path, "Bait1_Non-Selected_2")    def bait2_sel_fileDropped_2(self, path):        path = str(path)        if os.path.exists(path):            self.fileDropped(self.bait2_sel_list_2, path, "Bait2_Selected_2")    def bait2_nonsel_fileDropped_2(self, path):        path = str(path)        if os.path.exists(path):            self.fileDropped(self.bait2_nonsel_list_2, path, "Bait2_Non-Selected_2")    def write_r_input(self):        output = open(os.path.join(self.directory, 'r_input.params'), 'w')        for key in sorted(self.data.keys()):            # self.write_four_columns_from_csv(self.data[key])            output.write("%-25s = %s\n" % (key, self.data[key]))        output.write("%-25s = %d\n" % ("Threshold", self.threshold_sbx.value()))        # output.write("%-25s = %s\n" % ("R Path", self.r_path))        # output.write("%-25s = %s" % ("JAGS Path", self.jags_path))        output.close()    def set_interaction_state(self, state):        self.run_btn.setEnabled(state)        self.file_list.setEnabled(state)        self.vec_sel_list.setEnabled(state)        self.vec_nonsel_list.setEnabled(state)        self.bait1_sel_list.setEnabled(state)        self.bait1_nonsel_list.setEnabled(state)        self.bait2_sel_list.setEnabled(state)        self.bait2_nonsel_list.setEnabled(state)        self.vec_sel_list_2.setEnabled(state)        self.vec_nonsel_list_2.setEnabled(state)        self.bait1_sel_list_2.setEnabled(state)        self.bait1_nonsel_list_2.setEnabled(state)        self.bait2_sel_list_2.setEnabled(state)        self.bait2_nonsel_list_2.setEnabled(state)        self.folder_choice_btn.setEnabled(state)        self.quit_btn.setEnabled(state)        self.threshold_sbx.setEnabled(state)    def _merge_dicts(*dict_args):        """        Given any number of dicts, shallow copy and merge into a new dict,        precedence goes to key value pairs in latter dicts.        """        result = {}        for dictionary in dict_args:            result.update(dictionary)        return result    def get_junction_stats(self, key, name):        gene_stat = {'frame_orf' : 0,                     'upstream'  : 0,                     'in_orf'    : 0,                     'downstream': 0,                     'in_frame'  : 0,                     'backwards' : 0,                     'intron'    : 0,                     'total'     : 0,                     'junctions' : {}                     }        try:            gene = self.stats[key][name]            for nm in gene.keys():                if nm != 'stats':                    gene_stat['junctions'][nm] = []                    frame = 0                    orf = 0                    for j in gene[nm]:                        if j.orf == 'in_orf' and j.frame == 'in_frame':                            gene_stat['frame_orf'] += j.ppm                        # Check orf                        if j.orf == 'in_orf':                            gene_stat['in_orf'] += j.ppm                            orf = 2                        elif j.orf == 'upstream':                            gene_stat['upstream'] += j.ppm                            orf = 1                        elif j.orf == 'downstream':                            gene_stat['downstream'] += j.ppm                            orf = 3                        # Check frame                        if j.frame == 'in_frame':                            gene_stat['in_frame'] += j.ppm                            frame = 1                        elif j.frame == 'backwards':                            gene_stat['backwards'] += j.ppm                            frame = 2                        elif j.frame == 'intron':                            gene_stat['intron'] += j.ppm                            frame = 3                        gene_stat['total'] += j.ppm                        gene_stat['junctions'][nm].append([j.position,                                                           j.query_start,                                                           j.ppm, frame, orf])        except KeyError:            pass        try:            gene_stat['frame_orf'] = format(gene_stat['frame_orf'] * 100.0 / gene_stat['total'], ".1f")            gene_stat['upstream'] = format(gene_stat['upstream'] * 100.0 / gene_stat['total'], ".1f")            gene_stat['in_orf'] = format(gene_stat['in_orf'] * 100.0 / gene_stat['total'], ".1f")            gene_stat['downstream'] = format(gene_stat['downstream'] * 100.0 / gene_stat['total'], ".1f")            gene_stat['in_frame'] = format(gene_stat['in_frame'] * 100.0 / gene_stat['total'], ".1f")            gene_stat['backwards'] = format(gene_stat['backwards'] * 100.0 / gene_stat['total'], ".1f")            gene_stat['intron'] = format(gene_stat['intron'] * 100.0 / gene_stat['total'], ".1f")        except ZeroDivisionError:            gene_stat['frame_orf'] = '0'            gene_stat['upstream'] = '0'            gene_stat['in_orf'] = '0'            gene_stat['downstream'] = '0'            gene_stat['in_frame'] = '0'            gene_stat['backwards'] = '0'            gene_stat['intron'] = '0'        return gene_stat    def get_vector_gene_stats(self, key):        filehandle = open(self.data[key])        vec_genes = {}        read = False        for line in filehandle.readlines():            if read:                line_split = line.split(",")                gene_name = line_split[1].lstrip().rstrip()                vec_genes[gene_name] = self.get_junction_stats(key, gene_name)                vec_genes[gene_name]['ppm'] = line_split[2].lstrip().rstrip()            if re.match("^Chromosome", line):                read = True        filehandle.close()        return vec_genes    def runr(self):        command = "analyzeDeepn('" + os.path.join(self.directory, 'r_input.params') + "', outfile='" + \                  os.path.join(self.directory, 'stat_maker_output', 'statmaker_output.csv') + "', msgfile='" + \                  os.path.join(self.directory, 'stat_maker_output', 'overdispersion.txt') + "')"        self.r(command)        parameters = []        json_string = {}        json_string['files'] = {}        json_string['files']['selected'] = {}        json_string['files']['non_selected'] = {}        for key in self.data.keys():            filename = os.path.basename(self.data[key].replace("_summary.csv", "") + ".bqp")            self.stats[key] = cPickle.load(open(os.path.join(self.directory, 'blast_results_query', filename), 'rb'))        p = open(os.path.join(self.directory, "r_input.params"))        for line in p:            parameters.append(line.replace("=", ","))            key = line.split()[0]            if key == "Vector_Selected_1":                json_string['files']['selected']['vector1'] = os.path.basename(line.split()[2])            elif key == "Vector_Selected_2":                json_string['files']['selected']['vector2'] = os.path.basename(line.split()[2])            elif key == "Vector_Non-Selected_1":                json_string['files']['non_selected']['vector1'] = os.path.basename(line.split()[2])            elif key == "Vector_Non-Selected_2":                json_string['files']['non_selected']['vector2'] = os.path.basename(line.split()[2])            elif key == "Bait1_Selected_1":                json_string['files']['selected']['bait'] = os.path.basename(line.split()[2])            elif key == "Bait1_Non-Selected_1":                json_string['files']['non_selected']['bait'] = os.path.basename(line.split()[2])            elif key == "Threshold":                json_string['files']['threshold'] = int(line.split()[2])        p.close()        json_vector_genes = {}        json_vector_genes['non_selected'] = {}        json_vector_genes['selected'] = {}        json_vector_genes['non_selected']['vector1'] = self.get_vector_gene_stats('Vector_Non-Selected_1')        json_vector_genes['non_selected']['vector2'] = self.get_vector_gene_stats('Vector_Non-Selected_2')        json_vector_genes['selected']['vector1'] = self.get_vector_gene_stats('Vector_Selected_1')        json_vector_genes['selected']['vector2'] = self.get_vector_gene_stats('Vector_Selected_2')        json_bait_genes = []        overdispersion = []        od_filehandle = open(os.path.join(self.directory, 'stat_maker_output', "overdispersion.txt"))        parameters.append("Overdispersion")        od_keys = ['vector nonsel', 'vector+bait', 'vector sel']        l = 0        for line in od_filehandle.readlines():            if ":" in line:                split = line.strip().split(":")                value = split[1].strip()                parameters.append(",%s,%s" % (od_keys[l], value))                overdispersion.append(float(value))                l += 1        statmaker_filehandle = open(os.path.join(self.directory, 'stat_maker_output', "statmaker_output.csv"))        for line in statmaker_filehandle.readlines():            split = line.rstrip().split(",")            if split[0] == 'Gene':                length = len(split)                for key in sorted(self.data.keys()):                    split.extend([" ", " ", " ", " ", key, " ", " ", " "])                parameters.append(",".join(split))                parameters.append(",".join([" "] * (length + 1) + ["inframe_inorf", "upstream", "in_orf",                                                                   "downstream", "in_frame", "backwards",                                                                   "intron", " "] * len(self.data.keys())))            else:                _temp = []                jbg = {}                jbg['name'] = split[0]                for value in split[1:]:                    if value == 'NA':                        _temp.append(0.0)                    else:                        _temp.append(float(value))                jbg['stats'] = _temp                jbg['selected'] = {}                jbg['non_selected'] = {}                for key in sorted(self.data.keys()):                    gene_stat = self.get_junction_stats(key, split[0])                    stat_string = [" ", gene_stat['frame_orf'], gene_stat['upstream'], gene_stat['in_orf'],                                   gene_stat['downstream'], gene_stat['in_frame'], gene_stat['backwards'],                                   gene_stat['intron']]                    split.extend(stat_string)                    if key == "Bait1_Selected_1":                        jbg['selected']['junction_stats'] = map(float, stat_string[1:])                        jbg['selected']['junctions'] = gene_stat['junctions']                    elif key == "Bait1_Non-Selected_1":                        jbg['non_selected']['junction_stats'] = map(float, stat_string[1:])                        jbg['non_selected']['junctions'] = gene_stat['junctions']                parameters.append(",".join(split))                json_bait_genes.append(jbg)        json_string['genes'] = json_bait_genes        # Get over dispersion from statmaker output.        json_vector_genes['overdispersion'] = overdispersion        statmaker_filehandle.close()        FORMAT = '%d%b%Y-%H%M%S'        name = '%s_%s' % ('stat_maker', datetime.now().strftime(FORMAT))        out = open(os.path.join(self.directory, 'stat_maker_output', name + ".csv"), 'w')        for l in parameters:            out.write(l.replace("NA", "0.0"))            out.write("\n")        out.close()        # writing json file of csv        with open(os.path.join(self.directory, 'stat_maker_output', name + "_baits.json"), 'w') as outfile:            json.dump(json_string, outfile, separators=(',', ':'))        with open(os.path.join(self.directory, 'stat_maker_output', name + "_vectors.json"), 'w') as outfile:            json.dump(json_vector_genes, outfile, separators=(',', ':'))        map(os.remove, glob.glob(os.path.join(self.directory, "r_input.params")))        map(os.remove, glob.glob(os.path.join(self.directory, 'stat_maker_output', "statmaker_output.csv")))        map(os.remove, glob.glob(os.path.join(self.directory, 'stat_maker_output', "overdispersion.txt")))        self.statusbar.showMessage("Saved to File: %s" % os.path.join(self.directory, 'stat_maker_output', name))        self.set_interaction_state(True)    @QtCore.pyqtSlot()    def on_run_btn_clicked(self):        self.statusbar.showMessage("Running DEEPN statistics... Please Wait...")        self.write_r_input()        self.set_interaction_state(False)        thread.start_new_thread(self.runr, ())def appExit():    app.quit()    sys.exit()if __name__ == '__main__':    form = Stat_Maker_Gui()    form.show()    app.aboutToQuit.connect(appExit)    app.exec_()