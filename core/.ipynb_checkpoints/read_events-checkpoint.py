

__all__ = ["EventStore"]

from ROOT import gROOT
from ROOT import TFile, TTree



class EventStore( object ):
    
  __container_keys = [
                  "CaloClusterContainer_Clusters"     ,
                  "CaloCellContainer_Cells"           ,
                  "CaloRingsContainer_Rings"          ,
                  "EventInfoContainer_EventInfo"      ,
                  "TruthParticleContainer_Particles"  ,
                  "CaloDetDescriptorContainer_Cells"  ,
  ]

  #
  # Constructor
  #
  def __init__( self, filename, path):
    self.path = path
    self.filename = filename


    self.configure()

  def __del__(self):
    self.__file.Close()
    del self.__tree
    del self.__file

  #
  # Configure the event store
  #
  def configure(self):

    # load all necessary libraries by hand
    try:
        from ROOT import xAOD
    except:
        from . import dataframe_h
        gROOT.ProcessLine(dataframe_h)

    self.__file = TFile(self.filename)
    self.__tree = self.__file.Get(self.path)



  #
  # Get the container
  #
  def retrieve(self, key):
    return getattr( self.__tree, key ) if key in self.__container_keys else list()


  #
  # Read the current event
  #
  def GetEntry(self, evt):
    return self.__tree.GetEntry(evt)

  #
  # Get the total number of events
  #
  def GetEntries(self):
    return self.__tree.GetEntries()

  #
  # Get all container keys available
  #
  def keys(self):
    return self.__container




if __name__ == "__main__":

    from Gaugi import progressbar
    from pandas import DataFrame
        
    path='/home/jodafons/public/cern_data/simulation/MonteCarlo_Simulation_SingleParticle_Electron_50GeV_WithMagneticField/AOD/electrons.AOD.root'
    event = EventStore(path, "physics")
    nov=1
    vars = ['e','et','eta','phi','reta','rphi','rhad','eratio','weta2','f1','f3']
    d = { key:[] for key in vars }
    d['rings'] = []
    if nov < 0 or nov > event.GetEntries():
        nov = event.GetEntries()
    
    for entry in progressbar( range(nov) , 'Reading...') : 
        event.GetEntry(entry)
        cluster_cont = event.retrieve("CaloClusterContainer_Clusters")
        rings_cont = event.retrieve("CaloRingsContainer_Rings")
        for caloRings in event.retrieve("CaloRingsContainer_Rings"):
            emClus = cluster_cont.at(caloRings.cluster_link)
            for key in vars:
                d[key].append( getattr(emClus,key) )    
            #d['rings'].append(stdvector2list(caloRings.rings))
            
    print(d)
