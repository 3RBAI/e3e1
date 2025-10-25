"use client"

import { useEffect, useRef, useState } from "react"
import { chatKitOptions } from "@/lib/chatkit-config"

export function Chatbot() {
  const containerRef = useRef<HTMLDivElement>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    console.log("[v0] Chatbot component mounted")
    console.log("[v0] ChatKit options:", chatKitOptions)

    const script = document.createElement("script")
    script.src = "https://cdn.jsdelivr.net/npm/@openai/chatkit@1.0.0/dist/chatkit.umd.js"
    script.async = true

    script.onload = () => {
      console.log("[v0] ChatKit script loaded successfully")

      if (containerRef.current && (window as any).ChatKit) {
        try {
          console.log("[v0] Initializing ChatKit...")
          ;(window as any).ChatKit.mount(containerRef.current, chatKitOptions)
          setIsLoading(false)
          console.log("[v0] ChatKit mounted successfully")
        } catch (err) {
          console.error("[v0] Error mounting ChatKit:", err)
          setError("Failed to initialize chatbot")
          setIsLoading(false)
        }
      } else {
        console.error("[v0] ChatKit not available on window")
        setError("ChatKit library not loaded")
        setIsLoading(false)
      }
    }

    script.onerror = () => {
      console.error("[v0] Failed to load ChatKit script")
      setError("Failed to load chatbot library")
      setIsLoading(false)
    }

    document.body.appendChild(script)

    return () => {
      if (document.body.contains(script)) {
        document.body.removeChild(script)
      }
    }
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
    <div
      ref={containerRef}
      className="w-full h-full min-h-screen"
      style={{
        direction: "rtl",
        fontFamily: "Inter, sans-serif",
      }}
    />
  )
}
