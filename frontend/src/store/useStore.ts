import { create } from 'zustand';
import type { TreeNode, ChatMessage, Conversation, Tab, Agent, AgentLevel, WeaveState } from '../types';
import type { EntryAgentOutput, Checkpoint } from '../services/weaveApi';

interface WeaveStore {
  // Tree state
  nodes: TreeNode[];
  selectedNodeId: string | null;
  setSelectedNode: (id: string | null) => void;
  updateNode: (id: string, updates: Partial<TreeNode>) => void;
  addNode: (node: TreeNode) => void;

  // Chat state
  messages: ChatMessage[];
  addMessage: (message: Omit<ChatMessage, 'id' | 'timestamp'>) => void;
  removeMessage: (id: string) => void;
  clearMessages: () => void;

  // UI state
  activeTab: Tab;
  setActiveTab: (tab: Tab) => void;

  activeAgent: Agent;
  setActiveAgent: (agent: Agent) => void;

  conversations: Conversation[];
  
  // Layout state
  leftPanelWidth: number;
  setLeftPanelWidth: (width: number) => void;

  // Weave Backend Integration
  weave: WeaveState;
  setCurrentAgentLevel: (level: AgentLevel) => void;
  setEntrySessionId: (id: string) => void;
  setEntryOutput: (output: EntryAgentOutput) => void;
  setCharacterId: (id: string) => void;
  addCharacterCheckpoint: (checkpoint: Checkpoint) => void;
  setSceneProjectId: (id: string) => void;
  setProcessing: (isProcessing: boolean) => void;
  setError: (error: string | null) => void;
  initializeAgentTree: () => void;
}

// Mock data for initial state - Simplified high-level workflow
const mockNodes: TreeNode[] = [
  {
    id: 'root',
    name: 'South Park AI Episode',
    status: 'progress',
    progress: 62,
    description: 'Complete AI-generated South Park episode with character consistency and narrative flow',
    importance: 'Root project orchestrating all video production workflows',
  },

  // High-level Pipeline Stages
  {
    id: 'characters',
    name: 'Character & Asset Creation',
    status: 'completed',
    progress: 100,
    parent: 'root',
    description: 'All character models, voices, and animation rigs for the episode',
    importance: 'Foundation for consistent characters across all scenes',
  },

  // Simplified Scenes
  {
    id: 'scene1',
    name: 'Act 1: Setup',
    status: 'completed',
    progress: 100,
    parent: 'root',
    description: 'Town hall meeting where Cartman reveals AI takeover plan',
    importance: 'Establishes conflict and sets episode tone',
  },

  {
    id: 'scene2',
    name: 'Act 2: Rising Action',
    status: 'active',
    progress: 73,
    parent: 'root',
    description: 'Kyle and Stan plan resistance while AI interference escalates',
    importance: 'Currently in progress - Character development and tension building',
  },

  {
    id: 'scene3',
    name: 'Act 3: Climax',
    status: 'progress',
    progress: 35,
    parent: 'root',
    description: 'Fast-paced montage of AI systems taking over South Park',
    importance: 'Visual showcase of stakes and scope of the conflict',
  },

  {
    id: 'scene4',
    name: 'Act 4: Resolution',
    status: 'pending',
    parent: 'root',
    description: 'Final confrontation and episode conclusion',
    importance: 'Wraps up the story arc and provides satisfying ending',
  },

  // Post-Production
  {
    id: 'post',
    name: 'Final Polish & Export',
    status: 'pending',
    parent: 'root',
    description: 'Color grading, audio mastering, and final render',
    importance: 'Professional finishing touches for broadcast quality',
  },
];

