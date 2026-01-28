import React, { createContext, useCallback, useMemo, useState } from 'react';
import { conversationService } from '../services/conversationService';
import { chatService } from '../services/chatService';

export const ChatContext = createContext(null);

export const ChatProvider = ({ children }) => {
  const [conversations, setConversations] = useState([]);
  const [activeConversation, setActiveConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [sending, setSending] = useState(false);

  const loadConversations = useCallback(async () => {
    setLoading(true);
    try {
      const data = await conversationService.getConversations();
      setConversations(data);
      if (!activeConversation && data.length > 0) {
        setActiveConversation(data[0]);
      }
    } finally {
      setLoading(false);
    }
  }, [activeConversation]);

  const selectConversation = useCallback(async (conversation) => {
    setActiveConversation(conversation);
    const msgs = await conversationService.getMessages(conversation.id);
    setMessages(msgs);
  }, []);

  const createConversation = useCallback(async (payload) => {
    const newConversation = await conversationService.createConversation(payload);
    setConversations((prev) => [newConversation, ...prev]);
    await selectConversation(newConversation);
    return newConversation;
  }, [selectConversation]);

  const deleteConversation = useCallback(async (id) => {
    await conversationService.deleteConversation(id);
    setConversations((prev) => prev.filter((conv) => conv.id !== id));
    if (activeConversation?.id === id) {
      setActiveConversation(null);
      setMessages([]);
    }
  }, [activeConversation]);

  const sendMessage = useCallback(async (content) => {
    if (!activeConversation) {
      throw new Error('No active conversation');
    }
    
    // Optimistic update: Show user message immediately
    const tempUserMessage = {
      id: `temp-${Date.now()}`,
      role: 'user',
      content,
      created_at: new Date().toISOString(),
      isOptimistic: true,
    };
    setMessages((prev) => [...prev, tempUserMessage]);
    
    setSending(true);
    try {
      const response = await chatService.sendMessage(activeConversation.id, {
        content,
      });
      // Fetch updated messages (includes both user message and AI response)
      const updated = await conversationService.getMessages(activeConversation.id);
      setMessages(updated);
      return response;
    } catch (error) {
      // Remove optimistic message on error
      setMessages((prev) => prev.filter(m => m.id !== tempUserMessage.id));
      throw error;
    } finally {
      setSending(false);
    }
  }, [activeConversation]);

  const value = useMemo(
    () => ({
      conversations,
      activeConversation,
      messages,
      loading,
      sending,
      loadConversations,
      selectConversation,
      createConversation,
      deleteConversation,
      sendMessage,
      setActiveConversation,
    }),
    [
      conversations,
      activeConversation,
      messages,
      loading,
      sending,
      loadConversations,
      selectConversation,
      createConversation,
      deleteConversation,
      sendMessage,
    ]
  );

  return <ChatContext.Provider value={value}>{children}</ChatContext.Provider>;
};
