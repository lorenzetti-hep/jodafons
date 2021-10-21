

__all__ = ["EventStore"]

from ROOT import gROOT
from ROOT import TFile, TTree



class EventStore( object ):


  #
  # Constructor
  #
  def __init__( self, filename, path):
    self.path = path
    self.filename = filename

    # load all necessary libraries by hand
    try:
        from ROOT import xAOD
    except:
        from lorenzetti_utils import dataframe_h
        gROOT.ProcessLine(dataframe_h)

    self.configure()


  #
  # Configure the event store
  #
  def configure(self):

    self.__file = TFile(self.filename)
    self.__tree = self.__file.Get(self.path)

    # setup all containers
    from ROOT import xAOD, std
    self.__container = {
                  "CaloClusterContainer_Clusters"     : std.vector(xAOD.CaloCluster_t)(),
                  "CaloCellContainer_Cells"           : std.vector(xAOD.CaloCell_t)(), 
                  "CaloRingsContainer_Rings"          : std.vector(xAOD.CaloRings_t)(),
                  "EventInfoContainer_EventInfo"      : std.vector(xAOD.EventInfo_t)(),
                  "TruthParticleContainer_Particles"  : std.vector(xAOD.TruthParticle_t)(),
                  "CaloDetDescriptorContainer_Cells"  : std.vector(xAOD.CaloDetDescriptor_t)(),
                  }
    for key, cont in self.__container.items():
      self.__tree.SetBranchAddress(key,cont)


  #
  # Get the container
  #
  def retrieve(self, key):
    container = getattr( self.__tree, key )
    #return self.__container[key]
    return container

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
  def keys(self):
    return self.__container.keys()




if __name__ == "__main__":

        
        
    path='/home/jodafons/public/cern_data/simulation/MonteCarlo_Simulation_SingleParticle_Electron_50GeV_WithMagneticField/AOD/electrons.AOD.root'
    event = EventStore(path, "physics")
    nov=10
    vars = ['e','et','eta','phi','reta','rphi','rhad','eratio','weta2','f1','f3']
    d = { key:[] for key in vars }
    d['rings'] = []
    if nov < 0 or nov > event.GetEntries():
        nov = event.GetEntries()
    
    for entry in progressbar( range(nov) , 'Reading...') : 
        event.GetEntry(entry)
        cluster_cont = event.retrieve("CaloClusterContainer_Clusters")
        rings_cont = event.retrieve("CaloRingsContainer_Rings")
        #for caloRings in event.retrieve("CaloRingsContainer_Rings"):
        #    emClus = cluster_cont.at(caloRings.cluster_link)
        #    #for key in vars:
        #    #    d[key].append( getattr(emClus,key) )    
        #    #d['rings'].append(stdvector2list(caloRings.rings))
            
    print(d)
