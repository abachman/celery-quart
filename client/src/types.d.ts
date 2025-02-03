// this permits the for await (const chunk of response.body), which is legal in
// contemporary browsers.

// eslint-disable-next-line @typescript-eslint/no-explicit-any
interface ReadableStream<R = any> {
  [Symbol.asyncIterator](): AsyncIterableIterator<R>
}
