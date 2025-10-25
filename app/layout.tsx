import type React from "react"
import type { Metadata } from "next"
import { Analytics } from "@vercel/analytics/next"
import "@fontsource/geist-sans/400.css"
import "@fontsource/geist-sans/700.css"
import "@fontsource/geist-mono/400.css"
import "@fontsource/geist-mono/700.css"
import "./globals.css"

export const metadata: Metadata = {
  title: "ChatKit - المساعد الافتراضي",
  description: "مساعد ذكي مدعوم بالذكاء الاصطناعي",
  generator: "v0.app",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="ar" dir="rtl">
      <body className="font-sans antialiased">
        {children}
        <Analytics />
      </body>
    </html>
  )
}
