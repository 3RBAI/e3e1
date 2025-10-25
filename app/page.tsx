import { Chatbot } from "@/components/chatbot"

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-[#212121]">
      <div className="w-full h-screen max-w-7xl mx-auto">
        <Chatbot />
      </div>
    </main>
  )
}
