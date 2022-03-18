#!/usr/bin/env python
# coding: utf-8

# In[1]:


import fitz
import glob
import os


# In[2]:


if not os.path.exists('Results'):
    os.makedirs('Results')


# In[3]:


def outputAct(s,f,act,pType):
    doc2 = fitz.open()  
    doc2.insert_pdf(doc, from_page=s,to_page = f)
    if pType == 'I':
        pType = 'Inv'
    else:
        pType = 'Crn'
    doc2.save("Results\\"+pType + ' 0-' + act + ".pdf")


# In[4]:


def splitFile(doc):
    i=0 # Track current page number
    s=0 # Start of page for this account
    f=0 # Finish page for account
    d=0 # Flag to show whether we're in multi-page or not
    act1 ="0"
    pType1 = "0"
    for page in doc:
        pageType =page.get_text("blocks")[2][4].replace('\n',' ') # This seems to be the location of where the 'INVOICE' wording is on the left of the PDF
        # print(page.get_text("blocks")) # Uncomment this to view the text in case you need to find other text on the page
        if 'INVOICE' in pageType:
            pType = 'I'
        else:
            pType = 'C'
        act = page.get_text("blocks")[4][4].replace('\n','')[-5:] # This appears to be the location of the account number so return last 5 chars as per req.
        if(act ==act1):
            f=i
            d=1  # if act = act1 then we must be now in multi-page so set flag.
        else:
            if d==1: #If we are in multi-page and act!=act1 then this means we've found the end of the account pages
                f=i-1
                outputAct(s,f,act1,pType1)
                d=0 #reset everything once we have output the multi-page pdf
                s=i
                f=i
            else:
                if act1 != '0':
                    outputAct(s,f,act1,pType1)
                s=i
                f=i
        i=i+1
        act1 = act
        pType1 = pType


# In[5]:


for f in glob.glob("*.pdf"):
    doc = fitz.open(f)  
    splitFile(doc)
    doc.close()


# In[ ]:




