import { useReducer } from 'react'
import { chatReducer, ChatContext, ChatDispatchContext } from './state'

export const ChatProvider = ({ children }: { children: React.ReactNode }) => {
  const [state, dispatch] = useReducer(chatReducer, { messages: [] })

  // separate providers for state and dispatch means components that dispatch
  // but don't use state don't need to re-render when state changes
  return (
    <ChatContext.Provider value={state}>
      <ChatDispatchContext.Provider value={dispatch}>
        {children}
      </ChatDispatchContext.Provider>
    </ChatContext.Provider>
  )
}
