import { useEffect, useRef } from 'react'
import { ChatProvider } from './store/ChatProvider'
import { useChat, useStreamingChat } from './store/hooks'
import { ChatMessage } from './store/models'
import { Converter } from 'showdown'

export const App = () => {
  return (
    <ChatProvider>
      <Main>
        <Header />
        <Messages />
        <Prompt />
      </Main>
    </ChatProvider>
  )
}

const Main = ({ children }: { children: React.ReactNode }) => {
  return (
    <main className="grid h-screen w-screen grid-rows-[auto_1fr_auto] overflow-hidden">
      {children}
    </main>
  )
}

const Header = () => {
  return (
    <header className="bg-teal-400">
      <nav className="flex w-full justify-between bg-linear-to-r from-cyan-500 to-blue-500 p-4 text-white">
        <a href="#">
          <span className="text-xl font-semibold tracking-tight">Chat</span>
        </a>
      </nav>
    </header>
  )
}

type MessageProps = {
  message: ChatMessage
  loading?: boolean
}

const converter = new Converter()

const UserMessage = ({ message }: MessageProps) => {
  return (
    <div className="flex items-end justify-end">
      <div className="mx-2 flex max-w-lg flex-col items-end space-y-2 text-xs">
        <div>
          <span className="inline-block rounded-lg rounded-br-none bg-blue-600 px-4 py-2 text-base text-white">
            {message.content}
          </span>
        </div>
      </div>
    </div>
  )
}

const AssistantMessage = ({ message, loading }: MessageProps) => {
  return (
    <div className="flex items-end">
      <div className="mx-2 flex max-w-lg flex-col items-start space-y-2 text-xs">
        <div>
          <div
            className="inline-block rounded-lg rounded-bl-none bg-gray-300 px-4 py-2 text-base text-gray-600"
            dangerouslySetInnerHTML={{
              __html: converter.makeHtml(message.content),
            }}
          ></div>
        </div>
        {loading && (
          <div className="flex items-center space-x-2">
            <div className="h-3 w-3 animate-ping rounded-full bg-blue-400"></div>
            <div className="h-3 w-3 animate-ping rounded-full bg-blue-400"></div>
            <div className="h-3 w-3 animate-ping rounded-full bg-blue-400"></div>
          </div>
        )}
      </div>
    </div>
  )
}

const Messages = () => {
  const { messages, answer, loading } = useChat()
  const scrollto = useRef<HTMLDivElement>(null)

  useEffect(() => {
    scrollto.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  return (
    <div
      id="messages"
      className="scrollbar-thumb-blue scrollbar-thumb-rounded scrollbar-track-blue-lighter scrollbar-w-2 scrolling-touch flex flex-col space-y-4 overflow-y-auto p-3"
    >
      {messages.map((message, index) => {
        if (message.role === 'user') {
          return <UserMessage key={index} message={message} />
        } else {
          return <AssistantMessage key={index} message={message} />
        }
      })}

      {answer && (
        <AssistantMessage
          message={{ role: 'assistant', content: answer }}
          loading={true}
        />
      )}

      <div id="scroll-to" ref={scrollto}></div>
    </div>
  )
}

const Prompt = () => {
  const input = useRef<HTMLInputElement>(null)
  const { add, send } = useStreamingChat()
  const { messages } = useChat()

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()

    if (input.current) {
      add(input.current.value || '')
      await send({ prompt: input.current.value, conversation: { messages } })
      input.current.value = ''
    }
  }

  return (
    <div className="px-4 pt-4 pb-2 sm:mb-0">
      <form
        onSubmit={e => {
          console.log('submit')
          handleSubmit(e)
        }}
      >
        <div className="relative flex">
          <input
            type="text"
            placeholder="Write your message!"
            ref={input}
            className="w-full rounded-l-md bg-gray-200 py-3 pl-4 text-gray-900 placeholder-gray-600 focus:placeholder-gray-400 focus:outline-none"
          />
          <SendButton />
        </div>
      </form>
    </div>
  )
}

const SendButton = () => {
  return (
    <button
      type="submit"
      title="Send"
      className="inline-flex items-center justify-center rounded-r-md bg-gray-200 px-4 py-3 text-white hover:cursor-pointer hover:bg-slate-300 focus:outline-none"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 20 20"
        fill="black"
        className="ml-2 h-6 w-6 rotate-90 transform"
      >
        <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z"></path>
      </svg>
    </button>
  )
}
