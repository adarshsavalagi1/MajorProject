import sqlite3
from collections import namedtuple
from typing import Dict

# Named Tuples for structured query results
Chat = namedtuple("Chat", ["id", "name", "textbook_path", "pages"])
Chunk = namedtuple("Chunk", ["id", "chat_ref", "page_start", "page_end", "content", "chapter_name", "chapter_number"])

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn


CREATE_CHUNK_TABLE = """
CREATE TABLE IF NOT EXISTS chunk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_ref INTEGER NOT NULL,
    page_start INTEGER NOT NULL,
    page_end INTEGER NOT NULL,
    content TEXT NOT NULL,
    chapter_name TEXT NOT NULL,
    chapter_number INTEGER NOT NULL,
    FOREIGN KEY (chat_ref) REFERENCES chat (id) ON DELETE CASCADE
);
"""

CREATE_CHAT_TABLE = """
CREATE TABLE IF NOT EXISTS chat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    textbook_path VARCHAR(255) NOT NULL,
    pages INTEGER NOT NULL
);
"""

CREATE_MESSAGE_TABLE = """
CREATE TABLE IF NOT EXISTS message (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_ref INTEGER NOT NULL,
    prompt TEXT NOT NULL,
    response TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chat_ref) REFERENCES chat (id) ON DELETE CASCADE
);
"""

def init_db():
    conn = create_connection("db.sqlite")
    if conn is not None:
        c = conn.cursor()
        c.execute(CREATE_CHAT_TABLE)
        c.execute(CREATE_CHUNK_TABLE)
        c.execute(CREATE_MESSAGE_TABLE)
        conn.commit()
        conn.close()
    else:
        print("Error! cannot create the database connection.")

def insert_chat(name, textbook_path, pages):
    """
    Insert a chat record into the database and return its ID.
    Args:
        name (str): Name of the chat session.
        textbook_path (str): Path to the textbook.
        pages (str): Pages related to the chat.

    Returns:
        int: ID of the inserted row or None if failed.
    """
    conn = create_connection("db.sqlite")
    if conn is not None:
        try:
            c = conn.cursor()
            # Perform the insert
            c.execute("INSERT INTO chat (name, textbook_path, pages) VALUES (?, ?, ?)", (name, textbook_path, pages))
            conn.commit()
            # Get the ID of the inserted row
            inserted_id = c.lastrowid
            conn.close()
            return inserted_id
        except sqlite3.Error as e:
            print(f"Error inserting data: {e}")
            conn.close()
            return None
    else:
        print("Error! cannot create the database connection.")
        return None

def insert_chunk(chat_ref, page_start, page_end, content, chapter_name, chapter_number):
    conn = create_connection("db.sqlite")
    if conn is not None:
        c = conn.cursor()
        c.execute("INSERT INTO chunk (chat_ref, page_start, page_end, content, chapter_name, chapter_number) VALUES (?, ?, ?, ?, ?, ?)",
                  (chat_ref, page_start, page_end, content, chapter_name, chapter_number))
        conn.commit()
        conn.close()
    else:
        print("Error! cannot create the database connection.")

def get_chat(chat_id):
    conn = create_connection("db.sqlite")
    if conn:
        c = conn.cursor()
        c.execute("SELECT * FROM chat WHERE id = ?", (chat_id,))
        chat_row = c.fetchone()
        conn.close()
        if chat_row:
            return Chat(*chat_row)  # Return as named tuple
        return None
    else:
        print("Error! cannot create the database connection.")
        return None

def get_chunks(chat_id):
    conn = create_connection("db.sqlite")
    if conn:
        c = conn.cursor()
        c.execute("SELECT * FROM chunk WHERE chat_ref = ?", (chat_id,))
        chunk_rows = c.fetchall()
        conn.close()
        return [Chunk(*row) for row in chunk_rows]  # Return as list of named tuples
    else:
        print("Error! cannot create the database connection.")
        return []

def get_chunk(chunk_id):
    conn = create_connection("db.sqlite")
    if conn:
        c = conn.cursor()
        c.execute("SELECT * FROM chunk WHERE id = ?", (chunk_id,))
        chunk_row = c.fetchone()
        conn.close()
        if chunk_row:
            return Chunk(*chunk_row)  # Return as named tuple
        return None
    else:
        print("Error! cannot create the database connection.")
        return None

