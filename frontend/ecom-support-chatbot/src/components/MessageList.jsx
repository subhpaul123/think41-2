// src/components/MessageList.jsx
import { useChat } from "../context/ChatContext";
import Message from "./Message";

export default function MessageList() {
  const { messages } = useChat();

  return (
    <div style={styles.list}>
      {messages.map((msg, idx) => (
        <Message key={idx} sender={msg.sender} content={msg.content} />
      ))}
    </div>
  );
}

const styles = {
  list: {
    flex: 1,
    padding: "10px",
    overflowY: "auto",
    backgroundColor: "#f7f7f7",
  },
};
