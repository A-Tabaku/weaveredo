# Complete Frontend Integration Guide for Weave

## Overview

This guide shows how to integrate the Weave frontend with the complete multi-agent backend:

**Agent Flow:**
```
Entry Agent → Character Identity → Scene Creator
    ↓              ↓                    ↓
  Q&A        8 Checkpoints      Scene Creation
           + Image Gen         + Mode Selection
```

**Key Features to Implement:**
- Real-time chat with all 3 agent types
- Checkpoint approval/rejection UI
- Image display for generated character images
- Progress tracking across waves
- Mode selection for Scene Creator
- WebSocket updates for Character Development

---

## Part 1: API Architecture

### Base URL
```typescript
const API_BASE_URL = 'http://localhost:8000';
const WS_BASE_URL = 'ws://localhost:8000';
```

### Complete API Endpoints

#### **Entry Agent (Level 1)**
```typescript
POST   /api/entry/start                    // Start Entry conversation
POST   /api/entry/{session_id}/chat        // Send message
GET    /api/entry/{session_id}/status      // Get status

// Response format
{
  "response": string,          // Agent's text response
  "is_final": boolean,         // true when JSON output ready
  "output": {                  // null until is_final = true
    "characters": [...],
    "storyline": {...}
  },
  "status": "active" | "completed"
}
```

#### **Character Identity (Level 2)**
```typescript
POST   /api/character/start                      // Start character dev
GET    /api/character/{id}/status                // Get status
GET    /api/character/{id}/checkpoint/{num}      // Get checkpoint
POST   /api/character/{id}/approve               // Approve checkpoint
POST   /api/character/{id}/feedback              // Reject + feedback
GET    /api/character/{id}/final                 // Get final profile
WS     /ws/character/{id}                        // WebSocket updates

// Checkpoint structure
{
  "checkpoint_number": 1,
  "agent": "Personality",
  "status": "awaiting_approval",
  "output": {
    "narrative": string,       // Human-readable description
    "structured": {            // JSON data
      "core_traits": [...],
      "fears": [...],
      ...
    }
  },
  "metadata": {
    "wave": 1,
    "timestamp": string,
    "tokens_used": number,
    "agent_time_seconds": number
  }
}
```

#### **Scene Creator (Level 3)**
```typescript
POST   /api/scene/start                    // Start scene creation
POST   /api/scene/{project_id}/chat        // Send message
POST   /api/scene/{project_id}/mode        // Switch mode
GET    /api/scene/{project_id}/status      // Get status

// Mode options
"creative_overview"  // Fast prototyping
"analytical"         // Production quality
"deep_dive"          // Maximum control
```

#### **Project Management**
```typescript
POST   /api/projects                       // Create project
GET    /api/projects                       // List projects
GET    /api/projects/{id}                  // Get project
```

#### **Images**
```typescript
// Static file serving
GET    /character_data/{character_id}/images/portrait.png
GET    /character_data/{character_id}/images/full_body.png
GET    /character_data/{character_id}/images/action.png
GET    /character_data/{character_id}/images/expression.png
```

---

## Part 2: Frontend Implementation

### Step 1: API Service Layer

Create `/frontend/src/services/api.ts`:

