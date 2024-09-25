from Bio import SeqIO
from Bio import Entrez
from Bio import GenBank
import pandas as pd
import os
from pathlib import Path
from bs4 import BeautifulSoup
import requests
import urllib.parse as urlparse
import numpy as np
import json
import shutil
import re
                        
class literature:
    
    def __init__(self):
        
        self.ncbikey='5828bbfa3284f57313641eca97ae01703408' #my apikey https://www.ncbi.nlm.nih.gov/account/settings
        pass 
    
        
    def xrf_pmc(self,project_name,output_dir,qpmids):
        
        if 'PMC' in qpmids[0]:db = 'pmc'
        if 'PMC' not in qpmids[0]:db = 'pubmed'
        
        apmids = [] #all pmids        
        apmcids = [] #all pmc ids
        oapmcids = [] #all open access pmc ids
        xmeta = [] #pmc meta (abstract, title, ids ...)
        asqpmids = [] #all pmids with sequences
        oasqpmcids = [] #all open access pmcids with sequences
        sqmeta = [] #sequences products
        
        splt = 50 #query limit
        start = [n for n in range(0,len(qpmids),splt)] #generated to split query accessions if exceeds splt limit
        end = [*[m for m in range(splt,len(qpmids),splt)],*[len(qpmids)]] #generated to split query accessions if exceeds splt limit  
        ### get filter pubmed ids ###
        
        for n,s in enumerate(start):            
            e = end[n]
            qpmids2 = qpmids[s:e]
            
            ### get all pubmed and pmcids for all accessions ###
            if db == 'pubmed':qpmids2 = ['((EXT_ID:'+qp+') AND (SRC:MED))' for qp in qpmids2]
            if db == 'pmc':qpmids2 = ['(PMCID:'+qp+')' for qp in qpmids2]    
            [pmids,pmcids,oapids,pmetas] = self.get_pmc_meta(qpmids2)
            apmids = [*apmids,*pmids]
            apmcids = [*apmcids,*pmcids]
            oapmcids = [*oapmcids,*oapids]
            xmeta = [*xmeta,*pmetas]
            
            if len(pmids)>1:print(str(pmids[0])+'-'+str(pmids[-1]))
            print(pmids)
            print(pmcids)
            
        # saving outputs #
        sfs = {'xmeta':xmeta,'pmids':list(np.unique(apmids)),'pmcids':list(np.unique(apmcids)),'oapmcids':list(np.unique(oapmcids))}
        self.save_xref_meta(sfs,project_name,output_dir)

    def get_pmc_meta(self,query):
        
        if isinstance(query,list):query=' OR '.join(query) #converts query list into a string
        #query = urlparse.quote(query)
        pmetas = [] #list of ids metadata objects
        pmids = [] #list of pubmed ids
        pmcids = [] #list of pmc ids
        oapids = [] #list of open access pmc ids
        cr_mrk= '' #current cursor mark
        nxt_mrk = '*' #next cursor mark        
        while cr_mrk != nxt_mrk and nxt_mrk!=None:
            try:            
                url = 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?'
                params = {'query':query, 'resultType':'core', 'synonym':'TRUE','cursorMark':nxt_mrk,'pageSize':'999','format':'json'}
                response = requests.get(url,params)
                rjson = response.json()
                cr_mrk = urlparse.unquote(rjson['request']['cursorMark'])
                nxt_mrk = urlparse.unquote(rjson['nextCursorMark']) if 'nextCursorMark' in rjson.keys() else None    
                for rslt in rjson['resultList']['result']:
                    pmeta = {}
                    pmeta['pmid'] = ''
                    pmeta['pmcid'] = ''
                    pmeta['mesh'] = []
                    pmeta['pmc_title'] = ''
                    pmeta['pmc_abstract']= ''
                    pmeta['text_urls'] = []
                    pmeta['oa'] =  ''
                    pmeta['authMan'] = ''
                    pmeta['license'] = ''

                    if 'pmid' in rslt.keys():
                        pmeta['pmid'] = rslt['pmid']
                        pmids.append(rslt['pmid'])                
                    if 'meshHeadingList' in rslt.keys():
                        for m in rslt['meshHeadingList']['meshHeading']:
                            if 'meshQualifierList' in m.keys():
                                for q in m['meshQualifierList']['meshQualifier']:
                                    pmeta['mesh'].append(m['descriptorName'])
                                    pmeta['mesh'].append(q['qualifierName'])
                            else:
                                pmeta['mesh'].append(m['descriptorName'])
                    if 'title' in rslt.keys(): pmeta['pmc_title'] = rslt['title']
                    if 'abstractText' in rslt.keys(): pmeta['pmc_abstract'] = rslt['abstractText']
                    if 'fullTextUrlList' in rslt.keys():            
                        for u in rslt['fullTextUrlList']['fullTextUrl']:
                            pmeta['text_urls'].append(u['url'])
                    if 'isOpenAccess' in rslt.keys():pmeta['oa'] =  rslt['isOpenAccess']
                    if 'authMan' in rslt.keys():pmeta['authMan'] = rslt['authMan']
                    if 'license' in rslt.keys():pmeta['license'] = rslt['license']    
                    if 'pmcid' in rslt.keys() and rslt['pmcid']!='':
                        pmeta['pmcid'] = rslt['pmcid']
                        pmcids.append(rslt['pmcid'])
                        if (rslt['isOpenAccess'] == 'Y' or rslt['authMan'] == 'Y') and pmeta['license']!='':
                        #if rslt['isOpenAccess'] == 'Y':    
                            oapids.append(rslt['pmcid'])                        
                    pmetas.append(pmeta)
            except Exception as e:
                print(e)
                pass
        
        return [pmids,pmcids,oapids,pmetas]

    def save_xref_meta(self,data,db,output_dir):               
        for dk in data.keys():            
            with open(Path(output_dir,db+'_'+dk+'.json'), 'w', encoding='utf-8') as j:
                json.dump(data[dk],j,ensure_ascii=False,indent=4)
            os.chmod(Path(output_dir,db+'_'+dk+'.json'), 0o750)  
            
    def get_ft_xml(self,xml_dir,pmcidsj):
        
        ### load pmcids ###
        with open(pmcidsj) as j: pmcids = json.load(j)
        print(pmcids)
        
        ### remove old dbdir ###        
        if os.path.isdir(xml_dir): shutil.rmtree(xml_dir)
        os.mkdir(xml_dir,0o755)        
        
        ### getting xmls ###
        for pmcid in pmcids:
            print(pmcid)            
            try:
                url = 'https://www.ebi.ac.uk/europepmc/webservices/rest/'+pmcid+'/fullTextXML' # public api
                response = requests.get(url)
                xml = response.text 
                if xml != '':
                    xmlf = Path(xml_dir,pmcid+'.xml')
                    with open(xmlf,'w+') as f:
                        f.write(xml);
                        f.close()
                    os.chmod(xmlf,0o755)            
            except Exception as e:                
                print(e)
                pass  


        
    def get_ft_text(self,xml_dir,output_dirs,pmcidsj):
        
        ### remove old text directories for different full-text sections ###
        for odir in output_dirs:                
            if os.path.isdir(odir):
                shutil.rmtree(odir)
            os.mkdir(odir,0o755)
            for sect in ['abs','intro','method','discuss','result','all','all_mesh']:
                if os.path.isdir(Path(odir,sect)):
                    shutil.rmtree(Path(odir,sect))
                os.mkdir(Path(odir,sect),0o755)


        ### load pmcids ###
        with open(pmcidsj) as j:pmcids = json.load(j)
            
        
        ### parse pmcid xml ###
        for pmcid in pmcids:
            
            print(pmcid)
            
            if pmcid!='' and Path(xml_dir,pmcid+'.xml').is_file() and os.stat(Path(xml_dir,pmcid+'.xml')).st_size < 1000000:
                
                try:
                    sf = open(Path(xml_dir,pmcid+'.xml'))
                    xml = sf.read()
                    soup = BeautifulSoup(xml,'lxml')

                    sects_tags = {'abs':['abstract'],'intro':['intro','introduction'],'method':['methods','materials','materials and methods','materials-and-methods','materials|methods','methods'],'discuss':['discussion','discussions','results|discussion'],'result':['results','results|discussion']} # xml secttags to be included
                    sects = {'abs':[],'intro':[],'method':[],'discuss':[],'result':[],'all':[]}

                    for tag in soup.find_all(['title','p','tr','fig']):

                        text = tag.text.strip()
                        tag_attrs = list(tag.attrs.values())
                        #print(tag_attrs)
                        if tag.name == 'tr':
                            cells = tag.find_all(['th','td'])
                            text = ' '.join([cell.text.strip() for cell in cells]).strip()+'.'
                        #print(text)

                        for ptag in tag.parents:
                            #print(ptag.name)
                            ptag_attrs = list(ptag.attrs.values())
                            ptag_attrs.append(ptag.name.lower())
                            #print(ptag_attrs)
                            if 'sec' in [tag.name,ptag.name] or 'body' in [tag.name,ptag.name]:sects['all'].append(text)
                            for stk in sects_tags:
                                #print(list(np.intersect1d(sects_tags[sect],[*tag_attrs,*ptag_attrs])))
                                if list(np.intersect1d(sects_tags[stk],[*tag_attrs,*ptag_attrs]))!=[]:
                                    #print(sect_tags)
                                    sects[stk].append(text)                      
                                    #print(text)

                    for sect in sects.keys():

                        txt = re.sub(r'[\n\r\s]+',' ',' '.join(sects[sect]))
                        #doc = nlp(txt) # commented out because nlp generates segmentation issue with long texts
                        #snts = [sent.text.strip() for sent in doc.sents] # commented out because nlp generates segmentation issue with long texts

                        snts = sects[sect] # uncomment if segmentation error with long text is generated
                        txt = ' '.join(snts)
                        #print(txt)

                        # saving sentences and text files in the output dirs #
                        if txt != '':
                            jsf = Path(output_dirs[1],sect,pmcid+'.json') # json file
                            with open(jsf, 'w', encoding='utf-8') as j:
                                json.dump(snts,j)
                            os.chmod(jsf, 0o755)     

                            txtf = Path(output_dirs[0],sect,pmcid+'.txt') # text file
                            f = open(txtf,"a",encoding='utf-8')
                            f.write(txt)
                            f.close()
                            os.chmod(txtf, 0o755)
                except Exception as e:                    
                    print(e)
                    pass
        
        
    
    


