import enum
import itertools
import os


def byName(e):
    
    e=list(e).sort(reverse=True,key=str)
    return str(e)
def byLen(e):
    return len(str(e))
def byNo1(e):
    return str(str(e).count("1"))
def byNo2(e):
    return str(str(e).count("2"))
class PT(enum.Enum):
    OP = 1
    CP = 2
    RP = 3



props=[]
class Property:
    def __init__(self, name, property_type):
        self.name = name
        self.property_type = property_type
        props.append(self)
    def __repr__(self):
        return self.name

class Option:
    def __init__(self, name,option_properties):
        self.name = name
        self.option_properties = option_properties
    def __repr__(self):
        return self.name



class Base_Context:
    def __init__(self, name, context_properties):
        self.name = name
        self.context_properties = context_properties
    

class Context:
    def __init__(self, base_context=Base_Context('',[]), options=[], relational_properties=[]):
        self.base_context = base_context
        if(relational_properties==[]):
            for i in range(0,len(options)):
                relational_properties.append([])
            
        self.option_tuples = []
        
        for ind, option in enumerate(options):
            self.option_tuples.append((option, relational_properties[ind], set(relational_properties[ind]).union(set(self.base_context.context_properties).union(set(option.option_properties)))))

        #print(option_tuples)
    def options_masked(self,mask):
        ret=[]
        for i, val in enumerate(mask):
            if(val):
                ret.append(self.option_tuples[i])
        return ret





#moral_theory_to_def_rel ={'Util':{},'Deon':
# deon_defeat=set(({},{'Breaks(2,A)'}),
#                                             ({},{'Breaks(2,B)'}),
#                                             ({'Breaks(2,A)'},{'Breaks(2,B)'}),
#                                             ({'Breaks(2,B)'},{'Breaks(2,A)'}),
#                                             ({'Breaks(2,A)'},{'Breaks(1,A)'}),
#                                             ({'Breaks(2,B)'},{'Breaks(1,B)'})
#                           )
# #alt solution: 
    #represent sets of properties properly. sort values that can get those sets.


def all_subsets(properties):
    #create a list of every possible subset, as frozen sets.
    prop=set(properties)
    ret=[]
    for i in range (0,len(prop)+1):
        comb=list(itertools.combinations(prop,i))
        for i in range(0,len(comb)):
            comb[i]=frozenset(comb[i])
        ret=ret+comb
    return ret




def relevant_in_theory(name):
    #get every property that is relevant in some base context for the theory
    n_for_theory=moral_theory_to_norm_rel[name]
    props_relevant_in_theory=set([])
    for i in n_for_theory.values():
        props_relevant_in_theory=props_relevant_in_theory.union(i)
    return props_relevant_in_theory

def property_subset_names(props):
    #takes list of subsets, makes dictionary from numbers to sets.
    ss=set(props)
    ss=list(props)

    subset_names={}
    for i in range(len(ss)):
        s=set(ss[i])
        subset_names.update({i:s})
    return subset_names

def property_subset_list(props):
    #takes list of subsets, makes list of sets
    ss=set(props)
    ss=list(props)

    subset_names=[]
    for i in range(len(ss)):
        s=set(ss[i])
        subset_names.append(s)
    return subset_names
def get_defeat_samples(name):
    pass

import pandas as pd

def transitiveClosure(rel):
    #inefficient implementation I know.
    #0 defeats 3, 3 defeats 4, then 0 defeats 4
    fin_rel=rel.copy()
    for i in rel.index:
        for j in rel.columns:
            if(rel.at[i,j]):
                for k in rel.columns:
                    if(rel.at[j,k]):
                        fin_rel.at[i,k]=True
            
    if rel.sum().sum()<fin_rel.sum().sum():
        print("transitive again")
        fin_rel=transitiveClosure(fin_rel)
    return fin_rel

def reflexiveClosure(rel):
    print(rel.index)
    for i in rel.index:
        rel.at[i,i]=True
    return rel

