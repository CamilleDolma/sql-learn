import xml.etree.ElementTree as ET
import json
import os
from openai import OpenAI
from typing import Dict, List, Any
import re
import sys
import time

# 设置客户端
client = OpenAI(
    api_key="sk-ngwOcq4h7reY7qL7jQeOVkmZhWCg9Xh95ilq2NkXIsArpQRC",
    base_url="https://api.moonshot.cn/v1"
)

MODEL = "kimi-k2-0711-preview"

class ProgressBar:
    def __init__(self, total_steps: int, width: int = 50):
        self.total_steps = total_steps
        self.current_step = 0
        self.width = width
        self.start_time = time.time()
        
    def update(self, step_description: str = ""):
        """更新进度条"""
        self.current_step += 1
        progress = self.current_step / self.total_steps
        filled_width = int(self.width * progress)
        
        # 计算已用时间和预估剩余时间
        elapsed_time = time.time() - self.start_time
        if self.current_step > 0:
            avg_time_per_step = elapsed_time / self.current_step
            remaining_steps = self.total_steps - self.current_step
            eta = avg_time_per_step * remaining_steps
        else:
            eta = 0
            
        # 格式化时间显示
        def format_time(seconds):
            if seconds < 60:
                return f"{seconds:.0f}s"
            elif seconds < 3600:
                return f"{seconds//60:.0f}m{seconds%60:.0f}s"
            else:
                return f"{seconds//3600:.0f}h{(seconds%3600)//60:.0f}m"
        
        # 构建进度条
        bar = '█' * filled_width + '░' * (self.width - filled_width)
        percentage = progress * 100
        
        # 清除当前行并打印新的进度条
        sys.stdout.write('\r')
        sys.stdout.write(f'进度: [{bar}] {percentage:.1f}% ({self.current_step}/{self.total_steps}) ')
        sys.stdout.write(f'用时: {format_time(elapsed_time)} ')
        if eta > 0:
            sys.stdout.write(f'剩余: {format_time(eta)} ')
        if step_description:
            sys.stdout.write(f'\n当前任务: {step_description}')
        sys.stdout.flush()
        
    def finish(self):
        """完成进度条"""
        total_time = time.time() - self.start_time
        sys.stdout.write('\n')
        print(f"✅ 所有检索任务完成！总用时: {total_time/60:.1f}分钟")

