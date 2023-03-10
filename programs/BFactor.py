from libtbx.program_template import ProgramTemplate
from iotbx.pdb import common_residue_names_get_class as get_class
from cctbx import adptbx
import sys

class pv_data(dict):
  def __re1pr__(self):
    outl = 'test'
    return outl

# Display the number of residue group/chains in the protein that are above a chosing B-Factor 
  def NumHighBFactor(self, chain_id, BFactorThreshHold, atr = 'res'): 
    rc = self.get_chain(chain_id)
    NumHigh = 0
    for i,(key,item) in enumerate(rc.items()):
      # print(i,key,item)
      if item.get(atr, 0) > BFactorThreshHold:
        NumHigh += 1
    return NumHigh

  def get_chain(self, chain_id):
    tmp = {}
    for key, item in self.items():
      if key.find(chain_id)>-1:
        tmp[key]=item
    return tmp

class Program(ProgramTemplate):
  datatypes = ['model','phil']

  def validate(self): 
    pass

#--------------------------------------------------------
  def BFactorFinder(self):
    model = self.data_manager.get_model()
    #print('model',dir(model))
    BFactor = pv_data()
    hierarchy = model.get_hierarchy()
    for residue_group in hierarchy.residue_groups():
      averages = {}
      num_mc = 0
      num_sc = 0
      atom_group = residue_group.atom_groups()[0]
      # assert 0
      atom_Type = get_class(atom_group.resname)
      if atom_Type != 'common_amino_acid': 
        continue

      for atom in residue_group.atoms():
        IndividualBFactor = {}
        ag = atom.parent()
        rg = ag.parent()
        chain = rg.parent()
        if atom.element_is_hydrogen():
          continue
        # print(dir(atom))
#------------------------------------------------------------
  #Anisotropic BFactor Check
      # if (atom.uij_is_defined):
      #   print(atom.uij)
      #   print(adptbx.u_as_b(adptbx.u_cart_as_u_iso(atom.uij)))
      #   print(atom.b) 
#------------------------------------------------------------
  #See Different Classes and Branches
        # print(ag.resname,chain.id, rg.resseq)
    # print(dir(ag))
    # print('rg',rg.id_str())
    # print(chain.id)
    # print(ag.resname,chain.id, rg.resseq)
#------------------------------------------------------------
  # Math to calculate different sum of B-Factor averages 
        averages.setdefault('res', 0)
        averages['res'] += atom.b 

      # Find CA and their B-Factor sum
        if atom.name.strip() == 'CA':
          averages['CA'] = atom.b

      # Number of main chain and their sum
        if atom.name.strip() in ['CA', 'N', 'C', 'O', 'OXT']:
          averages.setdefault('main', 0)
          averages['main'] += atom.b
          num_mc += 1
      
      # Number of side chain and their sum
        else:
          averages.setdefault('side', 0)
          averages['side'] += atom.b
          num_sc += 1 
    
    # Averages      
      if num_mc != 0:
        averages['main'] /= num_mc
      if num_sc != 0:
        averages['side'] /= num_sc
      averages['res'] /= (num_mc + num_sc)

      BFactor[ag.id_str()] = averages

  # Display calculation of averages      
    for key, item in BFactor.items():
      print(key, item)
    print('Chain A residue groups B-factor averages', BFactor.get_chain("A"))
    print('Chain B residue groups B-factor averages',BFactor.get_chain("B"))
   
    print('Chain A residue group averages B-factors higher than 10', BFactor.NumHighBFactor('A',10))
    print('Chain A, side residue group averages B-factors higher than 12', BFactor.NumHighBFactor('A',12, 'side'))


  def run(self): 
    self.BFactorFinder()

  def results(self):
    return self.results


# import sys
#   from iotbx.cli_parser import run_program
#   if len(sys.argv)>=1:
#     print('provide PDB file')
#     exit()
#   else:
#     pdb_file = sys.argv[1]
#     results = run_program(program_class=Program, args=sys.argv[1:])

