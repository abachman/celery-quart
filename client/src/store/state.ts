import { createContext } from 'react'
import { ChatMessage, ChatState, StreamResponse } from './models'

type ChatActions =
  | { type: 'ADD_MESSAGE'; payload: ChatMessage }
  | { type: 'CLEAR_ERROR' }
  | { type: 'RESET' }
  | { type: 'SET_ERROR'; payload: string }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SAVE_ANSWER' }
  | { type: 'UPDATE_ANSWER'; payload: StreamResponse }

export const ChatContext = createContext<ChatState>({
  messages: [],
})

export const ChatDispatchContext = createContext<React.Dispatch<ChatActions>>(
  () => {},
)

export const chatReducer: React.Reducer<ChatState, ChatActions> = (
  state,
  action,
) => {
  switch (action.type) {
    case 'ADD_MESSAGE':
      return {
        ...state,
        messages: [...state.messages, action.payload],
      }
    case 'SET_LOADING':
      return {
        ...state,
        loading: action.payload,
      }
    case 'SET_ERROR':
      return {
        ...state,
        error: action.payload,
      }
    case 'CLEAR_ERROR':
      return {
        ...state,
        error: undefined,
      }
    case 'UPDATE_ANSWER':
      return {
        ...state,
        answer: (state.answer || '') + action.payload.message.content,
      }
    case 'SAVE_ANSWER':
      return {
        ...state,
        messages: [
          ...state.messages,
          { role: 'assistant', content: state.answer || '' },
        ],
        answer: undefined,
      }
    case 'RESET':
      return {
        messages: [],
        loading: false,
        error: undefined,
        answer: undefined,
      }
    default:
      return state
  }
}
