"use client"

import { useEffect, useRef } from "react"
import { chatKitOptions } from "@/lib/chatkit-config"

export function Chatbot() {
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // Dynamically load ChatKit script
    const script = document.createElement("script")
    script.src = "https://cdn.jsdelivr.net/npm/@openai/chatkit@latest/dist/chatkit.umd.js"
    script.async = true

    script.onload = () => {
      if (containerRef.current && (window as any).ChatKit) {
        // Initialize ChatKit
        ;(window as any).ChatKit.mount(containerRef.current, chatKitOptions)
      }
    }

    document.body.appendChild(script)

    return () => {
      // Cleanup
      if (document.body.contains(script)) {
        document.body.removeChild(script)
      }
    }
  }, [])

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