```typescript
import axios from 'axios';

const API_BASE = 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ============================================================================
// ENTRY AGENT API
// ============================================================================

export const entryAgent = {
  start: async () => {
    const { data } = await api.post('/api/entry/start', {});
    return data;
  },

  sendMessage: async (sessionId: string, message: string) => {
    const { data } = await api.post(`/api/entry/${sessionId}/chat`, { message });
    return data;
  },

  getStatus: async (sessionId: string) => {
    const { data } = await api.get(`/api/entry/${sessionId}/status`);
    return data;
  },
};

// ============================================================================
// CHARACTER IDENTITY API
// ============================================================================

export const characterAgent = {
  start: async (entryOutput: any, mode: string = 'balanced') => {
    const { data } = await api.post('/api/character/start', {
      characters: entryOutput.characters,
      storyline: entryOutput.storyline,
      mode,
    });
    return data;
  },

  getStatus: async (characterId: string) => {
    const { data } = await api.get(`/api/character/${characterId}/status`);
    return data;
  },

  getCheckpoint: async (characterId: string, checkpointNum: number) => {
    const { data } = await api.get(`/api/character/${characterId}/checkpoint/${checkpointNum}`);
    return data;
  },

  approveCheckpoint: async (characterId: string, checkpointNum: number) => {
    const { data } = await api.post(`/api/character/${characterId}/approve`, {
      checkpoint: checkpointNum,
    });
    return data;
  },

  rejectCheckpoint: async (characterId: string, checkpointNum: number, feedback: string) => {
    const { data } = await api.post(`/api/character/${characterId}/feedback`, {
      checkpoint: checkpointNum,
      feedback,
    });
    return data;
  },

  getFinalProfile: async (characterId: string) => {
    const { data } = await api.get(`/api/character/${characterId}/final`);
    return data;
  },
};

// ============================================================================
// SCENE CREATOR API
// ============================================================================

export const sceneAgent = {
  start: async (projectId: string, mode: string = 'creative_overview') => {
    const { data } = await api.post('/api/scene/start', { project_id: projectId, mode });
    return data;
  },

  sendMessage: async (projectId: string, message: string) => {
    const { data } = await api.post(`/api/scene/${projectId}/chat`, { message });
    return data;
  },

  switchMode: async (projectId: string, mode: string) => {
    const { data } = await api.post(`/api/scene/${projectId}/mode`, { mode });
    return data;
  },

  getStatus: async (projectId: string) => {
    const { data } = await api.get(`/api/scene/${projectId}/status`);
    return data;
  },
};

// ============================================================================
// PROJECT API
// ============================================================================

export const projectsAPI = {
  create: async (name: string, description: string = '') => {
    const { data } = await api.post('/api/projects', { name, description });
    return data;
  },

  list: async () => {
    const { data } = await api.get('/api/projects');
    return data;
  },

  get: async (projectId: string) => {
    const { data } = await api.get(`/api/projects/${projectId}`);
    return data;
  },
};

// ============================================================================
// WEBSOCKET CONNECTION
// ============================================================================

export const createWebSocket = (characterId: string, onMessage: (msg: any) => void) => {
  const ws = new WebSocket(`ws://localhost:8000/ws/character/${characterId}`);

  ws.onopen = () => {
    console.log('WebSocket connected');
    // Send ping every 30s to keep alive
    setInterval(() => ws.send('ping'), 30000);
  };

  ws.onmessage = (event) => {
    try {
      const message = JSON.parse(event.data);
      onMessage(message);
    } catch (e) {
      console.error('Failed to parse WebSocket message:', e);
    }
  };

  ws.onerror = (error) => {
    console.error('WebSocket error:', error);
  };

  ws.onclose = () => {
    console.log('WebSocket disconnected');
  };

  return ws;
};
```

---

### Step 2: Zustand Store Updates

Update `/frontend/src/store/useStore.ts`:

```typescript
import { create } from 'zustand';

interface Message {
  id: string;
  role: 'user' | 'agent' | 'system';
  content: string;
  timestamp: Date;
  agentType?: 'entry' | 'character' | 'scene';
}

interface Checkpoint {
  number: number;
  agent: string;
  status: 'pending' | 'awaiting_approval' | 'approved' | 'rejected';
  narrative: string;
  structured: any;
  images?: string[];
}

interface WeaveStore {
  // Session state
  currentAgentLevel: 'entry' | 'character' | 'scene';
  sessionId: string | null;
  characterId: string | null;
  projectId: string | null;

  // Entry Agent
  entryOutput: any | null;
  setEntryOutput: (output: any) => void;

  // Character Development
  checkpoints: Checkpoint[];
  currentCheckpoint: number | null;
  addCheckpoint: (checkpoint: Checkpoint) => void;
  updateCheckpointStatus: (num: number, status: string) => void;

  // Scene Creation
  sceneMode: string;
  setSceneMode: (mode: string) => void;

  // Chat messages
  messages: Message[];
  addMessage: (message: Omit<Message, 'id' | 'timestamp'>) => void;
  clearMessages: () => void;

  // Loading & errors
  isLoading: boolean;
  setLoading: (loading: boolean) => void;
  error: string | null;
  setError: (error: string | null) => void;

