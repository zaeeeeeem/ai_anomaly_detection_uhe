import React, { useEffect } from 'react';
import { useChat } from '../hooks/useChat';
import { MainLayout } from '../components/layout/MainLayout';
import { MessageList } from '../components/chat/MessageList';
import { ChatInput } from '../components/chat/ChatInput';
import { NewConversationButton } from '../components/conversations/NewConversationButton';
import './Chat.css';

export const Chat = () => {
  const { activeConversation, messages, sendMessage, sending, loadConversations } =
    useChat();

  useEffect(() => {
    loadConversations();
  }, [loadConversations]);

  const handleSendMessage = async (content) => {
    try {
      await sendMessage(content);
    } catch (error) {
      console.error('Failed to send message:', error);
      alert('Failed to send message. Please try again.');
    }
  };

  return (
    <MainLayout>
      <div className="chat-page">
        {activeConversation ? (
          <>
            <div className="chat-header">
              <h2 className="chat-title">{activeConversation.title}</h2>
              <div className="chat-info">
                <span className="chat-model">
                  {activeConversation.model_type}: {activeConversation.model_name}
                </span>
              </div>
            </div>

            <MessageList messages={messages} sending={sending} />
            <ChatInput onSend={handleSendMessage} disabled={sending} />
          </>
        ) : (
          <div className="chat-empty">
            <div className="chat-empty-panel">
              <svg
                className="chat-empty-icon"
                width="80"
                height="80"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
              >
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
              </svg>
              <h2>Start a New Conversation</h2>
              <p>
                Create a new conversation to begin chatting with MediGuard AI.
              </p>
              <NewConversationButton />
            </div>
          </div>
        )}
      </div>
    </MainLayout>
  );
};
