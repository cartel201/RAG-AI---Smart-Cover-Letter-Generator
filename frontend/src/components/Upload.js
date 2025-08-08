import { useState } from 'react';
import axios from 'axios';

export default function Upload() {
  const [file, setFile] = useState(null);
  const [userId, setUserId] = useState("madhup");
  const [message, setMessage] = useState("");

  const handleUpload = async () => {
    if (!file) return setMessage("❗ Please select a PDF file.");
    const formData = new FormData();
    formData.append("file", file);
    formData.append("user_id", userId);

    try {
      const res = await axios.post("http://localhost:8000/api/upload-resume", formData);
      setMessage(`✅ ${res.data.message || "Uploaded successfully"}`);
    } catch (err) {
      console.error(err);
      setMessage("❌ Upload failed.");
    }
  };

  return (
    <div className="bg-white p-6 rounded shadow">
      <h2 className="text-2xl font-semibold mb-4">📄 Upload Resume</h2>
      <input
        type="text"
        value={userId}
        onChange={(e) => setUserId(e.target.value)}
        className="mb-3 w-full p-2 border rounded"
        placeholder="Enter User ID"
      />
      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
        accept="application/pdf"
        className="mb-3 w-full"
      />
      <button
        onClick={handleUpload}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 w-full"
      >
        Upload
      </button>
      {message && (
        <div className="mt-3 p-2 text-sm bg-gray-100 rounded">{message}</div>
      )}
    </div>
  );
}
