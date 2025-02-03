////////////////////////////
// Chat State
export type ChatMessage = {
  role: string
  content: string
}

export type ChatState = {
  messages: ChatMessage[]
  loading?: boolean
  error?: string
  answer?: string
}

////////////////////////////
// API Request
export type GenerateRequest = {
  // system: str | None = None
  system?: string
  // model: str = "llama3.2"
  model?: string
  // conversation: Conversation = Conversation(messages=[])
  conversation?: { messages: ChatMessage[] }
  // prompt: str
  prompt: string
}

////////////////////////////
// API Response
export type StreamDelta = {
  role: string
  content: string
}

export type StreamResponse = {
  message: StreamDelta
  done: boolean
  done_reason: string
}