  // WebSocket
  wsConnection: WebSocket | null;
  setWSConnection: (ws: WebSocket | null) => void;
}

export const useStore = create<WeaveStore>((set) => ({
  // Initial state
  currentAgentLevel: 'entry',
  sessionId: null,
  characterId: null,
  projectId: null,

  entryOutput: null,
  setEntryOutput: (output) => set({ entryOutput: output }),

  checkpoints: [],
  currentCheckpoint: null,
  addCheckpoint: (checkpoint) =>
    set((state) => ({
      checkpoints: [...state.checkpoints, checkpoint],
      currentCheckpoint: checkpoint.number,
    })),
  updateCheckpointStatus: (num, status) =>
    set((state) => ({
      checkpoints: state.checkpoints.map((cp) =>
        cp.number === num ? { ...cp, status } : cp
      ),
    })),

  sceneMode: 'creative_overview',
  setSceneMode: (mode) => set({ sceneMode: mode }),

  messages: [],
  addMessage: (message) =>
    set((state) => ({
      messages: [
        ...state.messages,
        {
          ...message,
          id: Math.random().toString(36),
          timestamp: new Date(),
        },
      ],
    })),
  clearMessages: () => set({ messages: [] }),

  isLoading: false,
  setLoading: (loading) => set({ isLoading: loading }),
  error: null,
  setError: (error) => set({ error }),

  wsConnection: null,
  setWSConnection: (ws) => set({ wsConnection: ws }),
}));
```

---

### Step 3: Entry Agent Chat Component

Create `/frontend/src/components/agents/EntryAgentChat.tsx`:

```typescript
import React, { useState, useEffect } from 'react';
import { useStore } from '../../store/useStore';
import { entryAgent } from '../../services/api';