// Cursor-style messages with thinking, actions, and code output
const mockMessages: ChatMessage[] = [
  {
    id: '1',
    type: 'user',
    content: 'Create a South Park style episode about AI taking over a small town',
    timestamp: new Date(Date.now() - 10000),
  },
  {
    id: '2',
    type: 'thinking',
    content: 'Planning scene breakdown and character generation',
    timestamp: new Date(Date.now() - 9800),
    thinkingTime: '2s',
  },
  {
    id: '3',
    type: 'action',
    content: 'Read character_templates.json',
    timestamp: new Date(Date.now() - 9500),
  },
  {
    id: '4',
    type: 'action',
    content: 'Read scene_generator.py',
    timestamp: new Date(Date.now() - 9300),
  },
  {
    id: '5',
    type: 'agent',
    content: "Perfect! I'm generating the character profiles and scene breakdown. The tree view shows the generation progress in real-time.",
    timestamp: new Date(Date.now() - 9000),
  },
  {
    id: '6',
    type: 'user',
    content: 'Make the lighting warmer in scene 1',
    timestamp: new Date(Date.now() - 5000),
    nodeContext: 'scene1',
  },
  {
    id: '7',
    type: 'thinking',
    content: 'Analyzing current lighting settings',
    timestamp: new Date(Date.now() - 4800),
    thinkingTime: '1s',
  },
  {
    id: '8',
    type: 'action',
    content: 'Read scene_1_lighting.json',
    timestamp: new Date(Date.now() - 4500),
  },
  {
    id: '9',
    type: 'code',
    content: `{
  "temperature": 3200,
  "intensity": 0.8,
  "filter": "cool"
}`,
    timestamp: new Date(Date.now() - 4300),
  },
  {
    id: '10',
    type: 'action',
    content: 'Updating lighting parameters...',
    timestamp: new Date(Date.now() - 4000),
  },
  {
    id: '11',
    type: 'agent',
    content: "Adjusted lighting to warmer tones (4500K). Scene 1 will now have a golden hour feel with increased temperature and amber filter.",
    timestamp: new Date(Date.now() - 3500),
  },
  {
    id: '12',
    type: 'user',
    content: 'How is the overall production coming along?',
    timestamp: new Date(Date.now() - 2000),
  },
  {
    id: '13',
    type: 'thinking',
    content: 'Analyzing production pipeline status across all nodes',
    timestamp: new Date(Date.now() - 1800),
    thinkingTime: '1s',
  },
  {
    id: '14',
    type: 'agent',
    content: "Great progress! Character pipeline is complete (100%). Scene 1 is finished. Currently working on Scene 2 (73% - audio sync in progress). Scene 3 montage is at 35% with clips being generated. Scene 4 and post-production are queued. Overall episode is 62% complete.",
    timestamp: new Date(Date.now() - 1500),
  },
  {
    id: '15',
    type: 'user',
    content: 'Show me what\'s happening with Scene 2 audio',
    timestamp: new Date(Date.now() - 500),
    nodeContext: 'scene2-audio',
  },
  {
    id: '16',
    type: 'action',
    content: 'Read scene2_audio_mix.json',
    timestamp: new Date(Date.now() - 300),
  },
  {
    id: '17',
    type: 'code',
    content: `{
  "dialogue_tracks": {
    "kyle": { "level": -3.2, "eq": "vocal_clarity", "status": "complete" },
    "stan": { "level": -4.1, "eq": "vocal_clarity", "status": "complete" }
  },
  "sound_effects": {
    "door_open": { "timestamp": "2.4s", "status": "pending" },
    "footsteps": { "timestamp": "5.1s", "status": "pending" },
    "background_ambience": { "level": -18, "status": "processing" }
  },
  "sync_status": "in_progress",
  "estimated_completion": "45s"
}`,
    timestamp: new Date(Date.now() - 200),
  },
  {
    id: '18',
    type: 'agent',
    content: "Dialogue tracks are complete and balanced. Working on sound effects synchronization - door and footstep sounds need to be placed, and background ambience is processing. Should be done in about 45 seconds.",
    timestamp: new Date(Date.now() - 50),
  },
];

const mockConversations: Conversation[] = [
  {
    id: '1',
    name: 'South Park Episode',
    lastActivity: '2d ago',
    active: true,
  },
];

export const useStore = create<WeaveStore>((set) => ({
  // Tree state
  nodes: [],
  selectedNodeId: null,
  setSelectedNode: (id) => set({ selectedNodeId: id }),
  updateNode: (id, updates) =>
    set((state) => ({
      nodes: state.nodes.map((node) => (node.id === id ? { ...node, ...updates } : node)),
    })),
  addNode: (node) =>
    set((state) => ({
      nodes: [...state.nodes, node],
    })),

  // Chat state
  messages: [],
  addMessage: (message) =>
    set((state) => ({
      messages: [
        ...state.messages,
        {
          ...message,
          id: Math.random().toString(36).substr(2, 9),
          timestamp: new Date(),
        },
      ],
    })),
  clearMessages: () => set({ messages: [] }),

  // UI state
  activeTab: 'tree',
  setActiveTab: (tab) => set({ activeTab: tab }),

  activeAgent: 'Sub-1',
  setActiveAgent: (agent) => set({ activeAgent: agent }),

  conversations: mockConversations,

  // Layout state
  leftPanelWidth: 400,
  setLeftPanelWidth: (width) => set({ leftPanelWidth: width }),

  // Weave Backend Integration
  weave: {
    currentAgentLevel: 1,
    entrySessionId: null,
    entryOutput: null,
    characterId: null,
    characterCheckpoints: [],
    sceneProjectId: null,
    isProcessing: false,
    error: null,
  },

  setCurrentAgentLevel: (level) =>
    set((state) => ({
      weave: { ...state.weave, currentAgentLevel: level },
    })),

  setEntrySessionId: (id) =>
    set((state) => ({
      weave: { ...state.weave, entrySessionId: id },
    })),

  setEntryOutput: (output) =>
    set((state) => ({
      weave: { ...state.weave, entryOutput: output },
    })),

  setCharacterId: (id) =>
    set((state) => ({
      weave: { ...state.weave, characterId: id },
    })),

  addCharacterCheckpoint: (checkpoint) =>
    set((state) => ({
      weave: {
        ...state.weave,
        characterCheckpoints: [...state.weave.characterCheckpoints, checkpoint],
      },
    })),

  setSceneProjectId: (id) =>
    set((state) => ({
      weave: { ...state.weave, sceneProjectId: id },
    })),

  setProcessing: (isProcessing) =>
    set((state) => ({
      weave: { ...state.weave, isProcessing },
    })),

  setError: (error) =>
    set((state) => ({
      weave: { ...state.weave, error },
    })),

  // Initialize the agent tree structure based on AgentLevel enum
  initializeAgentTree: () =>
    set(() => ({
      nodes: [
        {
          id: 'agent-1',
          name: 'Entry Agent',
          status: 'active',
          progress: 0,
          description: 'Gathering story concept and characters',
          importance: 'Starting point for video creation',
          agentLevel: 1,
        },
        {
          id: 'agent-2',
          name: 'Character Identity',
          status: 'pending',
          progress: 0,
          parent: 'agent-1',
          description: 'Deep character development in 3 waves with 7 checkpoints',
          importance: 'Builds consistent character profiles',
          agentLevel: 2,
        },
        {
          id: 'agent-3',
          name: 'Scene Creator',
          status: 'pending',
          progress: 0,
          parent: 'agent-2',
          description: 'Refine scenes with cinematography details',
          importance: 'Production-ready scene descriptions',
          agentLevel: 3,
        },
      ],
    })),
}));
