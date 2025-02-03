import { useContext } from 'react'
import { ChatContext, ChatDispatchContext } from './state'
import { generateStream } from '../api/chat'
import { GenerateRequest } from './models'

export const useChat = () => {
  return useContext(ChatContext)
}

export const useChatDispatch = () => {
  return useContext(ChatDispatchContext)
}

export const useStreamingChat = () => {
  const dispatch = useChatDispatch()

  return {
    add: (message: string) => {
      dispatch({
        type: 'ADD_MESSAGE',
        payload: { role: 'user', content: message },
      })
    },
    send: async (request: GenerateRequest) => {
      dispatch({ type: 'SET_LOADING', payload: true })
      for await (const chunk of generateStream(request)) {
        dispatch({
          type: 'UPDATE_ANSWER',
          payload: chunk,
        })
      }
      dispatch({ type: 'SET_LOADING', payload: false })
      dispatch({
        type: 'SAVE_ANSWER',
      })
    },
  }
}
