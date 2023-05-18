from easygui import *

def nucleotidesSequence(code):
    s=0
    l=int(len(code))
    nucleotides=[]
    while s<l:
        nucleotidesname=code[s:s+3]
        nucleotides.append(nucleotidesname)
        s=s+3
    return nucleotides

def aminoacidSequence(nucl):
    aminoacids=[]
    for i in nucl:
        if i in ('TTT', 'TTC'):
            aminoacids.append('Phe')
        elif i in ('CTT','CTC','CTA','CTG'):
            aminoacids.append('Leu')
        elif i in ('ATT','ATC','ATA'):
            aminoacids.append('Ile')
        elif i in ('ATG'):
            aminoacids.append('Met')
        elif i in ('GTT','GTC','GTA','GTG'):
            aminoacids.append('Val')
        elif i in ('TCT','TCC','TCA' ,'TCG'):
            aminoacids.append('Ser')
        elif i in('CCT' ,'CCC','CCA','CCG'):
            aminoacids.append('Pro')
        elif i in ('ACT','ACC','ACA','ACG'):
            aminoacids.append('Thr')
        elif i in ('GCT','GCC','GCA','GCG'):
            aminoacids.append('Ala')
        elif i in ('TAT','TAC'):
            aminoacids.append('Tyr')
        elif i in ('TAA','TAG','TGA'):
            break
        elif i in ('CAT','CAC'):
            aminoacids.append('His')
        elif i in ('CAA','CAG'):
            aminoacids.append('Gln')
        elif i in ('AAT','AAC'):
            aminoacids.append('Asn')
        elif i in ('AAA','AAG'):
            aminoacids.append('Lys')
        elif i in ('GAT','GAC'):
            aminoacids.append('Asp')
        elif i in ('GAA','GAG'):
            aminoacids.append('Glu')
        elif i in ('TGT','TGC'):
            aminoacids.append('Cys')
        elif i in ('TGG'):
            aminoacids.append('Trp')
        elif i in ('CGT','CGC','CGA','CGG','AGA','AGG'):
            aminoacids.append('Arg')
        elif i in ('AGT','AGC'):
            aminoacids.append('Ser')
        elif i in ('GGT','GGC','GGA','GGG'):
            aminoacids.append('Gly')
    return aminoacids

def aminointer(aminoacids):
    countpos=0
    countneg=0
    counthydroph=0
    countsulph=0
    for i in aminoacids:
        if i=='Arg' or i=='His' or i=='Lys':
            countpos+=1
        if i=='Asp' or i=='Glu':
            countneg+=1
        if i=='Ala' or i=='Val' or i=='Ile' or i=='Leu' or i=='Met' or i=='Phe' or i=='Tyr' or i=='Trp':
            counthydroph+=1
        if i=='Cys':
            countsulph+=1
    ionic=''
    hydrophobic=''
    disulfide=''
    if countpos>0 and countneg>0:
        ionic='Ionic bonds'
    if counthydroph>1:
        hydrophobic='Hydrophobic interactions'
    if countsulph>1:
        disulfide='Disulfide bonds'
    return ("""
        """+ionic+"""
        """+hydrophobic+"""
        """+disulfide)

def mostfrequent(DNAseq, k):
    frequency={}
    length=len(DNAseq)
    for i in range(length-k+1):
        pattern=DNAseq[i:i+k]
        if pattern in frequency:
            frequency[pattern]+=1
        else:
            frequency[pattern]=1
    listOfpatterns=[]
    for keys, values in list(frequency.items()):
        listOfpatterns.append((values, keys))
    listOfpatterns.sort(reverse=True)
    return listOfpatterns[0]

