export interface TreeNode {
  id: string;
  name: string;
  status: 'completed' | 'progress' | 'pending' | 'active';
  progress?: number;
  children?: TreeNode[];
  parent?: string;
  description?: string;
  importance?: string;
  agentLevel?: number; // AgentLevel enum value (1, 2, 3)
  checkpointNumber?: number; // For Character Identity checkpoints
  metadata?: {
    workingOn?: string;
    estimatedTime?: string;
    lastUpdate?: string;
    wave?: number; // For Character Identity waves
    sessionId?: string; // Entry or Scene session ID
    characterId?: string; // Character development ID
  };
}

export interface ChatMessage {
  id: string;
  type: 'user' | 'agent' | 'thinking' | 'action' | 'code';
  content: string;
  timestamp: Date;
  nodeContext?: string;
  thinkingTime?: string; // e.g., "2s"
}

export interface Conversation {
  id: string;
  name: string;
  lastActivity: string;
  active?: boolean;
}

export type Tab = 'tree' | 'timeline';
export type Agent = 'Sub-1' | 'Sub-2' | 'Sub-3';

// For ReactFlow
export interface FlowNode {
  id: string;
  type: string;
  position: { x: number; y: number };
  data: {
    label: string;
    status: 'completed' | 'progress' | 'pending' | 'active';
    progress?: number;
  };
}

export interface FlowEdge {
  id: string;
  source: string;
  target: string;
  type?: string;
}
