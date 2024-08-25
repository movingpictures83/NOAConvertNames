import PyPluMA

class NOAConvertNamesPlugin:
    def input(self, infile):
        self.inputfile = open(infile, 'r')
        self.params = dict()
        for line in self.inputfile:
            contents = line.strip().split('\t')
            self.params[contents[0]] = PyPluMA.prefix()+"/"+contents[1]

    def run(self):
        self.noafile = open(self.params["noafile"], 'r')
        self.firstline = self.noafile.readline()
        #while "\"\"" in self.contents:
        #    self.contents.remove("\"\"")
        metabfile = open(self.params["metabfile"], 'r')
        metabfirst = metabfile.readline().strip()
        metabcontents = metabfirst.split(',')
        metabidx = metabcontents.index("CHEM_ID")
        plotidx = metabcontents.index("PLOT_NAME")
        self.metablookup = dict()
        for line in metabfile:
            contents2 = line.strip().split(',')
            self.metablookup["X"+contents2[metabidx]] = contents2[plotidx]
            
        
    def output(self, outfile):
        self.outputfile = open(outfile, 'w')
        self.outputfile.write(self.firstline)
        #self.outputfile.write("name\tplot\n")
        for line in self.noafile:
            contents = line.split('\t')
            entry = contents[0]
            if (entry[0] == 'X'):
                line = line.replace(entry,self.metablookup[entry])
            else:
                line = line.replace(entry,entry[entry.rfind('__')+2:])
            self.outputfile.write(line)
        