def cleavage(gencode):
    enzymes={'HindIII':'AGCTT', 'MluCI':'AATT', 'HpyCH4IV':'CGT', 'AfeI':'AGC', 'SwaI':'AAAT', 'EcoP15I':'CAGCAG', 'EcoRV':'GAT', 'EcoRI':'AATTC'}
    listOfenzymes=[]
    for key, value in list(enzymes.items()):
        listOfenzymes.append(key)
    enzyme = choicebox("""Restriction enzymes recognizes specific DNA sequences, and cleave DNA within the recognition sequence. This technique is used to fragment and clone DNA.
Choose restriction enzyme:""", choices = listOfenzymes)
    if enzyme==None:
        return
    seq=enzymes[enzyme]
    if seq in gencode:
        start_at=0
        list_of_positions=[]
        while start_at<len(gencode):
            if seq in gencode:
                part_of_code=gencode[start_at:len(gencode)]
                position_of_site=int(part_of_code.find(seq))
                if position_of_site>0:
                    position_of_site+=start_at
                    position_of_site_real=position_of_site+1
                    list_of_positions.append(position_of_site_real)
                    start_at+=position_of_site_real
                else:
                    break
            else:
                break
        To_cleave_or_not=buttonbox('This plasmid contains '+str(len(list_of_positions))+' sites for '+str(enzyme)+ '. Do you want to cleave this plasmid?', choices=['Yes', 'No'])
        if To_cleave_or_not=='No':
            return
        elif To_cleave_or_not=='Yes':
            start_point=0
            for i in range(len(list_of_positions)):
                part_of_code=gencode[start_point:int(list_of_positions[i])]
                start_point+=int(list_of_positions[i])
                file_name='DNA fragment number '+str(i+1)
                f=open(file_name, 'x')
                f.write(part_of_code)
            last=max(list_of_positions)
            last_file=open('DNA fragment number '+str(len(list_of_positions)+1), 'x')
            last_file.write(gencode[last:])
            msgbox('New files with cleaved fragments were reated!')
    else:
        msgbox('This enzyme can not be used for chosen plasmid')
        
def complimental(sequence):
    compliment=[]
    for i in sequence:
            if i=='A':
                compliment.append('T')
            elif i=='T':
                compliment.append('A')
            elif i=='C':
                compliment.append('G')
            elif i=='G':
                compliment.append('C')
    return ''.join(compliment)

def PCR(nucleotides_):
    sequencePCR=str(''.join(nucleotides_))
    press=buttonbox("""The polymerase chain reaction (PCR) is a method used to rapidly make millions to billions of copies of a specific DNA sample to to study in detail.

Here you can check your DNA sequence, generate the second one as PCR works with double stranded DNA and perform the PCR itself.

(Note that your DNA is considered as coding DNA strand)""", choices = ["Show sequence and generate the coding stand", "Choose the fragment for amplification", "Return"])
    second_strand=complimental(sequencePCR)
    
    if press=='Return':
            return
    elif press=="Show sequence and generate the coding stand":
        press1=buttonbox(nucleotides_, choices=['Return to PCR', 'Generate the second sequence'])
        if press1=='Return to PCR':
            return PCR(nucleotides_)
        elif press1=="Generate the second sequence":
            strands=[nucleotides_, nucleotidesSequence(second_strand)]
            msgbox("""Coding (your) strand:
"""+str(' '.join(strands[0]))+"""

Template (generated) strand:
"""+str(' '.join(strands[1])), 'Double stranded DNA')
            return PCR(nucleotides_)  
            
    elif press=="Choose the fragment for amplification":
        fragment=enterbox('Enter the sequence you want to aplify using capital letters (you can copy it from your sequence)')
        if fragment==None:
            return
        elif fragment not in sequencePCR:
            msgbox('Chosen fragment can not be found within the sequence')
            return PCR(nucleotides_)
        position=sequencePCR.find(fragment)
        position2=sequencePCR.find(fragment)+len(fragment)
        if len(sequencePCR[position2:])<15:
            forprimer1=sequencePCR[position2:]
        else:
            forprimer1=sequencePCR[position2:position2+15] 
        if len(second_strand[:position])<15:
            forprimer2=second_strand[:position]
        else:
            forprimer2=second_strand[position-15:position]
        if len(forprimer1)>len(forprimer2):
            forprimer1=forprimer1[:len(forprimer2)]
        elif len(forprimer2)>len(forprimer1):
            forprimer2=forprimer2[len(forprimer2)-len(forprimer1):]
        primers=[complimental(forprimer1), complimental(forprimer2)]
        meltingTempearture=0
        for i in primers:
            for j in i:
                if j in ('C', 'G'):
                    meltingTempearture+=2
                else:
                    meltingTempearture+=1
        
        
        msgbox("""Your PCR steps:
                1. 96 C for 10 min
                2. 96 C for 10 min
                3. """+str(meltingTempearture)+""" C for 1 min
                4. 72 C for 1 min
                
            Note that steps 2-3 should be performed 25-30 times
            
            Your primers are:
            Forward: """+primers[0]+"""
            Reverse: """+primers[1])
        return PCR(nucleotides_)


