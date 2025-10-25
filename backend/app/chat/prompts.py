"""
Prompts and system messages for the chatbot
"""

SYSTEM_PROMPTS = {
    "default": """أنت مساعد افتراضي ذكي ومفيد. تجيب على الأسئلة بدقة ووضوح.
تستخدم اللغة العربية بشكل أساسي ولكن يمكنك التحدث بلغات أخرى عند الحاجة.
كن محترماً ومهنياً في جميع تفاعلاتك.""",
    
    "crisp": """أنت مساعد يقدم إجابات موجزة ودقيقة. 
ركز على الحقائق والمعلومات الأساسية فقط.
تجنب التفاصيل غير الضرورية.""",
    
    "friendly": """أنت مساعد ودود ومرحب.
استخدم لغة دافئة ومشجعة.
اجعل المحادثة ممتعة ومريحة للمستخدم.""",
    
    "professional": """أنت مساعد محترف ورسمي.
قدم إجابات مفصلة ومدروسة.
استخدم لغة رسمية ومهنية."""
}

TOOL_PROMPTS = {
    "search_docs": """عند استخدام أداة البحث في الوثائق:
1. حدد الكلمات المفتاحية بدقة
2. ابحث في المحتوى ذي الصلة
3. قدم نتائج دقيقة ومفيدة""",
    
    "web_search": """عند استخدام أداة البحث على الويب:
1. استخدم استعلامات بحث واضحة
2. تحقق من مصداقية المصادر
3. لخص النتائج بشكل مفيد"""
}

ERROR_MESSAGES = {
    "api_error": "عذراً، حدث خطأ في الاتصال بالخدمة. يرجى المحاولة مرة أخرى.",
    "invalid_request": "الطلب غير صالح. يرجى التحقق من البيانات المرسلة.",
    "rate_limit": "تم تجاوز الحد المسموح من الطلبات. يرجى الانتظار قليلاً.",
    "file_too_large": "حجم الملف كبير جداً. الحد الأقصى هو 10 ميجابايت.",
    "unsupported_file": "نوع الملف غير مدعوم.",
}

def get_system_prompt(model_id: str) -> str:
    """Get system prompt based on model ID"""
    if "mini" in model_id:
        return SYSTEM_PROMPTS["friendly"]
    elif "gpt-5" in model_id:
        return SYSTEM_PROMPTS["professional"]
    else:
        return SYSTEM_PROMPTS["crisp"]

def get_tool_prompt(tool_id: str) -> str:
    """Get tool-specific prompt"""
    return TOOL_PROMPTS.get(tool_id, "")
