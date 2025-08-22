import json
import os
from openai import OpenAI

# 设置客户端
client = OpenAI(
    api_key="sk-ngwOcq4h7reY7qL7jQeOVkmZhWCg9Xh95ilq2NkXIsArpQRC",
    base_url="https://api.moonshot.cn/v1"
)


# 模型配置
MODEL = "kimi-k2-0711-preview"

def generate_lit_review(topic: str, major: str):

    messages = [
        {
            "role": "system",
            "content": ("""
You are tasked with creating a structured outline for a literature review on a given topic in Simplified Chinese. This outline will serve as a framework for further research and writing. Your goal is to generate a comprehensive structure that covers the research background, gaps in current research, main research directions, and regional comparisons.

The topic for the literature review is:
<topic>
{{TOPIC}}
</topic>

Before generating the final output, use a scratchpad to think through the structure and content for each section. Consider the following:
- What is the current state of research on this topic?
- What are the main gaps or limitations in existing research?
- What are the primary research directions within this field?
- How does research in this area differ between domestic and international contexts?

Once you have thought through these elements, generate the outline using the following XML structure. Provide brief, placeholder content for each section to guide further research and writing:

<framework>
<f-title>{{Title}}</f-title>
<!-- 3. Research Background (Abstract Framework) -->
<f-background>
  <f-research-status>
    <!-- Provide a brief overview of the current research status -->
  </f-research-status>
  <f-literature-map>
    <!-- Describe the main themes and relationships within the topic -->
  </f-literature-map>
</f-background>

<!-- 4. Research Gaps (Abstract Framework) -->
<f-gaps>
  <f-gap-1>
    <!-- Describe the first major gap in current research -->
  </f-gap-1>
  <f-gap-2>
    <!-- Describe the second major gap in current research -->
  </f-gap-2>
  <!-- Add more gap elements if necessary -->
</f-gaps>

<!-- 5. Main Directions (Abstract Framework) -->
<f-directions>
  <f-direction>
    <f-scope>
      <!-- Name and describe the scope of the first main research direction -->
    </f-scope>
    <f-inherent-limitations>
      <!-- Outline the inherent limitations of this research direction -->
    </f-inherent-limitations>
  </f-direction>
  <!-- Add more direction elements if necessary -->
</f-directions>

<!-- 6. Regional Comparison (Abstract Framework) -->
<f-regional-comparison>
  <f-domestic>
    <!-- Summarize the state of domestic research on the topic -->
  </f-domestic>
  <f-international>
    <!-- Summarize the state of international research on the topic -->
  </f-international>
</f-regional-comparison>
</output>

Ensure that each section contains relevant placeholder content that can guide further research and writing. The content should be concise yet informative, providing a clear direction for the literature review.
                        
NOTE!!! It is strictly forbidden to output any other text outside the given XML framework!!!
"""
            )
        },
        {
            "role": "user",
            "content": "<topic>{{" + topic + "}}</topic>" + 
"<major>{{" + major + "}}</major>"
        }
    ]

    tools = [
        {
            "type": "builtin_function",
            "function": {
                "name": "$web_search"
            }
        }
    ]

    # 第一次调用：触发联网搜索（流式输出）
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        temperature=0.3,
        stream=True  # 开启流式输出
    )

    # 处理流式响应
    tool_calls = []
    for chunk in response:
        if chunk.choices[0].delta.tool_calls:
            tool_calls.extend(chunk.choices[0].delta.tool_calls)
        
        # 如果有完整的工具调用，处理它
        if chunk.choices[0].finish_reason == "tool_calls":
            break
    
    # 处理工具调用
    if tool_calls:
        # 重构完整的tool_call对象
        tool_call = tool_calls[0]  # 假设只有一个工具调用
        messages.append({
            "role": "assistant",
            "content": "",
            "tool_calls": [tool_call]
        })

        # 提交工具结果（Kimi 会自动执行搜索）
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(tool_call.function.arguments)
        })

        # 第二次调用：获取最终综述（流式输出）
        final_response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.3,
            stream=True  # 开启流式输出
        )

        # 流式处理最终响应
        full_content = ""
        for chunk in final_response:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)  # 实时输出
                full_content += content
        
        print()  # 换行
        return full_content
    
    return "未能获取到有效响应"

# 示例运行
if __name__ == "__main__":
    
    topic = "PySpark 在大规模商业数据分析中的实践"
    major = "数据科学与大数据技术"

    print(f"正在生成关于'{topic}'的文献综述...\n---\n")
    review = generate_lit_review(topic, major)

    print("\n\n=== 完整综述 ===")
    print(review)