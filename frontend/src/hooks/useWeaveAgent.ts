/**
 * Custom hook to manage Weave agent interactions and tree updates
 */

import { useEffect, useCallback } from 'react';
import { useStore } from '../store/useStore';
import { entryAgent, characterAgent, type EntryAgentOutput } from '../services/weaveApi';
import { CharacterWebSocket } from '../services/websocket';

export function useWeaveAgent() {
  const {
    weave,
    setEntrySessionId,
    setEntryOutput,
    setCharacterId,
    addCharacterCheckpoint,
    setCurrentAgentLevel,
    updateNode,
    addNode,
    setProcessing,
    setError,
    addMessage,
  } = useStore();

  /**
   * Start Entry Agent session
   */
  const startEntryAgent = useCallback(async () => {
    try {
      setProcessing(true);
      setError(null);

      const response = await entryAgent.start();
      setEntrySessionId(response.session_id);

      updateNode('agent-1', {
        status: 'active',
        metadata: { sessionId: response.session_id },
      });

      addMessage({
        type: 'agent',
        content: response.message,
      });

      setProcessing(false);
      return response.session_id;
    } catch (error) {
      console.error('Failed to start entry agent:', error);
      setError('Failed to start entry agent');
      setProcessing(false);
      throw error;
    }
  }, [setProcessing, setError, setEntrySessionId, updateNode, addMessage]);

  /**
   * Send message to Entry Agent
   */
  const sendToEntryAgent = useCallback(
    async (message: string) => {
      if (!weave.entrySessionId) {
        // Auto-start if not already started
        await startEntryAgent();
      }

      try {
        setProcessing(true);
        addMessage({ type: 'user', content: message });

        const response = await entryAgent.chat(weave.entrySessionId!, message);

        addMessage({
          type: 'agent',
          content: response.response,
        });

        // Check if Entry Agent is complete
        if (response.is_final && response.output) {
          setEntryOutput(response.output);
          updateNode('agent-1', {
            status: 'completed',
            progress: 100,
          });

          // Unlock Character Identity agent
          updateNode('agent-2', {
            status: 'pending',
          });

          setCurrentAgentLevel(2);
        } else {
          // Update progress based on conversation
          const estimatedProgress = Math.min(
            (weave.entryOutput ? 50 : 0) + message.length / 20,
            90
          );
          updateNode('agent-1', {
            progress: estimatedProgress,
          });
        }

        setProcessing(false);
        return response;
      } catch (error) {
        console.error('Failed to send message to entry agent:', error);
        setError('Failed to send message');
        setProcessing(false);
        throw error;
      }
    },
    [
      weave.entrySessionId,
      weave.entryOutput,
      startEntryAgent,
      setProcessing,
      addMessage,
      setEntryOutput,
      updateNode,
      setCurrentAgentLevel,
      setError,
    ]
  );

  /**
   * Start Character Identity development
   */
  const startCharacterDevelopment = useCallback(
    async (entryOutput: EntryAgentOutput) => {
      try {
        setProcessing(true);
        setError(null);

        updateNode('agent-2', {
          status: 'active',
          progress: 0,
        });

        const response = await characterAgent.start({
          characters: entryOutput.characters,
          storyline: entryOutput.storyline,
          mode: 'balanced',
        });

        setCharacterId(response.character_id);

        updateNode('agent-2', {
          metadata: { characterId: response.character_id },
        });

        // Create checkpoint sub-nodes
        for (let i = 1; i <= response.checkpoint_count; i++) {
          addNode({
            id: `checkpoint-${i}`,
            name: `Checkpoint ${i}`,
            status: 'pending',
            parent: 'agent-2',
            checkpointNumber: i,
            agentLevel: 2,
          });
        }

        // Connect to WebSocket for real-time updates
        const ws = new CharacterWebSocket(
          response.character_id,
          (message) => {
            switch (message.type) {
              case 'wave_started':
                addMessage({
                  type: 'action',
                  content: `Wave ${message.wave} started: ${message.agents.join(', ')}`,
                });
                break;

              case 'checkpoint_ready':
                updateNode(`checkpoint-${message.checkpoint}`, {
                  status: 'active',
                });
                // Fetch checkpoint data
                characterAgent
                  .getCheckpoint(response.character_id, message.checkpoint)
                  .then((checkpoint) => {
                    addCharacterCheckpoint(checkpoint);
                    updateNode(`checkpoint-${message.checkpoint}`, {
                      status: 'completed',
                      description: checkpoint.output.narrative.substring(0, 150) + '...',
                    });
                  });
                break;

              case 'wave_complete':
                const progress = (message.wave / 3) * 100;
                updateNode('agent-2', { progress });
                break;

              case 'character_complete':
                updateNode('agent-2', {
                  status: 'completed',
                  progress: 100,
                });
                updateNode('agent-3', {
                  status: 'pending',
                });
                setCurrentAgentLevel(3);
                addMessage({
                  type: 'agent',
                  content: 'Character development complete! Ready for scene creation.',
                });
                ws.disconnect();
                break;

              case 'error':
                setError(message.message);
                break;
            }
          },
          (error) => {
            console.error('WebSocket error:', error);
          }
        );

        ws.connect();

        setProcessing(false);
      } catch (error) {
        console.error('Failed to start character development:', error);
        setError('Failed to start character development');
        setProcessing(false);
        throw error;
      }
    },
    [
      setProcessing,
      setError,
      updateNode,
      setCharacterId,
      addNode,
      addMessage,
      addCharacterCheckpoint,
      setCurrentAgentLevel,
    ]
  );

  return {
    startEntryAgent,
    sendToEntryAgent,
    startCharacterDevelopment,
    currentLevel: weave.currentAgentLevel,
    isProcessing: weave.isProcessing,
    error: weave.error,
    entryOutput: weave.entryOutput,
  };
}