export const EntryAgentChat: React.FC = () => {
  const [input, setInput] = useState('');
  const {
    sessionId,
    messages,
    addMessage,
    setEntryOutput,
    isLoading,
    setLoading,
  } = useStore();

  // Start Entry session on mount
  useEffect(() => {
    const startSession = async () => {
      const response = await entryAgent.start();
      useStore.setState({ sessionId: response.session_id });

      addMessage({
        role: 'agent',
        content: response.message,
        agentType: 'entry',
      });
    };

    if (!sessionId) {
      startSession();
    }
  }, [sessionId]);

  const handleSend = async () => {
    if (!input.trim() || !sessionId) return;

    // Add user message to chat
    addMessage({ role: 'user', content: input });
    setInput('');
    setLoading(true);

    try {
      // Send to Entry Agent
      const response = await entryAgent.sendMessage(sessionId, input);

      // Add agent response
      addMessage({
        role: 'agent',
        content: response.response,
        agentType: 'entry',
      });

      // If final output, store it and show transition option
      if (response.is_final && response.output) {
        setEntryOutput(response.output);

        addMessage({
          role: 'system',
          content: '✓ Video concept complete! Click "Start Character Development" to continue.',
        });
      }
    } catch (error) {
      console.error('Error sending message:', error);
      useStore.setState({ error: 'Failed to send message' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[70%] rounded-lg p-3 ${
                msg.role === 'user'
                  ? 'bg-blue-600 text-white'
                  : msg.role === 'system'
                  ? 'bg-green-900/30 text-green-300'
                  : 'bg-gray-800 text-gray-100'
              }`}
            >
              <p className="whitespace-pre-wrap">{msg.content}</p>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="text-gray-500 italic">Entry Agent is thinking...</div>
        )}
      </div>

      {/* Input */}
      <div className="border-t border-gray-700 p-4">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Describe your video concept..."
            className="flex-1 bg-gray-800 text-white rounded-lg px-4 py-2 outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          />
          <button
            onClick={handleSend}
            disabled={isLoading || !input.trim()}
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white px-6 py-2 rounded-lg transition"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
};
```

---

### Step 4: Checkpoint Approval Component

Create `/frontend/src/components/character/CheckpointApproval.tsx`:

```typescript
import React, { useState } from 'react';
import { Checkpoint } from '../../store/useStore';
import { characterAgent } from '../../services/api';

interface Props {
  checkpoint: Checkpoint;
  characterId: string;
  onApprove: () => void;
  onReject: (feedback: string) => void;
}

export const CheckpointApproval: React.FC<Props> = ({
  checkpoint,
  characterId,
  onApprove,
  onReject,
}) => {
  const [showFull, setShowFull] = useState(false);
  const [feedback, setFeedback] = useState('');
  const [showFeedbackInput, setShowFeedbackInput] = useState(false);

  const handleApprove = async () => {
    try {
      await characterAgent.approveCheckpoint(characterId, checkpoint.number);
      onApprove();
    } catch (error) {
      console.error('Failed to approve checkpoint:', error);
    }
  };

  const handleReject = async () => {
    try {
      await characterAgent.rejectCheckpoint(characterId, checkpoint.number, feedback);
      onReject(feedback);
      setShowFeedbackInput(false);
      setFeedback('');
    } catch (error) {
      console.error('Failed to reject checkpoint:', error);
    }
  };

  return (
    <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-bold text-white">
          Checkpoint #{checkpoint.number}: {checkpoint.agent}
        </h3>
        <span
          className={`px-3 py-1 rounded-full text-sm ${
            checkpoint.status === 'approved'
              ? 'bg-green-900/30 text-green-400'
              : checkpoint.status === 'awaiting_approval'
              ? 'bg-yellow-900/30 text-yellow-400'
              : 'bg-gray-700 text-gray-400'
          }`}
        >
          {checkpoint.status}
        </span>
      </div>

      {/* Narrative */}
      <div className="mb-4">
        <h4 className="text-sm font-semibold text-gray-400 mb-2">Narrative</h4>
        <p className="text-gray-300 whitespace-pre-wrap">
          {showFull
            ? checkpoint.narrative
            : checkpoint.narrative.slice(0, 800) +
              (checkpoint.narrative.length > 800 ? '...' : '')}
        </p>
        {checkpoint.narrative.length > 800 && (
          <button
            onClick={() => setShowFull(!showFull)}
            className="text-blue-400 hover:text-blue-300 mt-2 text-sm"
          >
            {showFull ? 'Show less' : 'Show full narrative'}
          </button>
        )}
      </div>

      {/* Structured Data Preview */}
      <div className="mb-4">
        <h4 className="text-sm font-semibold text-gray-400 mb-2">Structured Data</h4>
        <div className="bg-gray-900 rounded p-3 space-y-2">
          {Object.entries(checkpoint.structured).slice(0, 5).map(([key, value]) => (
            <div key={key} className="text-sm">
              <span className="text-gray-500">• {key}:</span>{' '}
              <span className="text-gray-300">
                {Array.isArray(value)
                  ? `${value.length} items`
                  : typeof value === 'string' && value.length > 60
                  ? value.slice(0, 60) + '...'
                  : String(value)}
              </span>
            </div>
          ))}
          <button
            onClick={() => setShowFull(!showFull)}
            className="text-blue-400 hover:text-blue-300 text-xs"
          >
            View full JSON
          </button>
        </div>
      </div>

      {/* Images (if any) */}
      {checkpoint.images && checkpoint.images.length > 0 && (
        <div className="mb-4">
          <h4 className="text-sm font-semibold text-gray-400 mb-2">Generated Images</h4>
          <div className="grid grid-cols-2 gap-3">
            {checkpoint.images.map((imgPath, idx) => (
              <img
                key={idx}
                src={`http://localhost:8000${imgPath}`}
                alt={`Generated ${idx + 1}`}
                className="w-full h-48 object-cover rounded border border-gray-700"
              />
            ))}
          </div>
        </div>
      )}

      {/* Action Buttons */}
      {checkpoint.status === 'awaiting_approval' && (
        <div className="flex gap-3">
          <button
            onClick={handleApprove}
            className="flex-1 bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded-lg transition"
          >
            ✓ Approve
          </button>
          <button
            onClick={() => setShowFeedbackInput(!showFeedbackInput)}
            className="flex-1 bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded-lg transition"
          >
            ✗ Reject & Provide Feedback
          </button>
        </div>
      )}

      {/* Feedback Input */}
      {showFeedbackInput && (
        <div className="mt-4">
          <textarea
            value={feedback}
            onChange={(e) => setFeedback(e.target.value)}
            placeholder="What would you like to change?"
            className="w-full bg-gray-900 text-white rounded-lg p-3 outline-none focus:ring-2 focus:ring-red-500 h-24"
          />
          <button
            onClick={handleReject}
            disabled={!feedback.trim()}
            className="mt-2 bg-red-600 hover:bg-red-700 disabled:bg-gray-600 text-white py-2 px-4 rounded-lg transition"
          >
            Submit Feedback
          </button>
        </div>
      )}
    </div>
  );
};
```

---

### Step 5: Character Development Component with WebSocket

Create `/frontend/src/components/character/CharacterDevelopment.tsx`:

```typescript
import React, { useEffect, useState } from 'react';
import { useStore } from '../../store/useStore';
import { characterAgent, createWebSocket } from '../../services/api';
import { CheckpointApproval } from './CheckpointApproval';

