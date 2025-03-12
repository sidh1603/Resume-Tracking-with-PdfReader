import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
import io
import base64
import PyPDF2 as pdf
from PyPDF2 import PdfReader

api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key = api_key)

def get_gemini_response(input, pdf_content,prompt):
    model =genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    """Extracts text from a PDF file."""
    text = ""
    reader = PdfReader(uploaded_file)
    
    for page in reader.pages: 
        text += page.extract_text() or ""  
    return text

##prompt_template



def main():
    st.set_page_config(page_title="ATS Resume Expert", page_icon="🦜")
    st.header("ATS Tracking System with PyReader")
    jd = st.text_area("JOb Description", key="input")
    uploaded_file = st.file_uploader("Upload your Resume", type=["pdf"])

    
    submit1 = st.button("🔍 Evaluate Resume")
    submit2 = st.button("📈 Improve Skills")
    submit3 = st.button("🔑 Identify Missing Keywords")
    submit4 = st.button("📊 Percentage Match Analysis")

    input_prompt1 ="""
    Hey act like a very skilled or ATS(application tracking system) with deep understanding of Tech field of Data Science , 
    Full Stack Developer , Devops , Data Engineering , Data Analyst and big data engineer.Your task is to evaluate the resume based
    on the job description and you must consider the job market is very competitive and you should provide the best assistance
    for improving the resume.Assign the percentage matching based on the jd and the missing keywords with high accuracy
    resume: {text}
    description: {jd}
    
    I want the response in one single string having the structure {{"JD match":"%","MissingKeywords:[]","Profile Summary: "}} 
    """

    input_prompt2 = """
     You are an Technical HUman REsource Manager with experience in  field of any one job role from Data Science , 
     Full Stack Developer,data Engineer,Devops , Data Analyst
     your role is to scruntinize the resume in the light of the job description provided.
     share your insights on the candidate's suitability for the role from an HR perspective,
     Additionally , offer advice on enhancing the candidate skills and identify  areas.
    """

    input_prompt3 = """  Youa re skilled ATS(Applicantion TRacking System) scanner with deep understanding of data science,
    , Full Stack Developer,data Engineer,Devops , Data Analyst and deep ATS functionality ,  your task is to evaluate the resume against the provided 
    job description and give me the percentage of match if the candidate's resume matches with 
    the job description. First the output should come as percentage and then keywords missing and final last thoughts"""

    input_prompt4 = """  
    You are a **highly advanced ATS system** that calculates the **percentage match**
    between a candidate's resume and the job description.
    
    - First, provide a **match percentage** (out of 100%).
    - Then, list the **missing skills and keywords** that could improve the match.
    - Finally, summarize the **strengths and weaknesses** of the resume in relation to the job.

    🎯 **Example Response Format:**
    - **Match Score:** 75%
    - **Missing Keywords:** SQL, Docker, Cloud Computing
    - **Strengths:** Strong Python skills, solid experience in Data Analysis
    - **Weaknesses:** Lacks exposure to cloud platforms, no DevOps experience
    """






    
    if submit1 or submit2 or submit3 or submit4:
        if uploaded_file is not None:
            pdf_content = input_pdf_setup(uploaded_file)

            if submit1:
                response = get_gemini_response(input_prompt1, pdf_content, jd)
                st.subheader("📄 Resume Evaluation:")
                st.write(response)

            elif submit2:
                response = get_gemini_response(input_prompt2, pdf_content, jd)
                st.subheader("📈 Skill Improvement Suggestions:")
                st.write(response)

            elif submit3:
                response = get_gemini_response(input_prompt3, pdf_content, jd)
                st.subheader("🔑 Missing Keywords Analysis:")
                st.write(response)

            elif submit4:
                response = get_gemini_response(input_prompt4, pdf_content, jd)
                st.subheader("📊 Percentage Match & Resume Analysis:")
                st.write(response)

        else:
            st.error("⚠️ Please upload your resume before proceeding.")



if __name__ == "__main__":
    main()


    

