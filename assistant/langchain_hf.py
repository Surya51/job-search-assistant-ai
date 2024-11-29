from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate

def init_langchain(app):
  # This is a sample model from the models of huggingface,
  # there are more models to this and also we can prepare our own model in huggingface if required.
  llm = HuggingFaceEndpoint(
    repo_id="microsoft/Phi-3-mini-4k-instruct",
    task="text-generation",
    max_new_tokens=2048,
    truncate=None,
    return_full_text=True,
    huggingfacehub_api_token = app.config.get("ACCESS_TOKEN")
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

  app.chain = prompt | model | parser