// src/components/Message.jsx
export default function Message({ sender, content }) {
    const isUser = sender === "user";
  
    return (
      <div style={{ ...styles.msg, alignSelf: isUser ? "flex-end" : "flex-start", backgroundColor: isUser ? "#dcf8c6" : "#fff" }}>
        <strong>{isUser ? "You" : "Bot"}:</strong> {content}
      </div>
    );
  }
  
  const styles = {
    msg: {
      maxWidth: "80%",
      padding: "10px",
      marginBottom: "10px",
      borderRadius: "10px",
      boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
    },
  };
  