class FrameworkProcessor:
    def __init__(self):
        self.reference_counter = 1
        self.references = {}
        
    def parse_framework(self, framework_path: str) -> Dict[str, Any]:
        """解析framework.xml文件"""
        tree = ET.parse(framework_path)
        root = tree.getroot()
        
        framework_data = {
            'title': root.find('f-title').text if root.find('f-title') is not None else '',
            'background': {
                'research_status': root.find('.//f-research-status').text if root.find('.//f-research-status') is not None else '',
                'literature_map': root.find('.//f-literature-map').text if root.find('.//f-literature-map') is not None else ''
            },
            'gaps': [],
            'directions': [],
            'regional_comparison': {
                'domestic': root.find('.//f-domestic').text if root.find('.//f-domestic') is not None else '',
                'international': root.find('.//f-international').text if root.find('.//f-international') is not None else ''
            }
        }
        
        # 解析研究空白
        gaps = root.find('f-gaps')
        if gaps is not None:
            for gap in gaps:
                if gap.text:
                    framework_data['gaps'].append(gap.text.strip())
        
        # 解析研究方向
        directions = root.find('f-directions')
        if directions is not None:
            for direction in directions.findall('f-direction'):
                scope = direction.find('f-scope')
                limitations = direction.find('f-inherent-limitations')
                framework_data['directions'].append({
                    'scope': scope.text.strip() if scope is not None and scope.text else '',
                    'limitations': limitations.text.strip() if limitations is not None and limitations.text else ''
                })
        
        return framework_data
    
    def search_literature(self, query: str, context: str = "") -> str:
        """使用Kimi API进行文献检索"""
        messages = [
            {
                "role": "system",
                "content": f"""
你是一个专业的文献检索助手。请根据用户提供的查询内容，搜索相关的学术文献和研究资料。

请按照以下要求进行检索和整理：
1. 搜索与查询内容相关的最新学术文献
2. 重点关注权威期刊、会议论文和专业报告
3. 提供文献的核心观点和主要发现
4. 包含作者信息、发表年份、期刊/会议名称等基本信息
5. 用中文总结文献内容

上下文信息：{context}
"""
            },
            {
                "role": "user",
                "content": f"请搜索关于以下内容的相关文献：{query}"
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
        
        try:
            # 第一次调用：触发联网搜索
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=tools,
                temperature=0.3,
                stream=True
            )
            
            # 处理流式响应
            tool_calls = []
            for chunk in response:
                if chunk.choices[0].delta.tool_calls:
                    tool_calls.extend(chunk.choices[0].delta.tool_calls)
                
                if chunk.choices[0].finish_reason == "tool_calls":
                    break
            
            # 处理工具调用
            if tool_calls:
                tool_call = tool_calls[0]
                messages.append({
                    "role": "assistant",
                    "content": "",
                    "tool_calls": [tool_call]
                })
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(tool_call.function.arguments)
                })
                
                # 第二次调用：获取最终结果
                final_response = client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    temperature=0.3,
                    stream=True
                )
                
                full_content = ""
                for chunk in final_response:
                    if chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        print(content, end="", flush=True)  # 实时输出
                        full_content += content
                
                return full_content
            
        except Exception as e:
            print(f"\n检索出错: {e}")
            return f"检索失败：{query}"
        
        return "未能获取到有效响应"
    
    def extract_references_from_content(self, content: str) -> List[Dict[str, Any]]:
        """从内容中提取参考文献信息"""
        references = []
        
        # 简单的参考文献提取逻辑（可以根据实际需要改进）
        patterns = [
            r'([\u4e00-\u9fa5a-zA-Z\s]+)\s*\(\s*(\d{4})\s*\)\s*[.。]\s*([^.。]+)[.。]\s*([^.。]+)[.。]?',
            r'([\u4e00-\u9fa5a-zA-Z\s,]+)[.。]\s*([^.。]+)[.。]\s*(\d{4})[.。]?',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if len(match) >= 3:
                    ref = {
                        'id': str(self.reference_counter),
                        'type': 'journal',
                        'creators': [match[0].strip()],
                        'title': match[2].strip() if len(match) > 2 else '',
                        'year': match[1].strip() if len(match) > 1 else '',
                        'publication': match[3].strip() if len(match) > 3 else ''
                    }
                    references.append(ref)
                    self.references[str(self.reference_counter)] = ref
                    self.reference_counter += 1
        
        return references
    
    def calculate_total_steps(self, framework_data: Dict[str, Any]) -> int:
        """计算总的检索步骤数"""
        total_steps = 0
        
        # 研究背景：2步（研究现状 + 文献地图）
        total_steps += 2
        
        # 研究空白：每个空白1步
        total_steps += len(framework_data['gaps'])
        
        # 研究方向：每个方向2步（范围 + 局限性）
        total_steps += len(framework_data['directions']) * 2
        
        # 国内外研究：2步（国内 + 国际）
        total_steps += 2
        
        return total_steps
    
    def generate_material_structure(self, framework_data: Dict[str, Any]) -> str:
        """生成material结构的XML"""
        # 计算总步骤数并初始化进度条
        total_steps = self.calculate_total_steps(framework_data)
        progress_bar = ProgressBar(total_steps)
        
        print(f"🚀 开始进行文献检索，共 {total_steps} 个检索任务...\n")
        
        # 检索研究现状
        progress_bar.update("检索研究现状相关文献")
        research_status_content = self.search_literature(
            framework_data['background']['research_status'],
            "研究现状和背景"
        )
        
        # 检索文献地图
        progress_bar.update("检索文献主题关系相关文献")
        literature_map_content = self.search_literature(
            framework_data['background']['literature_map'],
            "文献主题和关系"
        )
        
        # 检索研究空白
        gaps_content = []
        for i, gap in enumerate(framework_data['gaps']):
            progress_bar.update(f"检索研究空白 {i+1}/{len(framework_data['gaps'])}: {gap[:50]}...")
            content = self.search_literature(gap, "研究空白和不足")
            gaps_content.append(content)
        
        # 检索研究方向
        directions_content = []
        for i, direction in enumerate(framework_data['directions']):
            # 检索方向范围
            progress_bar.update(f"检索研究方向 {i+1} 的范围: {direction['scope'][:50]}...")
            scope_content = self.search_literature(direction['scope'], "研究方向和范围")
            
            # 检索方向局限性
            progress_bar.update(f"检索研究方向 {i+1} 的局限性: {direction['limitations'][:50]}...")
            limitations_content = self.search_literature(direction['limitations'], "研究局限性")
            
            directions_content.append({
                'scope': scope_content,
                'limitations': limitations_content
            })
        
        # 检索国内外研究
        progress_bar.update("检索国内研究现状相关文献")
        domestic_content = self.search_literature(
            framework_data['regional_comparison']['domestic'],
            "国内研究现状"
        )
        
        progress_bar.update("检索国际研究现状相关文献")
        international_content = self.search_literature(
            framework_data['regional_comparison']['international'],
            "国际研究现状"
        )
        
        # 完成进度条
        progress_bar.finish()
        
        print("\n📚 开始提取参考文献信息...")
        
        # 提取所有参考文献
        all_content = [research_status_content, literature_map_content] + gaps_content
        for direction in directions_content:
            all_content.extend([direction['scope'], direction['limitations']])
        all_content.extend([domestic_content, international_content])
        
        for content in all_content:
            self.extract_references_from_content(content)
        
        print(f"✅ 已提取 {len(self.references)} 条参考文献")
        print("\n🔧 正在生成XML结构...")
        
        # 生成XML结构
        xml_content = f"""
<material>
  <t-chapters>
    
    <!-- 3. 研究背景 -->
    <t-chapter id="c3">
      <t-heading>研究背景</t-heading>
      
      <!-- 3.1 研究现状 -->
      <t-section id="c3-s1">
        <t-heading>研究现状</t-heading>
        <t-purpose>本节将系统梳理{framework_data['title']}领域的已有研究成果</t-purpose>
        
        <t-point id="c3-s1-p1">
          <t-claim>{research_status_content[:200]}...</t-claim>
          <t-keywords>研究现状, 发展历程, 主要成果</t-keywords>
          <t-gap>需要进一步补充最新研究进展</t-gap>
        </t-point>
        
        <t-point id="c3-s1-p2">
          <t-claim>{literature_map_content[:200]}...</t-claim>
          <t-keywords>文献主题, 研究关系, 知识图谱</t-keywords>
          <t-gap>需要深入分析主题间的内在联系</t-gap>
        </t-point>
        
      </t-section>
    </t-chapter>
    
    <!-- 4. 当前研究中存在的问题和不足 -->
    <t-chapter id="c4">
      <t-heading>当前研究中存在的问题和不足</t-heading>
      
      <t-section id="c4-s1">
        <t-heading>主要研究空白</t-heading>
"""
        
        # 添加研究空白内容
        for i, gap_content in enumerate(gaps_content):
            xml_content += f"""
        <t-point id="c4-s1-p{i+1}">
          <t-claim>{gap_content[:200]}...</t-claim>
          <t-gap>待进一步深入研究</t-gap>
        </t-point>
"""
        
        xml_content += """
      </t-section>
    </t-chapter>
    
    <!-- 5. 当前研究的主要方向及其不足 -->
    <t-chapter id="c5">
      <t-heading>当前研究的主要方向及其不足</t-heading>
"""
        
        # 添加研究方向内容
        for i, direction_content in enumerate(directions_content):
            xml_content += f"""
      <t-section id="c5-s{i+1}">
        <t-heading>方向{i+1}</t-heading>
        <t-point id="c5-s{i+1}-p1">
          <t-claim>{direction_content['scope'][:200]}...</t-claim>
          <t-gap>{direction_content['limitations'][:200]}...</t-gap>
        </t-point>
      </t-section>
"""
        
        xml_content += f"""
    </t-chapter>
    
    <!-- 6. 国内外相关研究比较 -->
    <t-chapter id="c6">
      <t-heading>国内外相关研究比较</t-heading>
      
      <t-section id="c6-s1">
        <t-heading>国内研究</t-heading>
        <t-point id="c6-s1-p1">
          <t-claim>{domestic_content[:200]}...</t-claim>
        </t-point>
      </t-section>
      
      <t-section id="c6-s2">
        <t-heading>国外研究</t-heading>
        <t-point id="c6-s2-p1">
          <t-claim>{international_content[:200]}...</t-claim>
        </t-point>
      </t-section>
      
      <t-section id="c6-s3">
        <t-heading>差异与启示</t-heading>
        <t-point id="c6-s3-p1">
          <t-claim>通过比较分析，可以发现国内外研究的差异和互补性</t-claim>
        </t-point>
      </t-section>
    </t-chapter>
    
  </t-chapters>
  
  <!-- 参考文献容器 -->
  <t-sources>
"""
        
        # 添加参考文献
        for ref_id, ref_data in self.references.items():
            creators_xml = '\n'.join([f'    <t-creator>{creator}</t-creator>' for creator in ref_data['creators']])
            xml_content += f"""
    <t-ref id="{ref_id}" type="{ref_data['type']}">
{creators_xml}
      <t-title>{ref_data['title']}</t-title>
      <t-publication>
        <t-publisher>{ref_data['publication']}</t-publisher>
        <t-year>{ref_data['year']}</t-year>
      </t-publication>
    </t-ref>
"""
        
        xml_content += """
  </t-sources>
</material>
"""
        
        return xml_content
    
    def process_framework(self, framework_path: str, output_path: str = None):
        """处理整个框架，生成material结构"""
        print(f"📖 开始处理框架文件: {framework_path}")
        
        # 解析框架
        framework_data = self.parse_framework(framework_path)
        print(f"✅ 框架解析完成，标题: {framework_data['title']}")
        
        # 生成material结构
        material_xml = self.generate_material_structure(framework_data)
        
        # 保存结果
        if output_path is None:
            output_path = "material.xml"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(material_xml)
        
        print(f"\n🎉 处理完成，结果已保存到: {output_path}")
        return material_xml

# 使用示例
if __name__ == "__main__":
    processor = FrameworkProcessor()
    
    # 处理framework.xml文件
    framework_path = "framework.xml"
    output_path = "material-2.xml"
    
    try:
        result = processor.process_framework(framework_path, output_path)
        print("\n=== 🎊 所有任务完成 ===")
        print(f"📄 生成的material结构已保存到: {output_path}")
        print(f"📚 共提取了 {len(processor.references)} 条参考文献")
    except Exception as e:
        print(f"❌ 处理过程中出现错误: {e}")