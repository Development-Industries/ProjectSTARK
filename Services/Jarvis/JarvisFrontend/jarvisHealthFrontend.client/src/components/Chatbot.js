import React, { useState } from 'react';
import axios from 'axios';

function Chatbot() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');

    const sendMessage = async () => {
        try {
            const response = await axios.post('http://localhost:5001/chat', { input });
            setMessages([...messages, { sender: 'user', text: input }, { sender: 'bot', text: response.data.response }]);
            setInput('');
        } catch (error) {
            console.error('Error communicating with chatbot', error);
        }
    };

    return (
        <div className="chatbot">
            <div className="messages">
                {messages.map((msg, idx) => (
                    <div key={idx} className={`message ${msg.sender}`}>
                        {msg.text}
                    </div>
                ))}
            </div>
            <input value={input} onChange={(e) => setInput(e.target.value)} onKeyPress={(e) => e.key === 'Enter' && sendMessage()} />
            <button onClick={sendMessage}>Send</button>
        </div>
    );
}

export default Chatbot;