def separableClosureOld(rel, props):
    fin_rel=rel.copy()
    for i in props:
        c_props=props.copy()
        c_props.remove(i)
        subsets_without_i=all_subsets(c_props)
        positive:bool=False
        negative:bool=False
        #check if i is positive, negative or both
        #positive: causes sets with it to defeat
        #negative: causes sets with it to be defeated
        for j in subsets_without_i:
            j_plus_i=j.copy()
            j_plus_i=set(j_plus_i)
            j_plus_i.add(i)
            j_plus_i=frozenset(j_plus_i)
            if rel.at[j,j_plus_i]:
                negative=True
                if positive:
                    break
            if rel.at[j_plus_i,j]:
                positive=True
                if negative:
                    break
        print("%s is negative:%s positive:%s"%(i,negative,positive))
        for j in subsets_without_i:
            j_plus_i=j.copy()
            j_plus_i=set(j_plus_i)
            j_plus_i.add(i)
            j_plus_i=frozenset(j_plus_i)
            if negative:
                fin_rel.at[j,j_plus_i]=True
            if positive:
                fin_rel.at[j_plus_i,j]=True
    if rel.sum().sum()<fin_rel.sum().sum():
        print("separable again")
        fin_rel=separableClosureOld(fin_rel,props)
    return fin_rel
def separableClosureNew(rel,props):
        #alt maybe better:
    #   for each pair, extract the part that overlaps
    #   get all subsets of that part,
    #   copy the trues in the originals' relationship to them with each subset added
    
    #   for each pair, get the part that is missing
    #   for all subsets of that part,
    #   copy the trues in the originals' relationship to them with each subset added
    
    pass
def separableClosure(rel, props):
    #s1>s2 <-> s1+s3>s2+s3
    
    #this probably doesn't do exactly that?
    #more like
     #sX+s3>sX <-> sY+s3>sY
     #sX-s3>sX <-> sY-s3>sY
    
    fin_rel=rel.copy()

    sub=all_subsets(props)
    for i in sub:
        #subtract that subset from total
        c_props=props.copy()
        for j in i: 
            c_props.remove(j)
        #get all subsets of what's left
        subsets_without_i=all_subsets(c_props)
        #check if set i is positive, negative or both
        #positive: causes sets with it to defeat
        #negative: causes sets with it to be defeated
        positive:bool=False
        negative:bool=False
        for j in subsets_without_i: 
            #make a copy with i added
            j_plus_i=j.copy()
            j_plus_i=set(j_plus_i)
            for k in i:
                j_plus_i.add(k)
            j_plus_i=frozenset(j_plus_i)
            
            #negative: defeated by itself without i
            #positive: defeats itself without i
            if rel.at[j,j_plus_i]:
                negative=True
                if positive:
                    break
            if rel.at[j_plus_i,j]:
                positive=True
                if negative:
                    break
        print("%s is negative:%s positive:%s"%(i,negative,positive))
        for j in subsets_without_i:
            j_plus_i=j.copy()
            j_plus_i=set(j_plus_i)
            for k in i:
                j_plus_i.add(k)
            j_plus_i=frozenset(j_plus_i)
            if negative:
                fin_rel.at[j,j_plus_i]=True
            if positive:
                fin_rel.at[j_plus_i,j]=True
    if rel.sum().sum()<fin_rel.sum().sum():
        print("separable again")
        fin_rel=separableClosure(fin_rel,props)
    return fin_rel       
                
    #get 
    #for each true pair
    for i in range(0,len(rel)):
        for j in range(0,len(rel)):
            if rel.at[i,j]==True:
                
                pass
    #select the properties that pair represents
    #for each property, try to add that property to both.
    #if that works, flip it to true.
    #call this if that made it grow.
    return fin_rel

