"use client"

import { useEffect, useRef, useState } from "react"
import { chatKitOptions } from "@/lib/chatkit-config"

declare global {
  namespace JSX {
    interface IntrinsicElements {
      'openai-chatkit': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & {
        options?: string;
      }, HTMLElement>;
    }
  }
}

export function Chatbot() {
  const chatkitRef = useRef<any>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    console.log("[v0] Chatbot component mounted")
    console.log("[v0] ChatKit options:", chatKitOptions)

    // Since @openai/chatkit is a dependency, it should be loaded automatically by Next.js.
    // We only need to set the options once the custom element is available.
    const initializeChatKit = () => {
      if (chatkitRef.current) {
        console.log("[v0] Setting ChatKit options...")
        chatkitRef.current.setOptions(chatKitOptions)
        setIsLoading(false)
        console.log("[v0] ChatKit initialized successfully")
      } else {
        // Fallback or retry if element is not immediately available (shouldn't happen with Next.js)
        const timeout = setTimeout(initializeChatKit, 100)
        return () => clearTimeout(timeout)
      }
    }

    initializeChatKit()
  }, [])

  if (error) {
    return (
      <div className="flex items-center justify-center h-full min-h-screen bg-[#212121] text-white">
        <div className="text-center">
          <h2 className="text-xl font-semibold mb-2">خطأ في تحميل المساعد</h2>
          <p className="text-gray-400">{error}</p>
        </div>
      </div>
    )
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-full min-h-screen bg-[#212121] text-white">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
          <p className="text-gray-400">جاري تحميل المساعد...</p>
        </div>
      </div>
    )
  }

  return (
    <openai-chatkit
      ref={chatkitRef}
      className="w-full h-full min-h-screen"
      style={{
        direction: "rtl",
        fontFamily: "Inter, sans-serif",
      }}
    />
  )
}
