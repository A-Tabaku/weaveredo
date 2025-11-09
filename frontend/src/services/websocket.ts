/**
 * WebSocket Service for Real-time Character Development Updates
 */

import type { WebSocketMessageType } from './weaveApi';

const WS_BASE_URL = import.meta.env.VITE_APP_URL 
  ? import.meta.env.VITE_APP_URL.replace('https://', 'wss://').replace('http://', 'ws://')
  : 'ws://localhost:8000';

export class CharacterWebSocket {
  private ws: WebSocket | null = null;
  private pingInterval: number | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private shouldReconnect = true;

  constructor(
    private characterId: string,
    private onMessage: (msg: WebSocketMessageType) => void,
    private onError?: (error: Event) => void,
    private onClose?: () => void
  ) {}

  connect() {
    this.shouldReconnect = true;
    this.ws = new WebSocket(`${WS_BASE_URL}/ws/character/${this.characterId}`);

    this.ws.onopen = () => {
      console.log('[WS] Connected to character', this.characterId);
      this.reconnectAttempts = 0;

      // Start ping interval (every 30 seconds)
      this.pingInterval = window.setInterval(() => {
        if (this.ws?.readyState === WebSocket.OPEN) {
          this.ws.send('ping');
        }
      }, 30000);
    };

    this.ws.onmessage = (event) => {
      // Ignore pong responses
      if (event.data === 'pong') return;

      try {
        const message: WebSocketMessageType = JSON.parse(event.data);
        this.onMessage(message);
      } catch (e) {
        console.error('[WS] Parse error:', e);
      }
    };

    this.ws.onerror = (error) => {
      console.error('[WS] Error:', error);
      this.onError?.(error);
    };

    this.ws.onclose = () => {
      console.log('[WS] Closed');

      if (this.pingInterval) {
        clearInterval(this.pingInterval);
        this.pingInterval = null;
      }

      this.onClose?.();

      // Auto-reconnect with exponential backoff
      if (this.shouldReconnect && this.reconnectAttempts < this.maxReconnectAttempts) {
        const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
        console.log(`[WS] Reconnecting in ${delay}ms...`);
        setTimeout(() => this.connect(), delay);
        this.reconnectAttempts++;
      }
    };
  }

  disconnect() {
    this.shouldReconnect = false;
    if (this.pingInterval) {
      clearInterval(this.pingInterval);
    }
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}