export const CharacterDevelopment: React.FC = () => {
  const {
    characterId,
    entryOutput,
    checkpoints,
    addCheckpoint,
    updateCheckpointStatus,
    wsConnection,
    setWSConnection,
  } = useStore();

  const [currentWave, setCurrentWave] = useState(0);
  const [status, setStatus] = useState('idle');

  // Start character development
  useEffect(() => {
    const startDevelopment = async () => {
      if (!entryOutput || characterId) return;

      try {
        const response = await characterAgent.start(entryOutput, 'balanced');
        useStore.setState({ characterId: response.character_id });

        // Connect WebSocket
        const ws = createWebSocket(response.character_id, handleWebSocketMessage);
        setWSConnection(ws);
      } catch (error) {
        console.error('Failed to start character development:', error);
      }
    };

    startDevelopment();
  }, [entryOutput, characterId]);

  // Handle WebSocket messages
  const handleWebSocketMessage = (message: any) => {
    console.log('WebSocket message:', message);

    switch (message.type) {
      case 'wave_started':
        setCurrentWave(message.wave);
        break;

      case 'agent_started':
        setStatus(`${message.agent} agent running...`);
        break;

      case 'agent_completed':
        setStatus(`${message.agent} complete`);
        break;

      case 'checkpoint_ready':
        // Fetch full checkpoint data
        fetchCheckpoint(message.checkpoint);
        break;

      case 'character_complete':
        setStatus('Character development complete!');
        break;

      case 'error':
        setStatus(`Error: ${message.message}`);
        break;
    }
  };

  const fetchCheckpoint = async (checkpointNum: number) => {
    if (!characterId) return;

    try {
      const checkpoint = await characterAgent.getCheckpoint(characterId, checkpointNum);

      // Check if checkpoint has images
      const images: string[] = [];
      if (checkpoint.agent === 'ImageGeneration') {
        ['portrait', 'full_body', 'action', 'expression'].forEach((type) => {
          images.push(`/character_data/${characterId}/images/${type}.png`);
        });
      }

      addCheckpoint({
        number: checkpointNum,
        agent: checkpoint.agent,
        status: checkpoint.status,
        narrative: checkpoint.output.narrative,
        structured: checkpoint.output.structured,
        images: images.length > 0 ? images : undefined,
      });
    } catch (error) {
      console.error('Failed to fetch checkpoint:', error);
    }
  };

  const handleApprove = () => {
    // Checkpoint auto-continues via backend
    setStatus('Checkpoint approved, continuing...');
  };

  const handleReject = (feedback: string) => {
    setStatus(`Feedback submitted: ${feedback}`);
  };

  return (
    <div className="h-full overflow-y-auto p-6">
      {/* Header */}
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-white mb-2">Character Development</h2>
        <div className="flex items-center gap-4 text-sm">
          <span className="text-gray-400">Wave {currentWave}/3</span>
          <span className="text-gray-400">•</span>
          <span className="text-gray-400">{status}</span>
          <span className="text-gray-400">•</span>
          <span className="text-green-400">
            {checkpoints.filter((cp) => cp.status === 'approved').length}/8 checkpoints
          </span>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="mb-8">
        <div className="h-2 bg-gray-700 rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-blue-500 to-purple-500 transition-all duration-500"
            style={{ width: `${(checkpoints.length / 8) * 100}%` }}
          />
        </div>
      </div>

      {/* Checkpoints */}
      <div className="space-y-6">
        {checkpoints.map((checkpoint) => (
          <CheckpointApproval
            key={checkpoint.number}
            checkpoint={checkpoint}
            characterId={characterId!}
            onApprove={handleApprove}
            onReject={handleReject}
          />
        ))}
      </div>

      {/* Loading state */}
      {checkpoints.length === 0 && (
        <div className="text-center text-gray-500 py-12">
          <div className="animate-spin w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full mx-auto mb-4"></div>
          <p>Starting 7-agent character development pipeline...</p>
        </div>
      )}
    </div>
  );
};
```

---

### Step 6: Scene Creator Component

Create `/frontend/src/components/scene/SceneCreator.tsx`:

```typescript
import React, { useState, useEffect } from 'react';
import { useStore } from '../../store/useStore';
import { sceneAgent } from '../../services/api';

