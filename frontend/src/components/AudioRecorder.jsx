import React, { useState, useRef } from 'react';

const AudioRecorder = ({ onResponseReceived }) => {
    const [isRecording, setIsRecording] = useState(false);
    const [isProcessing, setIsProcessing] = useState(false);
    const mediaRecorderRef = useRef(null);
    const audioChunksRef = useRef([]);
    const sessionIdRef = useRef(crypto.randomUUID());

    const startRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorderRef.current = new MediaRecorder(stream);
            audioChunksRef.current = [];

            mediaRecorderRef.current.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    audioChunksRef.current.push(event.data);
                }
            };

            mediaRecorderRef.current.onstop = sendAudioToBackend;
            mediaRecorderRef.current.start();
            setIsRecording(true);
        } catch (err) {
            console.error("Error accessing microphone:", err);
            alert("Impossible d'accéder au microphone.");
        }
    };

    const stopRecording = () => {
        if (mediaRecorderRef.current && isRecording) {
            mediaRecorderRef.current.stop();
            setIsRecording(false);
            setIsProcessing(true);
        }
    };

    const sendAudioToBackend = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        const formData = new FormData();
        formData.append('audio', audioBlob, 'voice_message.wav');
        formData.append('session_id', sessionIdRef.current);

        try {
            const response = await fetch('http://localhost:8000/chat', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) throw new Error('Network response was not ok');

            const data = await response.json();
            onResponseReceived(data);
        } catch (error) {
            console.error("Error sending audio:", error);
            alert("Erreur de connexion avec Nour.");
        } finally {
            setIsProcessing(false);
        }
    };

    return (
        <div className="flex flex-col items-center justify-center space-y-6">
            <div className={`relative flex items-center justify-center transition-all duration-300 ${isRecording ? 'scale-110' : 'scale-100'}`}>
                {/* Pulse Animations */}
                {isRecording && (
                    <>
                        <div className="absolute w-24 h-24 bg-pink-300 rounded-full opacity-30 animate-ping"></div>
                        <div className="absolute w-32 h-32 bg-pink-200 rounded-full opacity-20 animate-pulse"></div>
                    </>
                )}

                {/* Main Button */}
                <button
                    onClick={isRecording ? stopRecording : startRecording}
                    disabled={isProcessing}
                    className={`relative z-10 p-8 rounded-full shadow-xl transition-all duration-300 focus:outline-none focus:ring-4 focus:ring-pink-200 ${isRecording
                        ? 'bg-red-500 hover:bg-red-600 text-white'
                        : 'bg-gradient-to-br from-pink-500 to-rose-400 hover:from-pink-600 hover:to-rose-500 text-white'
                        } ${isProcessing ? 'opacity-50 cursor-not-allowed' : ''}`}
                >
                    {isProcessing ? (
                        <svg className="animate-spin h-10 w-10 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                    ) : (
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            {isRecording ? (
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /> // Stop Icon placeholder
                            ) : (
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
                            )}
                        </svg>
                    )}
                </button>
            </div>

            <p className="text-gray-500 font-medium text-lg">
                {isProcessing ? "Nour réfléchit..." : isRecording ? "Je vous écoute..." : "Appuyez pour parler"}
            </p>
        </div>
    );
};

export default AudioRecorder;
