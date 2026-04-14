#!/usr/bin/env python3
"""
OpenClaw SEO Landing Page Generator

读取 keywords.json，为每个关键词生成一个独立的 SEO 着陆页 HTML 文件。
当前使用占位内容，后续可接入 AI API 生成真实内容。

用法:
    python generate.py                  # 生成所有页面
    python generate.py --category pricing  # 只生成某个分类
    python generate.py --slug gpt-4o-api-pricing  # 只生成某个页面
    python generate.py --dry-run        # 仅预览，不写文件
"""

import json
import os
import sys
import argparse
from datetime import date
from string import Template
from pathlib import Path

# ---------------------------------------------------------------------------
# 路径配置
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).parent.resolve()
KEYWORDS_FILE = SCRIPT_DIR / "keywords.json"
TEMPLATE_FILE = SCRIPT_DIR / "template.html"
OUTPUT_DIR = SCRIPT_DIR / "output"

# ---------------------------------------------------------------------------
# 分类中文映射
# ---------------------------------------------------------------------------
CATEGORY_NAMES = {
    "comparison": "对比评测",
    "pricing": "价格分析",
    "tutorial": "使用教程",
    "alternative": "替代方案",
    "use-case": "应用场景",
}

CATEGORY_URL_MAP = {
    "comparison": "compare",
    "pricing": "pricing",
    "tutorial": "tutorials",
    "alternative": "alternatives",
    "use-case": "tutorials",
}

# ---------------------------------------------------------------------------
# 内容生成器（占位内容，后续替换为 AI 生成）
# ---------------------------------------------------------------------------

def generate_comparison_content(kw: dict) -> str:
    """生成对比类页面的占位内容"""
    keyword = kw["keyword"]
    return f"""
            <p>{keyword}是很多开发者在选择 AI API 时关注的话题。本文将从定价、性能、功能、易用性等多个维度进行全面对比，帮助你做出最佳选择。</p>

            <h2>快速对比一览</h2>
            <div class="table-wrapper">
                <table>
                    <thead>
                        <tr>
                            <th>对比维度</th>
                            <th>API A</th>
                            <th>API B</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td>输入价格（每百万token）</td><td>$X.XX</td><td>$Y.YY</td></tr>
                        <tr><td>输出价格（每百万token）</td><td>$X.XX</td><td>$Y.YY</td></tr>
                        <tr><td>上下文窗口</td><td>128K tokens</td><td>200K tokens</td></tr>
                        <tr><td>平均响应延迟</td><td>~150ms</td><td>~120ms</td></tr>
                        <tr><td>多模态支持</td><td>支持</td><td>支持</td></tr>
                        <tr><td>函数调用</td><td>支持</td><td>支持</td></tr>
                        <tr><td>流式输出</td><td>支持</td><td>支持</td></tr>
                        <tr><td>免费额度</td><td>有</td><td>有</td></tr>
                    </tbody>
                </table>
            </div>

            <h2>性能基准测试</h2>
            <p>我们在多个标准基准测试上对两个 API 进行了评估，包括 MMLU、HumanEval、GSM8K 等。以下是关键测试结果的对比分析。</p>
            <p>【此处将填充真实基准测试数据】</p>

            <h2>定价详细对比</h2>
            <p>对于大多数开发者来说，API 的定价是最关键的考量因素之一。让我们深入分析两者的价格体系。</p>
            <p>【此处将填充详细的定价分析和成本计算示例】</p>

            <h2>使用场景推荐</h2>
            <ul>
                <li><strong>选择 API A 的场景：</strong>需要更强的代码生成能力、生态工具更丰富、团队已有相关经验</li>
                <li><strong>选择 API B 的场景：</strong>需要更长的上下文窗口、更好的中文支持、更严格的安全需求</li>
                <li><strong>使用 OpenClaw 中转：</strong>如果你的项目需要同时调用多个模型，可以通过 OpenClaw 统一接入</li>
            </ul>

            <h2>代码示例对比</h2>
            <h3>API A 调用示例</h3>
<pre><code>from openai import OpenAI

client = OpenAI(
    api_key="your-api-key",
    base_url="https://api.openclaw.com/v1"  # OpenClaw 中转
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{{"role": "user", "content": "你好"}}]
)
print(response.choices[0].message.content)</code></pre>

            <h3>API B 调用示例</h3>
<pre><code>import anthropic

client = anthropic.Anthropic(
    api_key="your-api-key",
    base_url="https://api.openclaw.com"  # OpenClaw 中转
)

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{{"role": "user", "content": "你好"}}]
)
print(message.content[0].text)</code></pre>

            <h2>总结</h2>
            <p>两个 API 各有优势。具体选择取决于你的使用场景、预算和技术需求。如果你希望灵活切换不同模型，可以考虑通过 OpenClaw 统一接入，一个 API Key 即可访问所有主流模型。</p>
"""


