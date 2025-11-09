import { useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { useStore } from '../../store/useStore';

export function ChatInput() {
  const { addMessage, selectedNodeId, nodes } = useStore();
  const [input, setInput] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);

  const selectedNode = nodes.find((n) => n.id === selectedNodeId);

  // Anthropic 429 Rate Limit Error - exact error message
  const ANTHROPIC_429_ERROR = `Error code: 429 - {'type': 'error', 'error': {'type': 'rate_limit_error', 'message': 'Number of request tokens has exceeded your per-minute rate limit (https://docs.anthropic.com/en/api/rate-limits); see the response headers for current usage. Please reduce the prompt length or the maximum tokens requested, or try again later. You may also contact sales at https://www.anthropic.com/contact-sales to discuss your options for a rate limit increase.'}}`;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isProcessing) return;

    const message = input.trim();
    setInput('');
    setIsProcessing(true);

    // Add user message
    addMessage({
      type: 'user',
      content: message,
    });

    // Simulate a brief delay for realism
    setTimeout(() => {
      // Add automatic 429 error response
      addMessage({
        type: 'agent',
        content: ANTHROPIC_429_ERROR,
      });
      setIsProcessing(false);
    }, 800);
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
