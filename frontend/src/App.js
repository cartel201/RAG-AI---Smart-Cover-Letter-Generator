import { useState } from 'react';
import Upload from './components/Upload';
import Chat from './components/Chat';
import CoverLetter from './components/CoverLetter';

function App() {
  return (
    <div className="dark bg-gray-900 text-white min-h-screen">
      <h1 className="text-3xl font-bold text-center">Career Assistant</h1>
      {/* <Upload />
      <Chat /> */}
      <CoverLetter />
    </div>
  );
}

export default App;
