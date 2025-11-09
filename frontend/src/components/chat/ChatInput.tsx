import { useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { useStore } from '../../store/useStore';
import { useWeaveAgent } from '../../hooks/useWeaveAgent';

export function ChatInput() {
  const { addMessage, selectedNodeId, nodes, weave } = useStore();
  const { sendToEntryAgent, startCharacterDevelopment, isProcessing } = useWeaveAgent();
  const [input, setInput] = useState('');

  const selectedNode = nodes.find((n) => n.id === selectedNodeId);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isProcessing) return;

    const message = input.trim();
    setInput('');

    // Route message based on current agent level
    try {
      if (weave.currentAgentLevel === 1) {
        // Entry Agent
        const response = await sendToEntryAgent(message);
        
        // If Entry Agent completed, auto-start Character Development
        if (response.is_final && response.output) {
          await startCharacterDevelopment(response.output);
        }
      } else if (weave.currentAgentLevel === 2) {
        // Character Identity - show message but currently auto-running
        addMessage({
          type: 'user',
          content: message,
        });
        addMessage({
          type: 'agent',
          content: 'Character development is currently running. Please wait for checkpoints to complete.',
        });
      } else if (weave.currentAgentLevel === 3) {
        // Scene Creator
        addMessage({
          type: 'user',
          content: message,
        });
        addMessage({
          type: 'agent',
          content: 'Scene Creator integration coming soon!',
        });
      }
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  return (
    <div className="p-4 pt-2 border-t border-border-subtle">
      <form onSubmit={handleSubmit} className="relative">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type message..."
          className="w-full h-9 px-3 bg-bg-secondary border border-border-subtle rounded text-sm placeholder:text-text-tertiary focus:outline-none focus:border-status-active/50 transition-colors"
        />
        {!input && (
          <span className="absolute left-3 top-1/2 -translate-y-1/2 text-text-tertiary pointer-events-none">
            <span className="inline-block animate-blink">|</span>
          </span>
        )}
      </form>
    </div>
  );
}