def generate_pricing_content(kw: dict) -> str:
    """生成价格类页面的占位内容"""
    keyword = kw["keyword"]
    return f"""
            <p>{keyword}——这是每个开发者在接入 AI API 前最关心的问题。本文将详细拆解最新的定价体系，帮你精准估算成本。</p>

            <h2>定价概览</h2>
            <div class="table-wrapper">
                <table>
                    <thead>
                        <tr>
                            <th>模型</th>
                            <th>输入价格（/百万token）</th>
                            <th>输出价格（/百万token）</th>
                            <th>上下文长度</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td>旗舰模型</td><td>$X.XX</td><td>$XX.XX</td><td>128K</td></tr>
                        <tr><td>标准模型</td><td>$X.XX</td><td>$X.XX</td><td>128K</td></tr>
                        <tr><td>轻量模型</td><td>$0.XX</td><td>$0.XX</td><td>128K</td></tr>
                    </tbody>
                </table>
            </div>

            <h2>免费额度详情</h2>
            <p>大多数 AI API 提供商都为新用户提供一定的免费额度。以下是当前的免费使用限制。</p>
            <p>【此处将填充真实的免费额度信息】</p>

            <h2>成本计算示例</h2>
            <h3>场景一：个人开发者（每月 10 万 token）</h3>
            <p>每月成本约：$X.XX</p>
            <h3>场景二：初创公司（每月 1000 万 token）</h3>
            <p>每月成本约：$XX.XX</p>
            <h3>场景三：中型企业（每月 1 亿 token）</h3>
            <p>每月成本约：$XXX.XX</p>

            <h2>省钱技巧</h2>
            <ol>
                <li><strong>使用 API 中转服务：</strong>通过 OpenClaw 等中转平台，通常可以节省 20-40% 的费用</li>
                <li><strong>选择合适的模型：</strong>不是所有任务都需要旗舰模型，轻量模型足以应对大部分场景</li>
                <li><strong>实现缓存策略：</strong>对重复查询进行缓存，避免不必要的 API 调用</li>
                <li><strong>优化 prompt：</strong>精简 prompt 可以显著减少 token 消耗</li>
                <li><strong>批量处理：</strong>利用批量 API 通常能获得更优惠的价格</li>
            </ol>

            <h2>与竞品价格对比</h2>
            <p>【此处将填充与其他 API 的价格横向对比表格】</p>
"""


def generate_tutorial_content(kw: dict) -> str:
    """生成教程类页面的占位内容"""
    keyword = kw["keyword"]
    return f"""
            <p>本教程将手把手教你{keyword}。无论你是刚接触 AI API 的新手，还是有经验的开发者，都能从中获得实用的指导。</p>

            <h2>前置要求</h2>
            <ul>
                <li>Python 3.8+ 或 Node.js 18+</li>
                <li>API Key（可通过 OpenClaw 获取统一的 API Key）</li>
                <li>基础的编程知识</li>
            </ul>

            <h2>第一步：获取 API Key</h2>
            <p>你可以直接从官方渠道获取 API Key，也可以通过 OpenClaw 统一管理。使用 OpenClaw 的好处是一个 Key 即可访问所有模型。</p>

            <h2>第二步：安装依赖</h2>
<pre><code># Python
pip install openai anthropic

# Node.js
npm install openai @anthropic-ai/sdk</code></pre>

            <h2>第三步：基础调用</h2>
<pre><code>from openai import OpenAI

# 使用 OpenClaw 中转（可选，国内推荐）
client = OpenAI(
    api_key="your-openclaw-key",
    base_url="https://api.openclaw.com/v1"
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {{"role": "system", "content": "你是一个有帮助的助手。"}},
        {{"role": "user", "content": "请解释什么是 API"}}
    ],
    temperature=0.7,
    max_tokens=1000
)

print(response.choices[0].message.content)</code></pre>

            <h2>第四步：进阶用法</h2>
            <h3>流式输出</h3>
<pre><code>stream = client.chat.completions.create(
    model="gpt-4o",
    messages=[{{"role": "user", "content": "写一首诗"}}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")</code></pre>

            <h3>错误处理</h3>
<pre><code>import openai

try:
    response = client.chat.completions.create(...)
except openai.RateLimitError:
    print("触发速率限制，请稍后重试")
except openai.APIConnectionError:
    print("网络连接失败，请检查网络")
except openai.APIError as e:
    print(f"API 错误: {{e}}")</code></pre>

            <h2>最佳实践</h2>
            <ol>
                <li><strong>设置合理的 timeout：</strong>避免请求长时间挂起</li>
                <li><strong>实现重试机制：</strong>使用指数退避策略处理临时错误</li>
                <li><strong>监控使用量：</strong>定期检查 token 消耗，避免超出预算</li>
                <li><strong>使用环境变量：</strong>不要在代码中硬编码 API Key</li>
            </ol>

            <h2>常见问题排查</h2>
            <div class="table-wrapper">
                <table>
                    <thead>
                        <tr><th>错误</th><th>原因</th><th>解决方案</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>401 Unauthorized</td><td>API Key 无效或过期</td><td>检查 Key 是否正确</td></tr>
                        <tr><td>429 Rate Limit</td><td>请求频率过高</td><td>实现退避重试或升级套餐</td></tr>
                        <tr><td>500 Server Error</td><td>服务端临时故障</td><td>等待后重试</td></tr>
                        <tr><td>网络超时</td><td>网络不通或延迟高</td><td>使用 OpenClaw 中转加速</td></tr>
                    </tbody>
                </table>
            </div>
"""


