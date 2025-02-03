import { GenerateRequest, StreamResponse } from '../store/models'

const sendPrompt = async (request: GenerateRequest) => {
  return await fetch('/api/streaming/generate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  })
}

async function* responseStream(response: Response) {
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }

  if (!response.body) {
    throw new Error('No response body')
  }

  if (response.body) {
    for await (const chunk of response.body as unknown as ReadableStream<Uint8Array>) {
      const data = new TextDecoder('utf-8').decode(chunk)
      const lines = data.split('\n')

      for (const line of lines) {
        if (line.trim() === '') continue

        let data: StreamResponse | null = null
        try {
          data = JSON.parse(line)
        } catch (e) {
          console.error('error', e)
          continue
        }
        yield data as StreamResponse
      }
    }
  }
}

export async function* generateStream(request: GenerateRequest) {
  const response = await sendPrompt(request)
  yield* responseStream(response)
}
