import React, { useState, useEffect, useRef } from 'react';
import AudioRecorder from './components/AudioRecorder';

function App() {
  const [conversation, setConversation] = useState([]);
  const audioRef = useRef(null);
  const bottomRef = useRef(null);

  const handleResponse = (data) => {
    // Add new exchange to history
    setConversation(prev => [...prev, {
      id: Date.now(),
      user_text: data.user_text,
      response_text: data.response_text,
      audio_url: data.audio_url
    }]);

    if (data.audio_url) {
      const audioUrl = `http://localhost:8000${data.audio_url}`;
      if (audioRef.current) {
        audioRef.current.src = audioUrl;
        audioRef.current.play().catch(e => console.error("Audio play error", e));
      }
    }
  };

  useEffect(() => {
    // Auto-scroll to bottom on new message
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [conversation]);

  return (
    <div className="min-h-screen bg-rose-50 flex flex-col items-center font-sans text-slate-800">
      {/* Header */}
      <header className="w-full bg-white shadow-sm py-4 px-6 flex items-center justify-between sticky top-0 z-10">
        <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-pink-500 to-rose-400">
          Nour
        </h1>
        <button className="text-sm text-gray-400 hover:text-pink-500 transition-colors">
          À propos
        </button>
      </header>

      {/* Main Content: Chat History */}
      <main className="flex-1 w-full max-w-lg px-4 py-6 space-y-6 flex flex-col">

        {/* Intro only if empty */}
        {conversation.length === 0 && (
          <div className="flex-1 flex flex-col items-center justify-center text-center space-y-4 animate-fade-in-up mt-10">
            <div className="w-20 h-20 bg-pink-100 rounded-full mx-auto flex items-center justify-center text-4xl shadow-inner mb-6">
              🌸
            </div>
            <h2 className="text-3xl font-semibold text-gray-800">Salam, ana Nour.</h2>
            <p className="text-gray-500 leading-relaxed max-w-xs">
              Je suis là pour t'écouter et répondre à tes questions sur ta santé, en toute bienveillance.
            </p>
          </div>
        )}

        {/* Messages List */}
        {conversation.map((msg) => (
          <div key={msg.id} className="w-full space-y-4 animate-fade-in">
            {/* User Bubble */}
            <div className="flex justify-end">
              <div className="bg-pink-100 text-pink-900 px-4 py-2 rounded-2xl rounded-tr-none max-w-[85%] shadow-sm">
                <p>{msg.user_text}</p>
              </div>
            </div>

            {/* Nour Bubble */}
            <div className="flex justify-start">
              <div className="bg-white text-gray-800 px-5 py-4 rounded-2xl rounded-tl-none max-w-[90%] shadow-md border border-gray-100 space-y-2">
                <p className="leading-relaxed">{msg.response_text}</p>
              </div>
            </div>
          </div>
        ))}

        <div ref={bottomRef} />
      </main>

      {/* Footer Area: Player & Recorder */}
      <div className="w-full bg-white/90 backdrop-blur-md border-t border-gray-100 p-4 sticky bottom-0 z-20">
        {/* Audio Player (Invisible or Subtle) */}
        <audio ref={audioRef} className="hidden" />

        <div className="w-full flex justify-center">
          <AudioRecorder onResponseReceived={handleResponse} />
        </div>

        <footer className="w-full pt-4 text-center text-[10px] text-gray-400">
          <p>Assistance virtuelle (POC v1.0). Ne remplace pas un médecin.</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
