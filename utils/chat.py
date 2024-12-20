

from chats.engine import Engine
from utils.db import get_chunks


import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

from langchain_core.prompts import PromptTemplate

template="""
Textbook Chapter:
{chapter_content}

Question:
{question}

Instruction:
Using the information provided in the textbook chapter, answer the question as accurately as possible. If the chapter content is not relevant to answering the question, provide an accurate and concise answer based on general knowledge instead. If unsure, answer to the best of your ability using available context.

Answer:
"""


Base_Template = PromptTemplate(
    input_variables=['chapter_content','question'],
    template=template)

def get_context(chapter: list, question: str) -> str:
    """
    This function takes the entire chapter content (in a list of sections)
    and the question as input, calculates text similarity, and returns 
    the most relevant context from the chapter.

    Args:
        chapter (list): List of strings, where each string represents a section of the chapter.
        question (str): The question to match with the chapter content.

    Returns:
        str: The most relevant section of the chapter based on similarity.
    """
    # Encode the chapter sections and the question into embeddings
    chapter_embeddings = model.encode(chapter, convert_to_tensor=True)
    question_embedding = model.encode([question], convert_to_tensor=True)

    # Move embeddings to CPU if using MPS or GPU
    chapter_embeddings = chapter_embeddings.cpu().numpy()
    question_embedding = question_embedding.cpu().numpy()

    # Calculate cosine similarity
    similarities = cosine_similarity(question_embedding, chapter_embeddings)

    # Find the index of the most relevant section
    most_relevant_index = np.argmax(similarities)
    return chapter[most_relevant_index]

obj = None

def init_chat():
    global obj  
    obj = Engine()

def is_ready():
    return obj.is_ready()

def get_response(prev_chats, prompt: str, chat_id: int):
    """
    Generate a response to the user's question by extracting relevant context
    and querying the chat engine.

    Args:
        prev_chats (list): List of previous chat messages.
        prompt (str): The user's question or prompt.
        chat_id (int): The chat session ID.

    Returns:
        str: The response generated by the chat engine.
    """
    # Retrieve all chunks for the given chat_id
    chapter = []
    for chunk in get_chunks(chat_id):
        chapter.append(chunk.content)
    
    # Get the most relevant context
    context = get_context(chapter, prompt)  # Avoid overwriting the function name
    
    # Format the prompt using the template
    prompt_template = Base_Template.format(chapter_content=context, question=prompt)

    # Get the response from the engine
    response = obj.get_response(prompt_template, prev_chats)
    return response
