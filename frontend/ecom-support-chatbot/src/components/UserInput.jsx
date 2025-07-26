// src/components/UserInput.jsx
import { useState } from "react";
import { useChat } from "../context/ChatContext";
import axios from "axios";

export default function UserInput() {
  const [text, setText] = useState("");
  const {
    messages,
    setMessages,
    setLoading,
    conversationId,
  } = useChat(); // ✅ Now using conversationId from context

  const sendMessage = async () => {
    if (!text.trim()) return;

    if (!conversationId) {
      alert("Please start or select a conversation.");
      return;
    }

    const newMsg = { sender: "user", content: text };
    setMessages([...messages, newMsg]);
    setText("");
    setLoading(true);

    try {
      const response = await axios.post("http://127.0.0.1:8000/api/chat", {
        user_id: 1,
        message: text,
        conversation_id: conversationId, // ✅ Now dynamic
      });

      const aiMsg = {
        sender: "ai",
        content: response.data.ai_message,
      };

      setMessages((prev) => [...prev, aiMsg]);
    } catch (err) {
      console.error("❌ Failed to send message:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.inputBox}>
      <input
        type="text"
        placeholder="Ask something..."
        value={text}
        onChange={(e) => setText(e.target.value)}
        style={styles.input}
        onKeyDown={(e) => e.key === "Enter" && sendMessage()}
      />
      <button onClick={sendMessage} style={styles.button}>
        Send
      </button>
    </div>
  );
}

const styles = {
  inputBox: {
    display: "flex",
    borderTop: "1px solid #ccc",
    padding: "10px",
  },
  input: {
    flex: 1,
    padding: "8px",
    borderRadius: "4px",
    border: "1px solid #ccc",
    marginRight: "10px",
  },
  button: {
    padding: "8px 12px",
    backgroundColor: "#282c34",
    color: "white",
    border: "none",
    borderRadius: "4px",
  },
}; //complete
