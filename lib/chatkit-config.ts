import type { ChatKitOptions } from "@openai/chatkit"





export const chatKitOptions: ChatKitOptions = {
  api: {
    url: `/api/chat`,
    headers: {
      "Content-Type": "application/json",
    },
    upload: {
      url: `/api/upload`,
      headers: {
        "Content-Type": "multipart/form-data",
      },
    },
  },
  theme: {
    colorScheme: "dark",
    radius: "pill",
    density: "compact",
    color: {
      grayscale: {
        hue: 0,
        tint: 0,
      },
      accent: {
        primary: "#ffffff",
        level: 1,
      },
      surface: {
        background: "#212121",
        foreground: "#303030",
      },
    },
    typography: {
      baseSize: 14,
      fontFamily: "Inter, sans-serif",
      fontSources: [
        {
          family: "Inter",
          src: "https://rsms.me/inter/font-files/Inter-Regular.woff2",
          weight: 400,
          style: "normal",
        },
        {
          family: "Inter",
          src: "https://rsms.me/inter/font-files/Inter-Medium.woff2",
          weight: 500,
          style: "normal",
        },
        {
          family: "Inter",
          src: "https://rsms.me/inter/font-files/Inter-SemiBold.woff2",
          weight: 600,
          style: "normal",
        },
        {
          family: "Inter",
          src: "https://rsms.me/inter/font-files/Inter-Bold.woff2",
          weight: 700,
          style: "normal",
        },
      ],
    },
  },
  composer: {
    attachments: {
      enabled: true,
      maxCount: 5,
      maxSize: 10485760, // 10MB
    },
    tools: [
      {
        id: "search_docs",
        label: "Search docs",
        shortLabel: "DeepThink",
        placeholderOverride: "Search documentation",
        icon: "atom",
        pinned: true,
      },
      {
        id: "web_search",
        label: "Web Search",
        shortLabel: "Web",
        icon: "globe",
        pinned: false,
      },
    ],
    models: [
      {
        id: "gpt-4o",
        label: "Crisp",
        description: "Concise and factual",
      },
      {
        id: "gpt-4o-mini",
        label: "Friendly",
        description: "Warm and helpful",
      },
      {
        id: "gpt-5",
        label: "Professional",
        description: "Formal and detailed",
      },
    ],
  },
  startScreen: {
    greeting: "مرحباً! كيف يمكنني مساعدتك اليوم؟",
    prompts: [
      {
        icon: "circle-question",
        label: "What is ChatKit?",
        prompt: "What is ChatKit and what does it do?",
      },
      {
        icon: "rocket",
        label: "Get Started",
        prompt: "How do I get started with ChatKit?",
      },
      {
        icon: "code",
        label: "Integration",
        prompt: "How do I integrate ChatKit into my website?",
      },
      {
        icon: "palette",
        label: "Customization",
        prompt: "How can I customize the appearance of ChatKit?",
      },
      {
        icon: "gear",
        label: "Configuration",
        prompt: "What configuration options are available?",
      },
      {
        icon: "shield",
        label: "Security",
        prompt: "How is security handled in ChatKit?",
      },
      {
        icon: "chart-line",
        label: "Analytics",
        prompt: "What analytics features are available?",
      },
      {
        icon: "life-ring",
        label: "Support",
        prompt: "How can I get support for ChatKit?",
      },
    ],
  },
  locale: "ar",
  header: {
    title: "المساعد الافتراضي",
    subtitle: "كيف يمكنني مساعدتك؟",
  },
  threadItemActions: {
    enabled: true,
    copy: true,
    edit: true,
    retry: true,
    delete: true,
  },
}