def generate_alternative_content(kw: dict) -> str:
    """生成替代方案类页面的占位内容"""
    keyword = kw["keyword"]
    return f"""
            <p>正在寻找{keyword}？你来对了。本文为你整理了 2026 年最值得关注的替代选择，涵盖开源方案和商业服务。</p>

            <h2>替代方案总览</h2>
            <div class="table-wrapper">
                <table>
                    <thead>
                        <tr>
                            <th>方案</th>
                            <th>类型</th>
                            <th>价格</th>
                            <th>特点</th>
                            <th>推荐指数</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td>替代方案 A</td><td>商业</td><td>按量计费</td><td>性能强、生态好</td><td>4.8/5</td></tr>
                        <tr><td>替代方案 B</td><td>商业</td><td>按量计费</td><td>性价比高</td><td>4.6/5</td></tr>
                        <tr><td>替代方案 C</td><td>开源</td><td>免费/自部署</td><td>可定制、数据安全</td><td>4.5/5</td></tr>
                        <tr><td>替代方案 D</td><td>国产</td><td>按量计费</td><td>中文优化、无需翻墙</td><td>4.4/5</td></tr>
                        <tr><td>OpenClaw 中转</td><td>聚合</td><td>按量计费</td><td>一键访问所有模型</td><td>4.7/5</td></tr>
                    </tbody>
                </table>
            </div>

            <h2>方案详细分析</h2>
            <h3>替代方案 A</h3>
            <p>【此处将填充详细的方案分析、优缺点、适用场景】</p>

            <h3>替代方案 B</h3>
            <p>【此处将填充详细的方案分析、优缺点、适用场景】</p>

            <h3>替代方案 C（开源方案）</h3>
            <p>【此处将填充开源部署方案、硬件需求、性能对比】</p>

            <h2>选择建议</h2>
            <ul>
                <li><strong>追求性能：</strong>选择方案 A，各项基准测试领先</li>
                <li><strong>追求性价比：</strong>选择方案 B 或通过 OpenClaw 中转</li>
                <li><strong>数据安全优先：</strong>选择开源方案自行部署</li>
                <li><strong>国内访问便捷：</strong>选择国产方案或 OpenClaw 中转服务</li>
            </ul>

            <h2>迁移指南</h2>
            <p>如果你已经在使用某个 API，迁移到替代方案并不复杂。大多数 AI API 都兼容 OpenAI 的接口格式，只需要修改 <code>base_url</code> 和 <code>api_key</code> 即可。</p>
<pre><code># 只需修改两行即可切换 API 提供商
client = OpenAI(
    api_key="your-new-key",
    base_url="https://api.openclaw.com/v1"  # 通过 OpenClaw 统一接入
)</code></pre>
"""


