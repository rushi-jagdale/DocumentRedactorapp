import streamlit as st 
import os,base64

#NLP PKG
import spacy
from spacy import displacy

nlp  = spacy.load("en_core_web_sm")

#Time PKG
import time
timestr = time.strftime("%Y%m%d-%H%M%S")
# Templates

HTML_WRAPPER = """<div style="overflow-x:auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>
"""
file_name = 'yourdocument' + timestr + '.txt'
#function to Sanitize and Redact
# def sanitize_names(text):
#     doc = nlp(text)
#     with doc.retokenize() as retokenizer:
#         for ent in doc.ents:
#             retokenizer.merge(ent)
#     tokens = map(replace_name_with_placeholder, doc)
#     return " ".join(tokens)
def sanitize_names(text):

    empty_space = []
    doc = nlp(text)
    for new in doc:
        if new.ent_type_ == 'PERSON':
            empty_space.append('[Redacted]')
        else:
            empty_space.append(new)
    return ' '.join(map(str,empty_space))

def sanitize_places(text):
    empty_space = []
    doc = nlp(text)
    for new in doc:
        if new.ent_type_ == 'GPE':
            empty_space.append('[Redacted]')
        else:
            empty_space.append(new)
    return ' '.join(map(str,empty_space))

def sanitize_org(text):
    empty_space = []
    doc = nlp(text)
    for new in doc:
        if new.ent_type_ == 'ORG':
            empty_space.append('[Redacted]')
        else:
            empty_space.append(new)
    return ' '.join(map(str,empty_space))

def sanitize_date(text):
    empty_space = []
    doc = nlp(text)
    for new in doc:
        if new.ent_type_ == 'DATE':
            empty_space.append('[Redacted]')
        else:
            empty_space.append(new)
    return ' '.join(map(str,empty_space))


    #         if token.ent_type =='GPE':
    #             redacted_sentences.append("[REDACTED NAME]") 
    #         else:
    #             redacted_sentences.append(token.text)
    #     return "".join(redacted_sentences)        


# def replace_name_with_placeholder(token):
#      if token.ent_iob != 0 and token.ent_type_ == "PERSON":
#          return "[REDACTED] "
#      else:
#          return token.text  


# Function display Entities

def render_entities(rawtext):
    docx = nlp(rawtext)
    html = displacy.render(docx,style='ent')
    html = html.replace("\n\n","\n")
    result = HTML_WRAPPER.format(html)
    return result   

#function to write
def writetofile(text,filename):
    with open(os.path.join("downloads",filename),"w") as f:
        f.write(text)
    return filename    

# Download file
def make_downloadable(filename):

    readfile = open(os.path.join("downloads",filename)).read()
    b64 = base64.b64encode(readfile.encode()).decode()
    #st.write(readfile)
    href = '<a href="data:file/readfile;base64,{}">Download File</a>(right click to save as file name)'.format(b64)
    return href

    # docx = nlp(text)
    # redacted_sentences = []
    # with docx.retokenize() as retokenizer:
    #     for ent in docx.ents:
    #        retokenizer.merge(ent)

            
    #     for token in docx:
    #         if token.ent_type =='GPE':
    #             redacted_sentences.append("[REDACTED NAME]") 
    #         else:
    #             redacted_sentences.append(token.text)
    #     return "".join(redacted_sentences)        





def main():

    st.title("Document Redactor app")
    st.text("Built with Streamlit and Spacy")
    activities = ["Redaction","Downloads","About"]

    choice = st.sidebar.selectbox("Select Task",activities)

    if choice == "Redaction":
        
        st.subheader("Redaction of Terms")
        rawtext = st.text_area("Enter Text","")
        redaction_item = ["names","places","org","dates"]
        redaction_choice = st.selectbox("Select Term to censor",redaction_item)
        save_option = st.radio("Save To File ",("Yes","No"))
        if st.button("submit"):
            if save_option == 'Yes':

                if redaction_choice =='names':
                    result = sanitize_names(rawtext)
            
                elif redaction_choice =='places': 
                    result = sanitize_places(rawtext)
            
                elif redaction_choice =='org': 
                    result = sanitize_org(rawtext)

                elif redaction_choice =='dates': 
                    result = sanitize_date(rawtext)
            
                st.subheader("Original Text")
                st.write(render_entities(rawtext),unsafe_allow_html=True)   

                st.subheader("Redacted Text") 
                st.write(result)
                
                file_to_download = writetofile(result,file_name)
                st.info("Saved Result as :: {}".format(file_name))
                d_link = make_downloadable(file_to_download)
                
                st.markdown(d_link,unsafe_allow_html=True)
 
                   
    elif choice == "Downloads":
          st.subheader("Downloads List")
          files = os.listdir(os.path.join('downloads'))
          file_to_download = st.selectbox("Select A file ",files)
          st.info("File Name :: {}".format(file_to_download))
          d_link = make_downloadable(file_to_download)
          st.markdown(d_link,unsafe_allow_html=True)



    elif choice == "About":
        st.subheader("About")
        st.text("Rushi @awesomestreamlit.org")




if __name__ == "__main__":

    main()    