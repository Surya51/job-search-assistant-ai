from flask import Blueprint, current_app, g, jsonify, request

from langchain_community.document_loaders import PyPDFLoader
from langchain_google_community import GCSFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnableParallel
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate

from assistant.db import get_assessment_data_by_guid, save_user_responses
from assistant.utils import get_token_data

assess_bp = Blueprint("assess", __name__, url_prefix='/assess')

@assess_bp.route('/generate/<assessment_guid>', methods=['POST'])
def generate_questions(assessment_guid):
  token_data = get_token_data(True)
  if(not token_data.get('success')):
    return jsonify(token_data), 401

  success, questions, error = _generate_questions_from_assessment(assessment_guid)

  if not success:
    return jsonify({'success': False, 'error': error}), 400

  return jsonify({'success': True, 'data': questions}), 200

@assess_bp.route('/submit-assessment/<assessment_guid>', methods=['POST'])
def submit_assessment_data(assessment_guid):
  token_data = get_token_data(True)
  if(not token_data.get('success')):
    return jsonify(token_data), 401

  data = request.json
  isContinue = data.get("isContinue")
  qnas = data.get("qnas")

  if qnas is not None:
    save_user_responses(assessment_guid, qnas)

  if isContinue:
    success, questions, error = _generate_questions_from_assessment(assessment_guid)
    if not success:
      return jsonify({'success': False, 'error': error}), 400
    return jsonify({'success': True, 'data': questions}), 200

  return jsonify({'success': True, 'data': None}), 200

def _getChain():
  # This is a sample model from the models of huggingface,
  # there are more models to this and also we can prepare our own model in huggingface if required.
  llm = HuggingFaceEndpoint(
    repo_id="microsoft/Phi-3-mini-4k-instruct",
    task="text-generation",
    max_new_tokens=2048,
    truncate=None,
    return_full_text=True,
    huggingfacehub_api_token = current_app.config.get("ACCESS_TOKEN")
  )

  model = ChatHuggingFace(llm=llm,verbose=True)

  parser = StrOutputParser()

  prompt_template = """
    Based on the provided resume and job description, ask one question directly about the candidate's qualifications or experiences from the resume
    and another question directly about their suitability for the role from the job description.
    Only ask the questions without adding any additional context.
    Do not give additional info like 'From the resume' or 'based on the job description' or 'from the job description' or 'Direct questions'.
    resume_context: {resume_context}
    job_description: {job_description}
  """

  prompt = PromptTemplate.from_template(prompt_template)

  chain = prompt | model | parser

  return chain

def _generate_questions_from_assessment(assessment_guid):
  assessment = get_assessment_data_by_guid(assessment_guid)

  if assessment is None:
    return False, None, 'No assessment found.',
  
  file_path = assessment['file_path']
  jobDesc = assessment['job_description']

  questions_text = runnable = None

  try:
    chain = _getChain()
    if g.get('runnable') is not None and g.get('file_path') == file_path:
      runnable = g.runnable
    if(runnable is None):
      runnable = _loadPDFData(file_path)

    questions_text = chain.invoke({
      'resume_context': runnable,
      'job_description': jobDesc
    })
  except Exception as e:
    return False, None, f'Error while generating questions. {e}'
  
  questions = [line for line in questions_text.split('\n') if line.strip() != '']

  return True, questions, None

def _loadPDFData(file_path):
  bucket_name = current_app.config.get('CLOUD_STORAGE_BUCKET')

  project_name = current_app.config.get('CLOUD_PROJECT_NAME')

  file_loader = GCSFileLoader(
    project_name=project_name, bucket=bucket_name, blob=file_path, loader_func=_load_pdf
  )

  page = file_loader.load_and_split()

  splitter = RecursiveCharacterTextSplitter(chunk_size=100,chunk_overlap=20)
  pages = splitter.split_documents(page)

  embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

  vector_storage = FAISS.from_documents(pages, embeddings_model)
  retriever = vector_storage.as_retriever()

  g.file_path = file_path
  runnable = RunnableParallel(resume_context = retriever)
  g.runnable = runnable
  return runnable

def _load_pdf(file_path):
    return PyPDFLoader(file_path)