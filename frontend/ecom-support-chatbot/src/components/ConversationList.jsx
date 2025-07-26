import { useEffect, useState } from "react";
import axios from "axios";
import { useChat } from "../context/ChatContext";

export default function ConversationList() {
  const [conversations, setConversations] = useState([]);
  const { setMessages, setConversationId } = useChat();

  useEffect(() => {
    fetchConversations();
  }, []);

  const fetchConversations = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:8000/api/conversations");
      setConversations(res.data);
    } catch (err) {
      console.error("Failed to fetch conversations", err);
    }
  };

  const handleClick = async (id) => {
    try {
      const res = await axios.get(`http://127.0.0.1:8000/api/conversations/${id}`);
      const messages = res.data.map((m) => ({
        sender: m.sender,
        content: m.content,
      }));

      setMessages(messages);
      setConversationId(id);
    } catch (err) {
      console.error("Failed to load conversation", err);
    }
  };

  const handleNewChat = async () => {
    try {
      const res = await axios.post("http://127.0.0.1:8000/api/chat", {
        user_id: 1,
        message: "Hi, I need help with my order.", // ✅ send truly empty string
      });
  
      const newId = res.data.conversation_id;
  
      setConversationId(newId);
      setMessages([]); // ✅ don't assume there's any message yet
  
      fetchConversations();
    } catch (err) {
      console.error("Failed to start new chat", err);
    }
  };
  

  return (
    <div style={styles.panel}>
      <h3 style={styles.title}>Past Conversations</h3>
      <button onClick={handleNewChat} style={styles.newChatButton}>➕ Start New Chat</button>
      {[...conversations]
        .sort((a, b) => b.id - a.id) 
        .map((c) => (
            <div key={c.id} style={styles.item} onClick={() => handleClick(c.id)}>
            Conversation #{c.id}
            </div>
        ))}
    </div>
  );
}

const styles = {
  panel: {
    width: "250px",
    padding: "10px",
    borderRight: "1px solid #ccc",
    overflowY: "auto",
  },
  title: {
    marginBottom: "10px",
  },
  newChatButton: {
    width: "100%",
    padding: "8px",
    marginBottom: "10px",
    backgroundColor: "#007bff",
    color: "white",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
  },
  item: {
    padding: "8px",
    cursor: "pointer",
    backgroundColor: "#f5f5f5",
    marginBottom: "5px",
    borderRadius: "4px",
  },
};
