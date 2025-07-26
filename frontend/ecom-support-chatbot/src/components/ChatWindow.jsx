import MessageList from "./MessageList";
import UserInput from "./UserInput";
import ConversationList from "./ConversationList";

export default function ChatWindow() {
  return (
    <div style={styles.wrapper}>
      <ConversationList />
      <div style={styles.chatContainer}>
        <h2 style={styles.header}>🛍️ E-Commerce Support Chat</h2>
        <MessageList />
        <UserInput />
      </div>
    </div>
  );
}

const styles = {
  wrapper: {
    display: "flex",
    height: "80vh",
    width: "90%",
    margin: "20px auto",
    border: "1px solid #ccc",
    borderRadius: "8px",
    overflow: "hidden",
  },
  chatContainer: {
    flex: 1,
    display: "flex",
    flexDirection: "column",
  },
  header: {
    padding: "10px",
    backgroundColor: "#282c34",
    color: "white",
    margin: 0,
  },
};