class Theory:
    def __init__(self, name):
        #a theory has a name
        self.name = name
        
        #constraints
        self.constr=moral_theory_constraints[self.name]
        
        #N function
        self.norm = moral_theory_to_norm_rel[self.name]
        
        #properties relevant in some context
        self.ever_N=relevant_in_theory(self.name)
        print(self.ever_N)
        
        #all subsets of those properties (as tuples)
        self.ever_N_subsets=all_subsets(self.ever_N)
        print(self.ever_N_subsets)
        self.ever_N_subsets.sort(key=byNo2)
        self.ever_N_subsets.sort(key=byNo1)
        #defeat relation
        self.defeat_relation=pd.DataFrame(False, index=self.ever_N_subsets, 
                                          columns=self.ever_N_subsets)
        print(self.defeat_relation)
        #populate defeat relation with defeat samples
        samp=moral_theory_defeat_samples[self.name]

        for i in samp:
            i=list(i)
            print(i)
            win=frozenset(i[0])
            lose=frozenset(i[1])
            
            self.defeat_relation.at[win,lose]=True
        
        
        if self.constr[CN.ref.value]:
            self.defeat_relation=reflexiveClosure(self.defeat_relation)
        #repeat closures until there is no change
        repeat=True
        while(repeat):
            defeat_before=self.defeat_relation.copy()
            if self.constr[CN.trans.value]:
                self.defeat_relation=transitiveClosure(self.defeat_relation)
            if self.constr[CN.separ.value]:
                self.defeat_relation=separableClosure(self.defeat_relation,self.ever_N)
            repeat=defeat_before.sum().sum()<self.defeat_relation.sum().sum()
            print("repeat %s"%repeat)
        self.defeat_relation.to_csv(os.getcwd()+"/defeat_relation.csv")

        print(self.defeat_relation)
        print(self.defeat_relation.sum().sum())
        print(self.notComparable())
    
    
    def rightness(self,context):  
        #make full mask
        right_options=list(pd.Series(True,index=range(0,len(context.option_tuples))))
        #make normatively relevant properties of each option-context pair
        relevant_properties=[]
        normNames=set()
        for i in self.norm[context.base_context]:
            normNames.add(i)
        for i in context.option_tuples:
            i_props=set(i[2])
            i_props=i_props.intersection(normNames)
            relevant_properties.append(frozenset(i_props))
        print("relevant properties:" +str(relevant_properties))
        #each index is the relevant properties of the option at that index.
        for i in range(0,len(right_options)):
            i_ind=frozenset(relevant_properties[i])
            for j in range (0, len(right_options)):
                j_ind=frozenset(relevant_properties[j])
                if not self.defeat_relation.at[i_ind,j_ind]: #if i does not defeat j. note this includes i==j
                    right_options[i]=False #i is not right
                    break 	#stop looping j since i has been disqualified.
        print(right_options)
        return right_options #which is now a list of booleans where True means something is right.
    
    
    def evaluate(self,context,functionIndex=0):
        mask=self.rightness(context)
        return context.options_masked(mask)
    
    def notComparable(self):
        #return index pairs that are false both ways
        ret=[]
        ind=self.defeat_relation.index
        for i in range(0,len(ind)):
            for j in range(i,len(ind)):
                if (not self.defeat_relation.at[ind[i],ind[j]]) and (not self.defeat_relation.at[ind[j],ind[i]]):
                    ret.append([ind[i],ind[j]])
        return ret
#START OF THINGS FOR USERS TO USE
                

#properties. 
#the second input is to check that only the right kind of thing can have them
#that check is not implemented.

#option properties representing breaking rules
opt_p_1A = Property('Br(1,A)', PT.OP.value)
opt_p_1B = Property('Br(1,B)', PT.OP.value)
opt_p_2A = Property('Br(2,A)', PT.OP.value)
opt_p_2B = Property('Br(2,B)', PT.OP.value)

#context properties representing reserved
con_p_RA = Property('Re(A)', PT.CP.value)
con_p_RB = Property('Re(B)', PT.CP.value)

#context properties representing allergy
con_p_AA = Property('Al(A)', PT.CP.value)
con_p_AB = Property('Al(B)', PT.CP.value)

#options. 1st value name, 2nd value option properties
opt_A = Option('use medicine A',[opt_p_1A, opt_p_2A]) 
opt_B = Option('use medicine B',[opt_p_1B, opt_p_2B])

#base contexts. 1st value name, 2nd value context properties. 
                        #not sure why these are in sets and the above are in lists.
base_cont_1 = Base_Context('AllergicB',{con_p_RA, con_p_AB})    #A reserved, but allergic to B
base_cont_2 = Base_Context('AllergicA',{con_p_RA, con_p_AA})    #A reserved, and allergic to A
base_cont_3 = Base_Context('NotAllergic',{con_p_RA})            #A reserved, not allergic
base_cont_4 = Base_Context('BothReserved',{con_p_RA, con_p_RB}) #A and B reserved, not allergic

#contexts. 1st value base context, 2nd value options, 3rd value relational properties - list of 1 list for each option
cont_1 = Context(base_cont_1,[opt_A,opt_B],[[],[]])
cont_2 = Context(base_cont_2,[opt_A,opt_B],[[],[]])
cont_3 = Context(base_cont_3,[opt_A,opt_B],[[],[]])
cont_4 = Context(base_cont_4,[opt_A,opt_B],[[],[]])

#normative relevance functions for each theory. maps from a base context to a set of properties.
#note. if adding new properties, they need to be here. I should make that also check the samples to see what it needs to care about.
moral_theory_to_norm_rel = {'Util':{},'Deon':{base_cont_2:{opt_p_1A,opt_p_2A},
                                            base_cont_1:{opt_p_1B,opt_p_2A},
                                              base_cont_3:{opt_p_2A},
                                            base_cont_4:{opt_p_2B,opt_p_2A}
                                            }}
