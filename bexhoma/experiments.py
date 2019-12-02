from os import makedirs, path
import ast
from bexhoma import masterAWS, masterK8s

class workflow():
    def __init__(self, clusterconfig='', resultfolder='', code=None):
        with open(clusterconfig) as f:
            configfile=f.read()
            self.config = eval(configfile)
        if len(resultfolder) == 0:
            self.resultfolder = self.config['benchmarker']['resultfolder']
        else:
            self.resultfolder = resultfolder
        self.clusterconfig = clusterconfig
        self.code = code
        filename = self.resultfolder+'/'+str(self.code)+'/experiments.config'
        if path.isfile(filename):
            with open(filename,'r') as inp:
                self.experiments = ast.literal_eval(inp.read())
        if self.experiments[0]['clustertype'] == 'K8s':
            self.cluster = masterK8s.testdesign(
                clusterconfig=clusterconfig,#experiments[0]['clusterconfig'],
                configfolder=self.experiments[0]['configfolder'],
                #configfolder=self.resultfolder+'/'+code+'/',#experiments[0]['configfolder'],
                yamlfolder=self.resultfolder+'/'+self.code+'/',#experiments[0]['yamlfolder'],
                #queryfile=experiments[0]['queryfile']
                )
    def runWorkflow(self):
        for i,e in enumerate(self.experiments):
            print(e['step'])
            step = e['step']
            if step == 'prepareExperiment':
                #print(e['docker'])
                #print(e['instance'])
                #print(e['volume'])
                #print(e['initscript'])
                self.cluster.setExperiment(
                    docker=list(e['docker'].keys())[0],
                    instance=e['instance'],
                    volume=e['volume'],
                    script=list(e['initscript'].keys())[0],
                    )
                self.cluster.prepareExperiment()
                self.cluster.delay(e['delay'])
            if step == 'startExperiment':
                self.cluster.setExperiment(
                    docker=list(e['docker'].keys())[0],
                    instance=e['instance'],
                    volume=e['volume'],
                    script=list(e['initscript'].keys())[0],
                    )
                self.cluster.startExperiment()
                self.cluster.delay(e['delay'])
            if step == 'stopExperiment':
                self.cluster.stopExperiment()
            if step == 'cleanExperiment':
                self.cluster.cleanExperiment()
            if step == 'runBenchmarks':
                self.cluster.connectionmanagement = e['connectionmanagement']
                self.cluster.runBenchmarks(
                    connection=e['connection'],
                    configfolder=self.resultfolder+'/'+str(self.code))

