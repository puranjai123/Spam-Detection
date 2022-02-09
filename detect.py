#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import nltk
import string
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

def clean_text(msg):
    stpwrds=stopwords.words('english')
    stpwrds.remove('not')
    stpwrds.remove("don't")
    stpwrds.remove("hasn't")
    stpwrds.remove("haven't")
    stpwrds.remove("wasn't")
    stpwrds.remove("weren't")
    def remv_punct(msg):
        return re.sub(f'[{string.punctuation}]','',msg)
    def remv_stpwrds(msg):
        words=word_tokenize(msg)
        new_word=[]
        for w in words:
            if (w not in stpwrds):
                new_word.append(w)
        return " ".join(new_word)
    def stemming(msg):
        ps=PorterStemmer()
        words=word_tokenize(msg)
        new_words=[]
        for w in words:
            new_words.append(ps.stem(w))
        return " ".join(new_words)
    X1=remv_punct(msg)
    X2=X1.lower()
    X3=remv_stpwrds(X2)
    X4=stemming(X3)
    return X4            

df=pd.read_csv('spam.txt',names=['msg_types','msg'])
df.msg=list(map(clean_text,df.msg))
cv=TfidfVectorizer(binary=False,ngram_range=(1,2))
X=cv.fit_transform(df.msg).toarray()
y=df.msg_types
clf=MultinomialNB()
clf.fit(X,y)

win=Tk()
win.state('zoomed')
win.resizable(width=False,height=False)
win.configure(bg='blue')
win.title('Ek no. Bar and Restuarant')
lbl_title=Label(win,text="Spam Detection",font=('',50,'bold'),bg='blue',fg='white')
lbl_title.place(relx=.3,rely=0)

def singlepred(entry_feedback,lbl_result):
    usr_review=entry_feedback.get()
    ct=clean_text(usr_review)
    X_test=cv.transform([ct]).toarray()
    pred=clf.predict(X_test)
    if (pred[0]=='ham'):
        lbl_result.configure(text="Ham",fg='red')   
    else:
        lbl_result.configure(text='Spam',fg='blue')
def pred_save(entry_src,entry_dest):
    srcpath=entry_src.get()
    dest_path=entry_dest.get()
    df=pd.read_csv(srcpath,names=['msg'])
    X=df.msg.map(clean_text)
    X_test=cv.transform(X).toarray()
    predict=clf.predict(X_test)
    result_df=pd.DataFrame()
    result_df['msg']=df.msg
    result_df['msg_type']=predict
    result_df.to_csv(dest_path,index=False,sep='\t')
    messagebox.showinfo('Result',"Prediction completed Sucessfully!")
def logout():
    option=messagebox.askyesno('Confirmation',"Do yo really want to logout")
    if(option==True):
        home_screen()
    else:
        pass

def home_screen():
    frm=Frame(win,bg='orange')
    frm.place(relx=0,rely=0.15,relwidth=1,relheight=1)
    user_label=Label(frm,text="Username:",font=('',20,'bold'),bg='orange')
    user_label.place(relx=.3,rely=.3)
    entry_lbl=Entry(frm,font=('',20,'bold'),bd=10)
    entry_lbl.place(relx=.42,rely=.3)
    entry_lbl.focus()
    user_pass=Label(frm,text="Password:",font=('',20,'bold'),bg='orange')
    user_pass.place(relx=.3,rely=.4)
    entry_pass=Entry(frm,font=('',20,'bold'),bd=10,show='*')
    entry_pass.place(relx=.42,rely=.4)
    btn_login=Button(frm,text="Login",command=lambda:welcome_screen(entry_lbl,entry_pass),font=('',20,'bold'),bd=10,width=10)
    btn_login.place(relx=.45,rely=.5)
    