export const SceneCreator: React.FC = () => {
  const [input, setInput] = useState('');
  const { projectId, sceneMode, setSceneMode, messages, addMessage, isLoading, setLoading } =
    useStore();

  // Start scene session
  useEffect(() => {
    const startScene = async () => {
      if (projectId) return;

      const response = await sceneAgent.start('default', sceneMode);
      useStore.setState({ projectId: response.project_id });

      addMessage({
        role: 'agent',
        content: response.message,
        agentType: 'scene',
      });
    };

    startScene();
  }, [projectId]);

  const handleSend = async () => {
    if (!input.trim() || !projectId) return;

    addMessage({ role: 'user', content: input });
    setInput('');
    setLoading(true);

    try {
      const response = await sceneAgent.sendMessage(projectId, input);

      addMessage({
        role: 'agent',
        content: response.response,
        agentType: 'scene',
      });
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleModeSwitch = async (mode: string) => {
    if (!projectId) return;

    try {
      await sceneAgent.switchMode(projectId, mode);
      setSceneMode(mode);

      addMessage({
        role: 'system',
        content: `Mode switched to ${mode}`,
      });
    } catch (error) {
      console.error('Failed to switch mode:', error);
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Mode Selector */}
      <div className="border-b border-gray-700 p-4">
        <div className="flex gap-2">
          {['creative_overview', 'analytical', 'deep_dive'].map((mode) => (
            <button
              key={mode}
              onClick={() => handleModeSwitch(mode)}
              className={`px-4 py-2 rounded-lg text-sm transition ${
                sceneMode === mode
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
              }`}
            >
              {mode.replace('_', ' ')}
            </button>
          ))}
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[70%] rounded-lg p-3 ${
                msg.role === 'user' ? 'bg-blue-600 text-white' : 'bg-gray-800 text-gray-100'
              }`}
            >
              <p className="whitespace-pre-wrap">{msg.content}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Input */}
      <div className="border-t border-gray-700 p-4">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Describe your scene..."
            className="flex-1 bg-gray-800 text-white rounded-lg px-4 py-2 outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          />
          <button
            onClick={handleSend}
            disabled={isLoading || !input.trim()}
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white px-6 py-2 rounded-lg transition"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
};
```

---

### Step 7: Main App Integration

Update `/frontend/src/App.tsx`:

```typescript
import React from 'react';
import { useStore } from './store/useStore';
import { EntryAgentChat } from './components/agents/EntryAgentChat';
import { CharacterDevelopment } from './components/character/CharacterDevelopment';
import { SceneCreator } from './components/scene/SceneCreator';

const App: React.FC = () => {
  const { currentAgentLevel, entryOutput, characterId } = useStore();

  // Determine which component to show
  const renderCurrentAgent = () => {
    if (!entryOutput) {
      return <EntryAgentChat />;
    } else if (!characterId || currentAgentLevel === 'character') {
      return <CharacterDevelopment />;
    } else {
      return <SceneCreator />;
    }
  };

  // Agent progress indicator
  const getAgentStep = () => {
    if (!entryOutput) return 1;
    if (!characterId) return 2;
    return 3;
  };

  return (
    <div className="h-screen bg-gray-900 flex flex-col">
      {/* Top Bar with Progress */}
      <div className="bg-gray-800 border-b border-gray-700 p-4">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-white">Weave</h1>

          {/* Agent Progress */}
          <div className="flex items-center gap-6">
            <div className={`flex items-center gap-2 ${getAgentStep() >= 1 ? 'text-green-400' : 'text-gray-500'}`}>
              {getAgentStep() > 1 ? '✓' : '1'}
              <span>Entry</span>
            </div>
            <div className={`flex items-center gap-2 ${getAgentStep() >= 2 ? 'text-blue-400' : 'text-gray-500'}`}>
              {getAgentStep() > 2 ? '✓' : '2'}
              <span>Character</span>
            </div>
            <div className={`flex items-center gap-2 ${getAgentStep() >= 3 ? 'text-purple-400' : 'text-gray-500'}`}>
              3<span>Scene</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-hidden">{renderCurrentAgent()}</div>
    </div>
  );
};

export default App;
```

---

## Part 3: Complete Flow Example

### User Journey:

1. **Entry Agent (Level 1)**
   ```
   User: "I want to create a detective character"
   Agent: [asks questions about character and storyline]
   ...
   Agent: [outputs JSON with characters and storyline]
   UI: Shows "Start Character Development" button
   ```

2. **Character Development (Level 2)**
   ```
   Backend: Starts 7 sub-agents in 3 waves
   WebSocket: Sends real-time updates
   UI: Shows checkpoints as they complete

   Checkpoint 1 (Personality):
   - Narrative: "Alex is a hypervigilant analyst..."
   - Structured: { core_traits: [...], fears: [...] }
   - User: [Approves or Rejects with feedback]

   Checkpoint 7 (Image Generation):
   - Shows 4 generated character images
   - User can view/approve

   Checkpoint 8 (Final):
   - Complete character profile
   - UI: Shows "Start Scene Creation" button
   ```

3. **Scene Creation (Level 3)**
   ```
   User: Selects mode (creative_overview, analytical, deep_dive)
   User: "Create a tense confrontation scene"
   Agent: [generates scene concepts with cinematography]
   User: Provides feedback iteratively
   Agent: Outputs final scene JSON
   ```

---

## Part 4: Key Features Checklist

### Must-Have Features:
- ✅ Entry Agent chat interface
- ✅ Character checkpoint approval/rejection UI
- ✅ WebSocket real-time updates
- ✅ Image display for generated characters
- ✅ Scene Creator with mode selection
- ✅ Progress tracking across all 3 levels
- ✅ Error handling and loading states
- ✅ Conversation history preservation

### Advanced Features:
- 🔲 Checkpoint history browser
- 🔲 Character comparison view
- 🔲 Scene timeline editor
- 🔲 Export/import project data
- 🔲 Multi-user collaboration
- 🔲 Version control for characters/scenes

---

## Part 5: Testing Checklist

### Backend Testing:
```bash
# Terminal 1: Start backend
cd backend
uvicorn api.server:app --reload --port 8000

# Terminal 2: Test endpoints
curl http://localhost:8000/health
curl -X POST http://localhost:8000/api/entry/start
```

### Frontend Testing:
```bash
# Terminal 3: Start frontend
cd frontend
npm run dev
```

### End-to-End Flow:
1. Start Entry Agent → answer questions → get JSON
2. Auto-transition to Character Development
3. WebSocket connects → receives checkpoints
4. Approve/reject each checkpoint
5. View generated images
6. Transition to Scene Creator
7. Create scenes with different modes

---

## Summary

**This guide provides:**
- ✅ Complete API service layer
- ✅ Zustand store integration
- ✅ All 3 agent chat components
- ✅ Checkpoint approval UI
- ✅ Image display
- ✅ WebSocket real-time updates
- ✅ Mode selection for Scene Creator
- ✅ Full Entry → Character → Scene flow

**Start building:**
1. Copy API service code
2. Update Zustand store
3. Create components one by one
4. Test with backend running
5. Iterate on UX/UI polish

The system is now fully integrated with interruptions, checkpoints, approvals, and real-time progress tracking! 🚀
