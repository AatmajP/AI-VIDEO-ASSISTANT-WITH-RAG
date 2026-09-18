from dotenv import load_dotenv

load_dotenv()  # MUST be before any core/ imports
from langchain_groq import ChatGroq # used groq
model = ChatGroq(model="openai/gpt-oss-0b")
response = model.invoke("full form of irctc") #we can also use the model.invoke_async() method to get the response asynchronously
print(response.content)