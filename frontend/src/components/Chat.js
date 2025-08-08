import { useState } from "react";
import axios from "axios";

export default function Chat() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const handleAsk = async () => {
    if (!question.trim()) return;
    try {
      const res = await axios.post("/api/chat", {
        user_id: "default",
        question,
      });
      setAnswer(res.data.answer);
    } catch (err) {
      console.error(err);
      setAnswer("❌ Failed to fetch answer.");
    }
  };

  return (
    <div className="bg-white p-6 rounded shadow space-y-3">
      <h2 className="text-2xl font-semibold">💬 Ask a Question</h2>
      <input
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && handleAsk()}
        placeholder="e.g., What are my top skills?"
        className="w-full p-2 border rounded"
      />
      <button
        onClick={handleAsk}
        className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
      >
        Ask
      </button>
      {answer && (
        <div className="bg-gray-100 p-3 rounded whitespace-pre-wrap">{answer}</div>
      )}
    </div>
  );
}
