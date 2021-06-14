import enum
import itertools

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


def all_Subsets(properties):
    #create a list of every possible subset
    prop=set(properties)
    ret=[]
    for i in range (0,len(prop)+1):
        ret=ret+list(itertools.combinations(prop,i))
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
            if(rel.iat[i,j]):
                for k in rel.columns:
                    if(rel.iat[j,k]):
                        fin_rel.iat[i,k]=True
            
    if rel.sum().sum()<fin_rel.sum().sum():
        print("transitive again")
        transitiveClosure(fin_rel)
    return fin_rel

def reflexiveClosure(rel):
    for i in rel.index:
        rel.iat[i,i]=True
    return rel

def separableClosure(theory, props):
    ##NOT DONE
    rel=theory.defeat_relation.copy()
    fin_rel=rel.copy()
    #for each true pair
    for i in range(0,len(rel)):
        for j in range(0,len(rel)):
            if rel.iat[i,j]==True:
                pass
    #select the properties that pair represents
    #for each property, try to add that property to both.
    #if that works, flip it to true.
    #call this if that made it grow.
    for i in props:
        for j in rel:
            m0=j[0].union({i})
            m1=j[1].union({j})
            if not(len(m0)==len(j[0]) or len(m1)==len(j[1])):
                fin_rel.append((m0,m1))
            m0=j[0].remove(i)
            m1=j[1].remove(j)
            if not(len(m0)==len(j[0]) or len(m1)==len(j[1])):
                fin_rel.append((m0,m1))
                
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
        self.ever_N_subsets=all_Subsets(self.ever_N)
        
        #unique IDs for all possible subsets of those properties
        #(necessary for defeat relation, python sets have problems with mutable objects)
        self.relevant_subset_list=property_subset_list(self.ever_N_subsets)
        
        #defeat relation
        self.defeat_relation=pd.DataFrame(0, index=range(0,len(self.relevant_subset_list)), 
                                          columns=range(0,len(self.relevant_subset_list)))
        #populate defeat relation with defeat samples
        samp=moral_theory_defeat_samples[self.name]

        for i in samp:
            i=list(i)
            if(i[0]==()):
                i[0]=set()
            if(i[1]==()):
                i[1]=set()
            win=self.relevant_subset_list.index(set(i[0]))
            lose=self.relevant_subset_list.index(set(i[1]))
        
            self.defeat_relation.iat[win,lose]=True
        
        print(self.relevant_subset_list)
        if self.constr[CN.ref.value]:
            self.defeat_relation=reflexiveClosure(self.defeat_relation)
        if self.constr[CN.trans.value]:
            self.defeat_relation=transitiveClosure(self.defeat_relation)
        
        print(self.defeat_relation)
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
            relevant_properties.append(i_props)
        print("relevant properties:" +str(relevant_properties))
        #each index is the relevant properties of the option at that index.
        for i in range(0,len(right_options)):
            i_ind=self.relevant_subset_list.index(relevant_properties[i])
            for j in range (0, len(right_options)):
                j_ind=self.relevant_subset_list.index(relevant_properties[j])
                if not self.defeat_relation.iat[i_ind,j_ind]: #if i does not defeat j. note this includes i==j
                    right_options[i]=False #i is not right
                    break 	#stop looping j since i has been disqualified.
        return right_options #which is now a list of booleans where True means something is right.
    def evaluate(self,context,functionIndex=0):
        mask=self.rightness(context)
        return context.options_masked(mask)

#START OF THINGS FOR USERS TO USE
                

#properties. 
#the second input is to check that only the right kind of thing can have them
#that check is not implemented.
opt_p_1A = Property('Breaks(1,A)', PT.OP.value)
opt_p_1B = Property('Breaks(1,B)', PT.OP.value)
opt_p_2A = Property('Breaks(2,A)', PT.OP.value)
opt_p_2B = Property('Breaks(2,B)', PT.OP.value)

con_p_RA = Property('Reserved(A)', PT.CP.value)
con_p_RB = Property('Reserved(B)', PT.CP.value)

con_p_AA = Property('Allergic(A)', PT.CP.value)
con_p_AB = Property('Allergic(B)', PT.CP.value)

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

#samples of things that defeat. need a lot for deontology because I'm not done with separable closure.
#you should actually declare any conflicts you want to check here, because of that.
moral_theory_defeat_samples ={'Util':[], 'Deon':[(set(),(opt_p_2A,)),           #nothing is better than something
                                                 (set(),(opt_p_2B,)),   
                                                 (set(),(opt_p_1A,opt_p_2A)),
                                                 ((opt_p_2A,),(opt_p_1A,)), #lower number is worse to break
                                                 ((opt_p_2A,),(opt_p_1B,)),
                                                 ((opt_p_2B,),(opt_p_1A,)),
                                                 ((opt_p_2B,),(opt_p_1B,)),
                                                 ((opt_p_2B,),(opt_p_2A,)), #same number is equally bad
                                                 ((opt_p_2A,),(opt_p_2B,)),
                                                 ((opt_p_1B,),(opt_p_1A,)), 
                                                 ((opt_p_1A,),(opt_p_1B,)),
                                                 ((opt_p_2A,opt_p_2B,),(opt_p_1A,)), #rather break both lower than one higher
                                                 ((opt_p_2A,opt_p_2B,),(opt_p_1B,)),
                                                 ((opt_p_1A,),(opt_p_1A,opt_p_2A)), #rather break 1 higher than 1 lower and 1 higher
                                                 ((opt_p_1A,),(opt_p_1A,opt_p_2B)),
                                                 ((opt_p_1A,),(opt_p_1B,opt_p_2A)),
                                                 ((opt_p_1A,),(opt_p_1B,opt_p_2B)),
                                                 ((opt_p_1B,),(opt_p_1A,opt_p_2A)),
                                                 ((opt_p_1B,),(opt_p_1A,opt_p_2B)),
                                                 ((opt_p_1B,),(opt_p_1B,opt_p_2A)),
                                                 ((opt_p_1B,),(opt_p_1B,opt_p_2B)),
                                                 ]}









            
#make theories, automatically loads info about them from above based on the name.
th_1 = Theory('Util')
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


