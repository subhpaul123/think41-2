// src/components/ChatWindow.jsx
import MessageList from "./MessageList";
import UserInput from "./UserInput";

export default function ChatWindow() {
  return (
    <div style={styles.chatContainer}>
      <h2 style={styles.header}>🛍️ E-Commerce Support Chat</h2>
      <MessageList />
      <UserInput />
    </div>
  );
}

const styles = {
  chatContainer: {
    width: "400px",
    margin: "20px auto",
    border: "1px solid #ccc",
    borderRadius: "8px",
    display: "flex",
    flexDirection: "column",
    height: "80vh",
    overflow: "hidden",
    fontFamily: "sans-serif",
  },
  header: {
    padding: "10px",
    backgroundColor: "#282c34",
    color: "white",
    margin: 0,
  },
};