# ---------------------------------------------------------------------------
# 内容生成路由
# ---------------------------------------------------------------------------
CONTENT_GENERATORS = {
    "comparison": generate_comparison_content,
    "pricing": generate_pricing_content,
    "tutorial": generate_tutorial_content,
    "alternative": generate_alternative_content,
    "use-case": generate_tutorial_content,
}


# ---------------------------------------------------------------------------
# FAQ 生成（占位）
# ---------------------------------------------------------------------------
FAQ_TEMPLATES = {
    "comparison": [
        ("两个 API 哪个更便宜？", "定价取决于具体的使用量和模型选择。一般来说，轻量级模型价格更低，但旗舰模型的性能更强。建议根据实际需求做成本测算。通过 OpenClaw 中转通常可以获得更优惠的价格。"),
        ("哪个 API 响应速度更快？", "响应速度受多种因素影响，包括模型大小、prompt 长度、并发量等。我们的测试显示两者在大多数场景下响应时间相差不大，均在可接受范围内。"),
        ("可以同时使用两个 API 吗？", "当然可以。很多企业会根据不同任务选择不同的模型。使用 OpenClaw 中转服务，一个 API Key 即可切换调用不同的模型。"),
        ("哪个 API 的中文支持更好？", "近年来各大模型在中文能力上都有显著提升。具体表现因任务类型而异，建议实际测试对比。"),
        ("切换 API 难吗？", "大多数 AI API 都兼容 OpenAI 的接口格式，迁移成本很低。通常只需修改 base_url 和 model 参数即可。"),
    ],
    "pricing": [
        ("有免费额度吗？", "大多数 AI API 提供商为新用户提供免费额度。具体额度请查看官方最新政策。通过 OpenClaw 注册同样可以获得免费体验额度。"),
        ("超出额度会怎样？", "超出免费额度后会按照标准价格计费。建议设置用量告警，避免意外超支。"),
        ("有年付折扣吗？", "部分提供商支持预付费折扣。通过 OpenClaw 按量计费，无需大额预付。"),
        ("Token 是怎么计算的？", "Token 是语言模型处理文本的基本单位。中文约 1-2 个字符对应一个 token，英文约 4 个字符对应一个 token。"),
        ("如何降低 API 成本？", "可以通过优化 prompt、使用缓存、选择合适模型、使用中转服务等方式降低成本。详见文中省钱技巧部分。"),
    ],
    "tutorial": [
        ("新手需要什么基础？", "基本的 Python 或 JavaScript 编程能力即可。本教程会从安装环境开始手把手教你。"),
        ("API Key 在哪里获取？", "可以从各 API 提供商官网注册获取，也可以通过 OpenClaw 获取统一的 API Key，一个 Key 访问所有模型。"),
        ("国内可以直接调用吗？", "部分海外 API 在国内可能存在网络问题。推荐使用 OpenClaw 中转服务，国内直连、低延迟。"),
        ("调用失败怎么排查？", "常见原因包括：API Key 无效、网络不通、请求格式错误、触发速率限制等。请参考文中的常见问题排查表格。"),
        ("有完整的代码示例吗？", "本教程提供了完整的可运行代码示例，你可以直接复制使用。"),
    ],
    "alternative": [
        ("替代方案的质量如何？", "现在的替代方案在很多任务上已经接近甚至超越了原方案。建议根据你的具体需求进行实际测试对比。"),
        ("迁移到替代方案难吗？", "大多数 AI API 都兼容 OpenAI 格式，迁移通常只需修改 base_url 和 model 参数。"),
        ("有免费的替代方案吗？", "有的。部分开源模型可以免费使用（自部署），商业 API 通常也提供免费额度。"),
        ("国内有好的替代方案吗？", "国产大模型 API 发展迅速，如 DeepSeek、智谱、百川等都提供了高质量的 API 服务，且无需翻墙。"),
        ("OpenClaw 中转是什么？", "OpenClaw 是 AI API 聚合中转服务，一个 API Key 即可访问 GPT-4o、Claude、Gemini 等所有主流模型，国内直连。"),
    ],
}


def generate_faq_html(category: str) -> str:
    """生成 FAQ 区域的 HTML"""
    faqs = FAQ_TEMPLATES.get(category, FAQ_TEMPLATES["tutorial"])
    html_parts = []
    for q, a in faqs:
        html_parts.append(f"""                <div class="faq-item">
                    <div class="faq-question">{q}</div>
                    <div class="faq-answer">{a}</div>
                </div>""")
    return "\n".join(html_parts)


