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

    let mounted = true

    const loadChatKit = async () => {
      try {
        console.log("[v0] Loading ChatKit from CDN...")
        
        // Load ChatKit script from CDN
        const script = document.createElement('script')
        script.src = 'https://cdn.jsdelivr.net/npm/@openai/chatkit@1.0.0/dist/index.js'
        script.type = 'module'
        script.async = true
        
        script.onload = () => {
          if (!mounted) return
          console.log("[v0] ChatKit script loaded successfully")
          
          // Wait a bit for the custom element to be registered
          setTimeout(() => {
            if (chatkitRef.current) {
              console.log("[v0] Setting ChatKit options...")
              chatkitRef.current.setOptions(chatKitOptions)
              setIsLoading(false)
              console.log("[v0] ChatKit initialized successfully")
            }
          }, 100)
        }
        
        script.onerror = () => {
          if (mounted) {
            console.error("[v0] Failed to load ChatKit script")
            setError("Failed to load chatbot library")
            setIsLoading(false)
          }
        }
        
        document.head.appendChild(script)
        
        return () => {
          document.head.removeChild(script)
        }
      } catch (err) {
        console.error("[v0] Error loading ChatKit:", err)
        if (mounted) {
          setError("Failed to load chatbot library")
          setIsLoading(false)
        }
      }
    }

    loadChatKit()

    return () => {
      mounted = false
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