def get_all_chunks():
    conn = create_connection("db.sqlite")
    if conn:
        c = conn.cursor()
        c.execute("SELECT * FROM chunk")
        chunk_rows = c.fetchall()
        conn.close()
        return [Chunk(*row) for row in chunk_rows]  # Return as named tuples
    else:
        print("Error! cannot create the database connection.")
        return []

def get_all_chats():
    """
    Fetch all chats and their associated messages from the database and return them as JSON.
    """
    conn = create_connection("db.sqlite")
    if conn:
        try:
            c = conn.cursor()
            
            # Fetch all chats
            c.execute("SELECT * FROM chat")
            chat_rows = c.fetchall()
            
            # Prepare a list to hold all data to return
            all_chats = []
            
            # Loop through all chat sessions
            for chat in chat_rows:
                chat_id = chat[0]
                
                # Fetch messages associated with the current chat_id
                c.execute("SELECT * FROM message WHERE chat_ref = ?", (chat_id,))
                message_rows = c.fetchall()
                
                # Map message data into a list of dictionaries
                messages = [
                    {
                        "id": msg[0],
                        "chat_ref": msg[1],
                        "prompt": msg[2],
                        "response": msg[3],
                        "timestamp": msg[4],
                    }
                    for msg in message_rows
                ]
                
                # Combine chat data with its messages
                all_chats.append({
                    "id": chat[0],
                    "name": chat[1],
                    "textbook_path": chat[2],
                    "pages": chat[3],
                    "messages": messages,
                })

            conn.close()
            return all_chats
            
        except Exception as e:
            print(f"Error fetching data: {e}")
            raise e
    else:
        print("Error! cannot create the database connection.")
        raise Exception("Database connection error")

def delete_chat(chat_id):

    conn = create_connection("db.sqlite")
    if conn:
        c = conn.cursor()
        c.execute("DELETE FROM chat WHERE id = ?", (chat_id,))
        conn.commit()
        conn.close()
    else:
        print("Error! cannot create the database connection.")
        raise Exception("Database connection error")
    


def insert_message(chat_ref, prompt, response):
    conn = create_connection("db.sqlite")
    if conn is not None:
        c = conn.cursor()
        c.execute("INSERT INTO message (chat_ref, prompt, response) VALUES (?, ?, ?)", (chat_ref, prompt, response))
        conn.commit()
        conn.close()
    else:
        print("Error! cannot create the database connection.")


def get_all_message(id: int):
    conn = create_connection("db.sqlite")
    if conn:
        c = conn.cursor()
        c.execute("SELECT * FROM message WHERE chat_ref = ?", (id,))
        message_rows = c.fetchall()
        conn.close()
        return message_rows
    else:
        print("Error! cannot create the database connection.")
        return []

def get_data(id: int) -> Dict:
    """
    Fetches previous chat responses and textbook path from the database
    based on the provided chat id.

    Args:
        id (int): The ID of the chat session.

    Returns:
        Dict: A JSON-like dictionary containing chat responses, textbook path, and all params.
    """
    conn = create_connection("db.sqlite")
    if conn is None:
        raise Exception("Failed to connect to the database")

    try:
        # Query the textbook path from the 'chat' table
        chat_cursor = conn.cursor()
        chat_cursor.execute("SELECT textbook_path FROM chat WHERE id = ?", (id,))
        chat_row = chat_cursor.fetchone()
        if chat_row is None:
            raise ValueError("Chat ID not found in database")

        textbook_path = chat_row[0]

        # Query all responses from the 'message' table related to this chat
        message_cursor = conn.cursor()
        message_cursor.execute(
            "SELECT prompt, response, timestamp FROM message WHERE chat_ref = ? ORDER BY timestamp",
            (id,),
        )
        messages = message_cursor.fetchall()

        # Map fetched messages to a list of dictionaries
        previous_responses = [
            {"prompt": msg[0], "response": msg[1], "timestamp": msg[2]} for msg in messages
        ]

        # Close database connection
        conn.close()

        # Combine data into a single JSON-like response
        response_data = {
            "textbook_path": textbook_path,
            "previous_responses": previous_responses,
            "chat_id": id,
        }

        return response_data

    except Exception as e:
        print(f"Error during query: {e}")
        conn.close()
        return {"error": str(e)}