def generate_faq_schema(category: str) -> str:
    """生成 FAQ Schema.org JSON-LD 片段"""
    faqs = FAQ_TEMPLATES.get(category, FAQ_TEMPLATES["tutorial"])
    items = []
    for q, a in faqs:
        items.append(f"""            {{
                "@type": "Question",
                "name": "{q}",
                "acceptedAnswer": {{
                    "@type": "Answer",
                    "text": "{a}"
                }}
            }}""")
    return ",\n".join(items)


# ---------------------------------------------------------------------------
# 相关页面推荐
# ---------------------------------------------------------------------------

def generate_related_pages(current_slug: str, keywords: list, max_count: int = 4) -> str:
    """为当前页面选择相关页面"""
    # 简单策略：同分类的其他页面
    current = None
    for kw in keywords:
        if kw["slug"] == current_slug:
            current = kw
            break

    if not current:
        return ""

    related = [kw for kw in keywords if kw["slug"] != current_slug]
    # 优先同分类，然后其他分类
    same_cat = [kw for kw in related if kw["category"] == current["category"]]
    other_cat = [kw for kw in related if kw["category"] != current["category"]]
    selected = (same_cat[:2] + other_cat[:2])[:max_count]

    html_parts = []
    for kw in selected:
        cat_url = CATEGORY_URL_MAP.get(kw["category"], kw["category"])
        cat_name = CATEGORY_NAMES.get(kw["category"], kw["category"])
        html_parts.append(f"""                    <a class="related-card" href="/{cat_url}/{kw['slug']}.html">
                        <span class="tag">{cat_name}</span>
                        <h4>{kw['keyword']}</h4>
                    </a>""")
    return "\n".join(html_parts)


# ---------------------------------------------------------------------------
# 主生成函数
# ---------------------------------------------------------------------------

def generate_page(kw: dict, template_str: str, all_keywords: list) -> str:
    """为一个关键词生成完整的 HTML 页面"""
    category = kw["category"]
    slug = kw["slug"]
    keyword = kw["keyword"]
    cat_url = CATEGORY_URL_MAP.get(category, category)
    cat_name = CATEGORY_NAMES.get(category, category)
    today = date.today().isoformat()

    # 生成标题（基于分类和关键词）
    title_map = {
        "comparison": f"{keyword} | 2026完整对比指南",
        "pricing": f"{keyword} | 2026最新价格详解",
        "tutorial": f"{keyword} | 完整教程与代码示例",
        "alternative": f"{keyword} | 2026年最佳选择",
        "use-case": f"{keyword} | 实战教程与代码示例",
    }
    title = title_map.get(category, keyword)

    # 生成 meta description
    desc_map = {
        "comparison": f"详细对比{keyword}。包含定价、性能、功能全方位评测，帮助你选择最适合的AI API。",
        "pricing": f"{keyword}详解。包含各套餐对比、隐藏费用分析和省钱技巧。",
        "tutorial": f"{keyword}完整指南。包含代码示例、最佳实践和常见问题排查，新手友好。",
        "alternative": f"{keyword}完整盘点。对比各方案优缺点，帮你找到最佳替代选择。",
        "use-case": f"{keyword}实战教程。从入门到进阶，附完整代码示例。",
    }
    description = desc_map.get(category, f"{keyword}详细指南与分析。")

    # 生成内容
    generator = CONTENT_GENERATORS.get(category, generate_tutorial_content)
    content = generator(kw)

    # 生成 FAQ
    faq_html = generate_faq_html(category)
    faq_schema = generate_faq_schema(category)

    # 生成相关页面
    related_html = generate_related_pages(slug, all_keywords)

    # 估算阅读时间
    read_time = max(3, len(content) // 500)

    # 填充模板
    canonical_url = f"https://openclaw.com/{cat_url}/{slug}"

    # 使用简单的字符串替换（兼容性好，不需要额外依赖）
    html = template_str
    replacements = {
        "{{title}}": title,
        "{{description}}": description,
        "{{keyword}}": keyword,
        "{{canonical_url}}": canonical_url,
        "{{date_published}}": today,
        "{{date_modified}}": today,
        "{{category}}": cat_url,
        "{{category_name}}": cat_name,
        "{{breadcrumb_current}}": keyword,
        "{{read_time}}": str(read_time),
        "{{content}}": content,
        "{{faqs}}": faq_html,
        "{{faq_schema}}": faq_schema,
        "{{related_pages}}": related_html,
    }
    for placeholder, value in replacements.items():
        html = html.replace(placeholder, value)

    return html


def main():
    parser = argparse.ArgumentParser(description="OpenClaw SEO 着陆页生成器")
    parser.add_argument("--category", help="只生成指定分类的页面")
    parser.add_argument("--slug", help="只生成指定 slug 的页面")
    parser.add_argument("--dry-run", action="store_true", help="仅打印文件列表，不写入文件")
    parser.add_argument("--output", default=str(OUTPUT_DIR), help="输出目录")
    args = parser.parse_args()

    output_dir = Path(args.output)

    # 读取关键词
    with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    keywords = data["keywords"]

    # 读取模板
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        template_str = f.read()

    # 过滤关键词
    if args.slug:
        keywords_to_gen = [kw for kw in keywords if kw["slug"] == args.slug]
        if not keywords_to_gen:
            print(f"错误：找不到 slug '{args.slug}'")
            sys.exit(1)
    elif args.category:
        keywords_to_gen = [kw for kw in keywords if kw["category"] == args.category]
        if not keywords_to_gen:
            print(f"错误：找不到分类 '{args.category}'")
            sys.exit(1)
    else:
        keywords_to_gen = keywords

    print(f"准备生成 {len(keywords_to_gen)} 个着陆页...")
    print(f"输出目录: {output_dir}")
    print()

    # 按分类创建子目录并生成页面
    generated = 0
    for kw in keywords_to_gen:
        cat_url = CATEGORY_URL_MAP.get(kw["category"], kw["category"])
        page_dir = output_dir / cat_url
        file_path = page_dir / f"{kw['slug']}.html"

        if args.dry_run:
            print(f"  [预览] {file_path}")
            generated += 1
            continue

        page_dir.mkdir(parents=True, exist_ok=True)
        html = generate_page(kw, template_str, keywords)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"  [生成] {file_path}")
        generated += 1

    print()
    print(f"完成！共生成 {generated} 个页面。")

    if not args.dry_run:
        # 生成索引页
        generate_index(output_dir, keywords)
        # 生成 sitemap
        generate_sitemap(output_dir, keywords)
        print("已生成 index.html 和 sitemap.xml")


