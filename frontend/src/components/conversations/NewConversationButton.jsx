import React, { useEffect, useState } from 'react';
import { useChat } from '../../hooks/useChat';
import { chatService } from '../../services/chatService';
import './NewConversationButton.css';

const MODEL_TYPES = [
  { label: 'Gemini', value: 'gemini' },
  { label: 'Ollama', value: 'ollama' },
];

export const NewConversationButton = () => {
  const { createConversation } = useChat();
  const [open, setOpen] = useState(false);
  const [title, setTitle] = useState('New Conversation');
  const [modelType, setModelType] = useState('gemini');
  const [modelName, setModelName] = useState('gemini-2.5-flash-lite');
  const [modelOptions, setModelOptions] = useState(['gemini-2.5-flash-lite']);

  useEffect(() => {
    const loadModels = async () => {
      try {
        if (modelType === 'gemini') {
          const data = await chatService.getGeminiModels();
          setModelOptions(data.models || ['gemini-2.5-flash-lite']);
          setModelName(data.models?.[0] || 'gemini-2.5-flash-lite');
        } else {
          const data = await chatService.getOllamaModels();
          const names = (data.models || []).map((m) => m.name);
          setModelOptions(names.length ? names : ['llama2']);
          setModelName(names[0] || 'llama2');
        }
      } catch (error) {
        setModelOptions(
          modelType === 'gemini' ? ['gemini-2.5-flash-lite'] : ['llama2']
        );
        setModelName(modelType === 'gemini' ? 'gemini-2.5-flash-lite' : 'llama2');
      }
    };

    loadModels();
  }, [modelType]);

  const handleCreate = async () => {
    await createConversation({
      title,
      model_type: modelType,
      model_name: modelName,
    });
    setOpen(false);
  };

  return (
    <>
      <button className="new-conversation-btn" onClick={() => setOpen(true)}>
        + New
      </button>
      {open && (
        <div className="new-conversation-modal">
          <div className="new-conversation-card">
            <h3>New Conversation</h3>
            <label>
              Title
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
              />
            </label>
            <label>
              Model Type
              <select
                value={modelType}
                onChange={(e) => setModelType(e.target.value)}
              >
                {MODEL_TYPES.map((type) => (
                  <option key={type.value} value={type.value}>
                    {type.label}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Model Name
              <select
                value={modelName}
                onChange={(e) => setModelName(e.target.value)}
              >
                {modelOptions.map((model) => (
                  <option key={model} value={model}>
                    {model}
                  </option>
                ))}
              </select>
            </label>
            <div className="new-conversation-actions">
              <button className="ghost" onClick={() => setOpen(false)}>
                Cancel
              </button>
              <button className="primary" onClick={handleCreate}>
                Create
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};