#started implementing closures based on constraints on each theory's defeat relation.
class CN(enum.Enum):
    ref = 0     #reflexive
    trans = 1   #transitive
    separ = 2   #separable (atomistic) #NOT DONE
#if the given value is true here for the theory, it'll run that kind of closure.
moral_theory_constraints = {'Util':[True,True,True], 'Deon':[True,True,True]}

#samples of sets. first in a row defeats the second
moral_theory_defeat_samples ={'Util':[], 'Deon':[((),(opt_p_2A,)),           #breaking fewer instances of a given rule is better
                                                 ((),(opt_p_2B,)),
                                                 ((),(opt_p_2A,opt_p_2B)),
                                                 ((),(opt_p_1A,)),
                                                 ((),(opt_p_1B,)),
                                                 ((),(opt_p_2A,opt_p_1B)),
                                                 ((),(opt_p_2B,opt_p_1A)),
                                                 ((),(opt_p_2A,opt_p_2A,opt_p_1B)),
                                                 ((),(opt_p_2B,opt_p_2A,opt_p_1A)),
                                                 
                                                 
                                                 ((),(opt_p_1A,opt_p_2B,opt_p_2A)),
                                                 ((),(opt_p_1A,opt_p_2B,opt_p_2A)),
                                                 ((),(opt_p_1A,opt_p_1B,opt_p_2B)),
                                                 ((),(opt_p_1A,opt_p_1B,opt_p_2A)),
                                                 
                                                 ((opt_p_2A,),(opt_p_1A,)), #lower number is worse to break
                                                 ((opt_p_2B,),(opt_p_1B,)),
                                                 ((opt_p_2A,),(opt_p_1B,)),
                                                 ((opt_p_2B,),(opt_p_1A,)),
                                                 
                                                 ((opt_p_2B,),(opt_p_2A,)), #breaking the same number of equally severe rules is equally bad
                                                 ((opt_p_2A,),(opt_p_2B,)), #breaking 1 2 rule
                                                 
                                                 ((opt_p_1B,),(opt_p_1A,)), #breaking 1 1 rule
                                                 ((opt_p_1A,),(opt_p_1B,)), 
                                                 
                                                 ((opt_p_1B,opt_p_2B),(opt_p_1A,opt_p_2A)), #1 2 and 1 1
                                                 ((opt_p_1A,opt_p_2A),(opt_p_1B,opt_p_2B)),
                                                 ((opt_p_1B,opt_p_2A),(opt_p_1A,opt_p_2A)), 
                                                 ((opt_p_1A,opt_p_2A),(opt_p_1B,opt_p_2A)),
                                                 ((opt_p_1A,opt_p_2B),(opt_p_1B,opt_p_2B)), 
                                                 ((opt_p_1B,opt_p_2B),(opt_p_1A,opt_p_2B)),
                                                 
                                                 
                                                 ((opt_p_1A,opt_p_2B,opt_p_2A),(opt_p_1B,opt_p_2B,opt_p_2A)),  #2 2 and 1 1
                                                 ((opt_p_1B,opt_p_2B,opt_p_2A),(opt_p_1A,opt_p_2B,opt_p_2A)),
                                                 
                                                 ((opt_p_1A,opt_p_1B,opt_p_2A),(opt_p_1A,opt_p_1B,opt_p_2B)),  #1 2 and 2 1
                                                 ((opt_p_1A,opt_p_1B,opt_p_2B),(opt_p_1A,opt_p_1B,opt_p_2A)),
                                                 
                                                 ((opt_p_2A,opt_p_2B,),(opt_p_1A,)), #rather break both higher than 1 lower
                                                 ((opt_p_2A,opt_p_2B,),(opt_p_1B,)), 
                                                 
                                                 ((opt_p_2A,opt_p_2B,opt_p_1A,),(opt_p_1A,opt_p_1B)), #rather break 2 higher and 1 lower than both higher



                                                 ]}









            
#make theories, automatically loads info about them from above based on the name.
#th_1 = Theory('Util')
th_2 = Theory('Deon')

#gives answers. currently set up to choose from same 2 options for 4 contexts
print("base context: "+ str(cont_1.base_context.name))
print(th_2.evaluate(cont_1))
print("")
print("base context: "+ str(cont_2.base_context.name))
print(th_2.evaluate(cont_2))
print("")
print("base context: "+ str(cont_3.base_context.name))
print(th_2.evaluate(cont_3))
print("")
print("base context: "+ str(cont_4.base_context.name))
print(th_2.evaluate(cont_4))