buttons = ["yes","quit"]
pressed = buttonbox("Do you want to start?", choices = buttons)
if pressed=='quit':
    quit()
file1=enterbox('Enter the name of file with DNA sequence: ')
try:
    file=open(file1)
except:
    msgbox('File can not be opened')
    quit()
    
    
geneticode=file.read()
for i in geneticode:
    if i=='A' or i=='T' or i=='C' or i=='G':
        continue
    if i=='U':
        msgbox('This is RNA sequence. Choose another file')
        quit()
    else:
        msgbox('This is not a genetic code. Choose another file')
        quit()

while True:
    options = ["Determine amino acid sequence","Calculate the mass of the protein","Find specific part of genome","Find amino acids interaction", "Find the most frequent k-mer", "Cleave this plasmid", "Perform PCR"]
    pressed = choicebox("Choose desirable option: ", choices = options)
    if pressed == None:
        msgbox("You did not choose anything")
        quit()
    elif pressed=="Determine amino acid sequence":
        first=nucleotidesSequence(geneticode)
        second=aminoacidSequence(first)
        msgbox('Amino acids sequence: '+ str(' '.join(second)))
        continue
    elif pressed=='Calculate the mass of the protein':
        first=nucleotidesSequence(geneticode)
        second=aminoacidSequence(first)
        count=0
        for aa in second:
            count+=110
        msgbox('Mass: '+str(count)+ ' Da')
        continue
    elif pressed=="Find specific part of genome":
        part=enterbox('Enter the sequence of nucleotides you want to find: ')
        if part in geneticode:
            position=geneticode.find(part)
            start=int(position)+1
            end=start+len(part)-1
            msgbox('This sequence appears at '+str(start)+ ' nucleotide and ends at '+str(end)+' nucleotide')
        else:
            msgbox('Chosen genetic code does not contaion this sequence')
        continue
    elif pressed=="Find amino acids interaction":
        first=nucleotidesSequence(geneticode)
        second=aminoacidSequence(first)
        interactions=' '.join(aminointer(second))
        msgbox('The protein structure will contain: '+aminointer(second))
        continue
    elif pressed=="Find the most frequent k-mer":
        k=integerbox("""You can find the most frequent sequence that consists of k nucleotides. This could be useful for genome screening and investigation of conservative DNA fragments.
        
        Enter the number of nucloetides (k):""")
        if k==None:
            continue
        else:
            times,sequence=mostfrequent(geneticode, k)
            msgbox('The most frequent '+str(k)+'-mer is '+str(sequence)+'. It appears '+str(times)+' times')
        continue
    elif pressed=="Cleave this plasmid":
        cleavage(geneticode)
    elif pressed=="Perform PCR":
        PCR(nucleotidesSequence(geneticode))
quit()
#genetic_codeRNA.txt
#genetic_codeWITHerror.txt
#Genetic_code_1000.txt