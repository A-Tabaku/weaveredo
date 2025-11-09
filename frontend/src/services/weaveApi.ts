/**
 * Weave API Service
 * Handles all communication with the backend FastAPI server
 */

const API_BASE_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

export interface Character {
  name: string;
  appearance: string;
  personality: string;
  role: string;
  importance?: string;
}

export interface Scene {
  title: string;
  description: string;
  characters_involved: string[];
  setting: string;
  mood: string;
}

export interface Storyline {
  overview: string;
  tone: string;
  scenes: Scene[];
}

export interface VisualStyle {
  description: string;
  image_path: string;
}

export interface EntryAgentOutput {
  characters: Character[];
  storyline: Storyline;
  visual_style?: VisualStyle;
}

export interface EntryChatResponse {
  response: string;
  is_final: boolean;
  output: EntryAgentOutput | null;
  status: 'active' | 'completed';
}

export interface CheckpointOutput {
  narrative: string;
  structured: Record<string, any>;
}

export interface Checkpoint {
  checkpoint_number: number;
  agent: string;
  status: 'pending' | 'awaiting_approval' | 'approved' | 'rejected';
  output: CheckpointOutput;
  metadata: {
    wave: number;
    timestamp: string;
    tokens_used: number;
    agent_time_seconds: number;
  };
}

export interface CharacterStatus {
  character_id: string;
  current_wave: number;
  current_checkpoint: number;
  status: string;
  progress: {
    completed_checkpoints: number;
    total_checkpoints: number;
    current_checkpoint: number;
  };
  agents: Record<string, any>;
}

export type WebSocketMessageType =
  | { type: 'wave_started'; wave: number; agents: string[] }
  | { type: 'agent_completed'; agent: string; wave: number; time_seconds: number }
  | { type: 'checkpoint_ready'; checkpoint: number; agent: string }
  | { type: 'wave_complete'; wave: number; agents_completed: string[]; next_wave?: number }
  | { type: 'awaiting_approval'; wave: number; checkpoints: number[] }
  | { type: 'character_complete'; character_id: string; total_checkpoints: number }
  | { type: 'error'; message: string; agent?: string };

/**
 * Entry Agent API
 */
export const entryAgent = {
  async start(): Promise<{ session_id: string; status: string; message: string }> {
    const response = await fetch(`${API_BASE_URL}/api/entry/start`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({}),
    });
    if (!response.ok) throw new Error('Failed to start entry agent');
    return response.json();
  },

  async chat(sessionId: string, message: string): Promise<EntryChatResponse> {
    const response = await fetch(`${API_BASE_URL}/api/entry/${sessionId}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message }),
    });
    if (!response.ok) throw new Error('Failed to send message');
    return response.json();
  },

  async getStatus(sessionId: string) {
    const response = await fetch(`${API_BASE_URL}/api/entry/${sessionId}/status`);
    if (!response.ok) throw new Error('Failed to get status');
    return response.json();
  },
};

/**
 * Character Identity Agent API
 */
export const characterAgent = {
  async start(data: {
    characters: Character[];
    storyline: Storyline;
    mode?: 'balanced' | 'detailed' | 'quick';
  }): Promise<{ character_id: string; status: string; message: string; checkpoint_count: number }> {
    const response = await fetch(`${API_BASE_URL}/api/character/start`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error('Failed to start character development');
    return response.json();
  },

  async getStatus(characterId: string): Promise<CharacterStatus> {
    const response = await fetch(`${API_BASE_URL}/api/character/${characterId}/status`);
    if (!response.ok) throw new Error('Failed to get character status');
    return response.json();
  },

  async getCheckpoint(characterId: string, checkpointNumber: number): Promise<Checkpoint> {
    const response = await fetch(
      `${API_BASE_URL}/api/character/${characterId}/checkpoint/${checkpointNumber}`
    );
    if (!response.ok) throw new Error('Failed to get checkpoint');
    return response.json();
  },

  async approve(characterId: string, checkpoint: number) {
    const response = await fetch(`${API_BASE_URL}/api/character/${characterId}/approve`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ checkpoint }),
    });
    if (!response.ok) throw new Error('Failed to approve checkpoint');
    return response.json();
  },

  async getFinal(characterId: string) {
    const response = await fetch(`${API_BASE_URL}/api/character/${characterId}/final`);
    if (!response.ok) throw new Error('Failed to get final profile');
    return response.json();
  },
};

/**
 * Scene Creator Agent API
 */
export const sceneAgent = {
  async start(data: {
    project_id?: string;
    mode?: 'creative_overview' | 'analytical' | 'deep_dive';
  }) {
    const response = await fetch(`${API_BASE_URL}/api/scene/start`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error('Failed to start scene creator');
    return response.json();
  },

  async chat(projectId: string, message: string) {
    const response = await fetch(`${API_BASE_URL}/api/scene/${projectId}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message }),
    });
    if (!response.ok) throw new Error('Failed to send message');
    return response.json();
  },

  async getStatus(projectId: string) {
    const response = await fetch(`${API_BASE_URL}/api/scene/${projectId}/status`);
    if (!response.ok) throw new Error('Failed to get status');
    return response.json();
  },
};