def generate_index(output_dir: Path, keywords: list):
    """生成一个简单的索引页"""
    categories = {}
    for kw in keywords:
        cat = kw["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(kw)

    links_html = ""
    for cat, kws in categories.items():
        cat_name = CATEGORY_NAMES.get(cat, cat)
        cat_url = CATEGORY_URL_MAP.get(cat, cat)
        links_html += f"<h2>{cat_name}</h2>\n<ul>\n"
        for kw in kws:
            links_html += f'  <li><a href="/{cat_url}/{kw["slug"]}.html">{kw["keyword"]}</a></li>\n'
        links_html += "</ul>\n"

    index_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenClaw - AI API 技术指南</title>
    <meta name="description" content="AI API 对比、价格、教程和替代方案完整指南。帮助开发者选择最适合的 AI API 服务。">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans SC", sans-serif; max-width: 780px; margin: 0 auto; padding: 40px 20px; color: #1a1a2e; line-height: 1.8; }}
        h1 {{ font-size: 28px; margin-bottom: 8px; }}
        h2 {{ font-size: 20px; margin: 32px 0 12px; color: #2563eb; }}
        .subtitle {{ color: #4a4a6a; margin-bottom: 32px; }}
        ul {{ padding-left: 20px; }}
        li {{ margin-bottom: 6px; }}
        a {{ color: #2563eb; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>OpenClaw AI API 技术指南</h1>
    <p class="subtitle">对比、价格、教程和替代方案 — 帮助你选择和使用最适合的 AI API</p>
    {links_html}
</body>
</html>"""

    with open(output_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(index_html)


def generate_sitemap(output_dir: Path, keywords: list):
    """生成 sitemap.xml"""
    today = date.today().isoformat()
    urls = ['  <url>\n    <loc>https://openclaw.com/</loc>\n    <lastmod>{}</lastmod>\n    <priority>1.0</priority>\n  </url>'.format(today)]

    for kw in keywords:
        cat_url = CATEGORY_URL_MAP.get(kw["category"], kw["category"])
        priority = "0.8" if kw.get("estimated_difficulty") == "high" else "0.7"
        urls.append(f"""  <url>
    <loc>https://openclaw.com/{cat_url}/{kw['slug']}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{priority}</priority>
  </url>""")

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>"""

    with open(output_dir / "sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap)


if __name__ == "__main__":
    main()
