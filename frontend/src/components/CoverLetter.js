import { useState, useRef } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { ClipboardCopy, Loader2 } from 'lucide-react';

export default function CoverLetterForm() {
  const [resumeFile, setResumeFile] = useState(null);
  const [resumeMeta, setResumeMeta] = useState({});
  const [jobDesc, setJobDesc] = useState('');
  const [tone, setTone] = useState('formal');
  const [letter, setLetter] = useState('');
  const [message, setMessage] = useState('');
  const [copied, setCopied] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [generating, setGenerating] = useState(false);

  const letterRef = useRef(null);

  const handleCopy = () => {
    if (letterRef.current) {
      navigator.clipboard.writeText(letterRef.current.innerText);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleResumeUpload = async () => {
    if (!resumeFile) {
      setMessage('❗ Please select a resume file.');
      return;
    }
    setUploading(true);
    const formData = new FormData();
    formData.append('file', resumeFile);
    formData.append('user_id', 'default');
    try {
      const res = await axios.post('http://localhost:8000/api/upload-resume', formData);
      if (res.data && res.data.metadata) {
        setResumeMeta(res.data.metadata);
        setMessage('✅ Resume uploaded and metadata extracted.');
      } else {
        setMessage('❌ Failed to extract metadata from resume.');
      }
    } catch (err) {
      console.error(err);
      setMessage('❌ Error uploading resume.');
    } finally {
      setUploading(false);
    }
  };

  const handleSubmit = async () => {
    if (!jobDesc.trim()) {
      setMessage('❗ Please enter job description.');
      return;
    }
    setGenerating(true);
    try {
      const res = await axios.post('http://localhost:8000/api/cover-letter', {
        job_description: jobDesc,
        user_id: 'default',
        tone,
        metadata: resumeMeta,
      });
      if (res.data.letter) {
        const cleaned = res.data.letter.replace(/^Here( is|'s).*?:\s*/i, '');
        setLetter(cleaned);
        setMessage('✅ Letter generated successfully.');
      } else {
        setMessage(res.data.error || '❌ Unknown error.');
        setLetter('');
      }
    } catch (err) {
      console.error(err);
      setMessage('❌ Failed to generate cover letter.');
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-white transition duration-300 p-6 flex flex-col items-center justify-start">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="w-full max-w-2xl bg-gray-100 dark:bg-gray-800 rounded-2xl shadow-lg p-6"
      >
        <h1 className="text-3xl font-bold mb-6 text-center">📝 Cover Letter Generator</h1>

        <label className="block mb-2 text-sm font-medium">Upload Resume (PDF/DOCX)</label>
        <input
          type="file"
          accept=".pdf,.doc,.docx"
          onChange={(e) => setResumeFile(e.target.files[0])}
          className="w-full mb-4 p-2 border border-gray-300 rounded dark:bg-gray-700"
        />
        <button
          onClick={handleResumeUpload}
          className="w-full mb-4 px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded transition flex justify-center items-center gap-2"
          disabled={uploading}
        >
          {uploading ? (
            <>
              <Loader2 className="animate-spin h-4 w-4" />
              Uploading...
            </>
          ) : (
            'Upload Resume'
          )}
        </button>

        <label className="block mb-2 text-sm font-medium">Paste Job Description</label>
        <textarea
          rows={5}
          value={jobDesc}
          onChange={(e) => setJobDesc(e.target.value)}
          placeholder="Paste job description here..."
          className="w-full p-2 mb-4 border border-gray-300 rounded resize-none dark:bg-gray-700"
        />

        <label className="block mb-2 text-sm font-medium">Select Tone</label>
        <select
          value={tone}
          onChange={(e) => setTone(e.target.value)}
          className="w-full mb-4 p-2 border border-gray-300 rounded dark:bg-gray-700"
        >
          <option value="formal">Formal</option>
          <option value="friendly">Friendly</option>
          <option value="enthusiastic">Enthusiastic</option>
        </select>

        <button
          onClick={handleSubmit}
          className="w-full px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded transition flex items-center justify-center gap-2"
          disabled={generating}
        >
          {generating ? (
            <>
              <Loader2 className="animate-spin h-4 w-4" />
              Generating...
            </>
          ) : (
            'Generate Cover Letter'
          )}
        </button>

        {message && (
  <motion.div
    initial={{ opacity: 0, y: -20 }}
    animate={{ opacity: 1, y: 0 }}
    exit={{ opacity: 0, y: -20 }}
    transition={{ duration: 0.5 }}
    className={`fixed top-6 right-6 z-50 px-4 py-2 rounded-lg shadow-lg text-white 
      ${message.startsWith('✅') ? 'bg-green-600' : 'bg-red-600'}
    `}
  >
    {message}
  </motion.div>
)}


        {letter && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
            className="mt-6 relative p-4 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg whitespace-pre-wrap"
          >
            {/* 📋 Copy Button */}
           <motion.button
  onClick={handleCopy}
  whileTap={{ scale: 1.2, rotate: 15 }}
  className="absolute top-3 right-3 text-gray-600 dark:text-gray-300 hover:text-blue-600 transition-all"
  title="Copy letter"
>
  <motion.div
    animate={copied ? { scale: [1, 1.4, 1], rotate: [0, 20, -10, 0] } : {}}
    transition={{ duration: 0.4 }}
  >
    <ClipboardCopy className="h-5 w-5" />
  </motion.div>

  <AnimatePresence>
    {copied && (
      <motion.span
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.8 }}
        className="absolute -top-6 right-0 text-xs text-green-500 font-semibold"
      >
        Copied!
      </motion.span>
    )}
  </AnimatePresence>
</motion.button>


            {/* Letter Content */}
            <div ref={letterRef}>{letter}</div>
          </motion.div>
        )}
      </motion.div>
    </div>
  );
}
