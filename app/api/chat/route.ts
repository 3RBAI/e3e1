import { type NextRequest, NextResponse } from "next/server"
import OpenAI from "openai"

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
})

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { messages, model = "gpt-4o", tools } = body

    // Handle tool calls if present
    const toolDefinitions = tools
      ?.map((tool: any) => {
        if (tool.id === "search_docs") {
          return {
            type: "function",
            function: {
              name: "search_docs",
              description: "Search through documentation",
              parameters: {
                type: "object",
                properties: {
                  query: {
                    type: "string",
                    description: "The search query",
                  },
                },
                required: ["query"],
              },
            },
          }
        }
        if (tool.id === "web_search") {
          return {
            type: "function",
            function: {
              name: "web_search",
              description: "Search the web",
              parameters: {
                type: "object",
                properties: {
                  query: {
                    type: "string",
                    description: "The search query",
                  },
                },
                required: ["query"],
              },
            },
          }
        }
        return null
      })
      .filter(Boolean)

    const completion = await openai.chat.completions.create({
      model,
      messages,
      tools: toolDefinitions?.length ? toolDefinitions : undefined,
      stream: true,
    })

    const encoder = new TextEncoder()
    const stream = new ReadableStream({
      async start(controller) {
        try {
          for await (const chunk of completion) {
            const text = chunk.choices[0]?.delta?.content || ""
            const toolCalls = chunk.choices[0]?.delta?.tool_calls

            if (text) {
              controller.enqueue(encoder.encode(`data: ${JSON.stringify({ content: text })}\n\n`))
            }

            if (toolCalls) {
              controller.enqueue(encoder.encode(`data: ${JSON.stringify({ tool_calls: toolCalls })}\n\n`))
            }
          }
          controller.enqueue(encoder.encode("data: [DONE]\n\n"))
          controller.close()
        } catch (error) {
          controller.error(error)
        }
      },
    })

    return new Response(stream, {
      headers: {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        Connection: "keep-alive",
      },
    })
  } catch (error) {
    console.error("Chat API error:", error)
    return NextResponse.json({ error: "Failed to process chat request" }, { status: 500 })
  }
}
