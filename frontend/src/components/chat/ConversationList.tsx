import { useState } from 'react';
import { useStore } from '../../store/useStore';

interface ConversationListProps {
  onNewProject: () => void;
}

export function ConversationList({ onNewProject }: ConversationListProps) {
  const { conversations } = useStore();
  const [hoveredId, setHoveredId] = useState<string | null>(null);

  return (
    <div className="mb-6">
      <div className="flex items-center justify-between mb-2">
        <span className="text-[10px] font-semibold text-text-tertiary uppercase tracking-wider">
          Projects
        </span>
        <button
          onClick={onNewProject}
          className="text-text-tertiary hover:text-text-primary transition-colors"
          title="New Project (⌘N)"
        >
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <path d="M7 2V12M2 7H12" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
          </svg>
        </button>
      </div>

      <div className="space-y-0.5">
        {conversations.map((conv) => (
          <div
            key={conv.id}
            onMouseEnter={() => setHoveredId(conv.id)}
            onMouseLeave={() => setHoveredId(null)}
            className="relative group"
          >
            <button
              className={`w-full h-8 px-2 rounded-md flex items-center gap-2 text-sm transition-all ${
                conv.active
                  ? 'bg-status-active/15 text-text-primary'
                  : 'hover:bg-bg-tertiary text-text-secondary hover:text-text-primary'
              }`}
            >
              <svg width="14" height="14" viewBox="0 0 14 14" fill="none" className="flex-shrink-0 opacity-60">
                <rect x="2" y="2" width="10" height="10" rx="2" stroke="currentColor" strokeWidth="1.5"/>
                <line x1="4" y1="5" x2="10" y2="5" stroke="currentColor" strokeWidth="1.5"/>
                <line x1="4" y1="7.5" x2="8" y2="7.5" stroke="currentColor" strokeWidth="1.5"/>
              </svg>
              <span className="truncate flex-1 text-left">{conv.name}</span>
              <span className="text-[10px] text-text-tertiary flex-shrink-0">{conv.lastActivity}</span>
            </button>

            {hoveredId === conv.id && (
              <div className="absolute right-1 top-1 flex items-center gap-0.5 bg-bg-secondary/95 rounded px-1">
                <button
                  className="p-1 hover:bg-bg-tertiary rounded transition-colors"
                  title="More options"
                >
                  <svg width="12" height="12" viewBox="0 0 12 12" fill="none" className="text-text-tertiary">
                    <circle cx="6" cy="2" r="1" fill="currentColor"/>
                    <circle cx="6" cy="6" r="1" fill="currentColor"/>
                    <circle cx="6" cy="10" r="1" fill="currentColor"/>
                  </svg>
                </button>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
