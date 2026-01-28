import React, { useEffect, useRef } from 'react';
import { ChatMessage } from './ChatMessage';
import { TypingIndicator } from './TypingIndicator';
import './MessageList.css';

export const MessageList = ({ messages, sending }) => {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, sending]);

  return (
    <div className="message-list">
      {messages.map((message) => (
        <ChatMessage key={message.id} message={message} />
      ))}
      {sending && <TypingIndicator />}
      <div ref={bottomRef} />
    </div>
  );
};