def welcome_screen(entry_lbl=None,entry_pass=None):
    if(entry_lbl!=None or entry_pass!=None):
        user=entry_lbl.get()
        pwd=entry_pass.get()
    else:
        user="puranjai"
        pwd="thisismyyard"
    if len(user)==0 or len(pwd)==0 :
        messagebox.showwarning("validation","Please fill both the fields")
        return
    else:
      if(user=="puranjai" and pwd=="thisismyyard"):
        frm=Frame(win,bg='orange')
        frm.place(relx=0,rely=.15,relwidth=1,relheight=1)
        btn_single=Button(frm,command=lambda:single_feedback_screen(),text="Single Feedback Prediction",font=('',20,'bold'),bd=10,width=25)
        btn_single.place(relx=.35,rely=.2)

        btn_bulk=Button(frm,command=lambda:bulk_feedback_screen(),text="Bulk Feedback Prediction",font=('',20,'bold'),bd=10,width=25)
        btn_bulk.place(relx=.35,rely=.4)
        btn_logout=Button(frm,command=lambda:logout(),text="Logout",font=('',20,'bold'),bd=10)
        btn_logout.place(relx=.9,rely=0)
      else:
        messagebox.showerror('Fail',"Invalid username or password")
        
def single_feedback_screen():
    frm=Frame(win,bg='orange')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=1)
    lbl_feedback=Label(frm,text="Enter Feedback:",font=('',20,'bold'),bg='orange')
    lbl_feedback.place(relx=.25,rely=.35)
    entry_feedback=Entry(frm,font=('',20,'bold'),bd=10)
    entry_feedback.place(relx=.43,rely=.35)
    entry_feedback.focus()
    btn_predict=Button(frm,command=lambda:singlepred(entry_feedback,lbl_result),text="Predict",font=('',20,'bold'),bg='white')
    btn_predict.place(relx=.4,rely=.48)
    lbl_result=Label(frm,text="Prediction:",font=('',20,'bold'),bg='orange')
    lbl_result.place(relx=.25,rely=.58)
    back_btn=Button(frm,command=lambda:welcome_screen(),text="Back",font=('',20,'bold'),bd=10)
    back_btn.place(relx=.9,rely=0)
    
def bulk_feedback_screen():
     frm=Frame(win,bg='orange')
     frm.place(relx=0,rely=.15,relwidth=1,relheight=1)
     lbl_src=Label(frm,text="Select Source file:",font=('',20,'bold'),bg='orange')
     lbl_src.place(relx=.28,rely=.2)
     lbl_dest=Label(frm,text="Select Destination file:",font=('',20,'bold'),bg='orange')
     lbl_dest.place(relx=.28,rely=.6)
     entry_src=Entry(frm,font=('',20,'bold'),bd=10)
     entry_src.place(relx=.48,rely=.2)
     entry_src.focus()
     entry_dest=Entry(frm,font=('',20,'bold'),bd=10) 
     entry_dest.place(relx=.5,rely=.6)
     entry_dest.focus() 
     btn_browse1=Button(frm,command=lambda:browse1(entry_src),text="Browse",font=('',20,'bold'),bd=10,width=7)
     btn_browse1.place(relx=.74,rely=.2)   
     btn_browse2=Button(frm,command=lambda:browse2(entry_dest),text="Browse",font=('',20,'bold'),bd=10,width=7)
     btn_browse2.place(relx=.75,rely=.6)   
     btn_predict=Button(frm,command=lambda:pred_save(entry_src,entry_dest),text="Predict & Save",font=('',20,'bold'),bd=10,width=14)
     btn_predict.place(relx=.47,rely=.35)
     
     btn_back=Button(frm,command=lambda:welcome_screen(),text="Back",font=('',20,'bold'),bg='white')   
     btn_back.place(relx=.9,rely=0)
def browse1(entry_path):
    filepath=filedialog.askopenfilename()
    entry_path.delete(0,END)
    entry_path.insert(0,filepath)
def browse2(entry_path):
    filepath=filedialog.askdirectory()+"/result.txt"
    entry_path.delete(0,END)
    entry_path.insert(0,filepath)
    
    
home_screen()    
win.mainloop()

