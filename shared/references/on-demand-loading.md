# 按需加载机制技术方案

**版本**: v1.0
**创建日期**: 2026-03-18
**关联任务**: Phase 2.5 - 上下文优化

---

## 1. 概述

### 1.1 问题定义

当前系统读取章节内容时，无论是否需要，都加载完整章节文件（4000字），导致上下文膨胀。

```
传统方式:
Agent: "我需要查看第3章的伏笔"
→ 读取 chapter-003.md (4000字)
→ 实际使用: 只有2段相关内容 (200字)
→ 浪费: 3800字 (95%)
```

### 1.2 解决方案

**按需加载**: 只加载引用指定的内容片段，而非完整文件。

```
按需加载:
Agent: "我需要查看第3章的伏笔"
→ 解析引用: "chapter-003#foreshadowing"
→ 加载: 段落15-20 (200字)
→ 无浪费
```

### 1.3 核心组件

```yaml
按需加载系统:
  ├─ 引用解析器 (Reference Parser)
  │   └─ 将文本引用转换为结构化路径
  ├─ 内容加载器 (Content Loader)
  │   └─ 根据路径读取指定内容
  ├─ 缓存管理器 (Cache Manager)
  │   └─ 避免重复加载，LRU淘汰
  └─ 索引服务 (Index Service)
      └─ 基于章节索引定位内容
```

---

## 2. 引用格式规范

### 2.1 基础引用格式

```markdown
## 格式: <文件标识>#<定位符>

chapter-003                    # 完整章节（不推荐）
chapter-003#paragraph-15       # 第15段
chapter-003#paragraph-15-20    # 第15-20段
chapter-003#section-2          # 第2节
chapter-003#foreshadowing      # 伏笔段落（语义标签）
chapter-003#dialogue-3         # 第3段对话
```

### 2.2 语义引用格式

```markdown
## 基于章节索引的语义引用

{{chapter-003.keyEvents[0]}}           # 第3章第1个关键事件
{{chapter-003.characters}}              # 第3章出场角色列表
{{chapter-003.foreshadowing}}           # 第3章伏笔列表
{{chapter-003.cliffhanger}}             # 第3章结尾钩子

## 跨章节引用

{{prev-chapter.cliffhanger}}            # 前一章的结尾钩子
{{chapter-001.foreshadowing.resolved}}  # 第1章已回收伏笔
```

### 2.3 范围引用格式

```markdown
## 段落范围
chapter-003#paragraph-10-15

## 章节范围（用于连贯性检查）
chapter-001..chapter-003              # 第1-3章
chapter-003[-2:]                      # 第3章最后2段
chapter-003[:5]                       # 第3章前5段
```

---

## 3. 引用解析器

### 3.1 解析流程

```typescript
// reference-parser.ts

interface ParsedReference {
  chapterId: string;        // "chapter-003"
  chapterNumber: number;    // 3
  path: string;             // 实际文件路径
  selector?: string;        // "paragraph-15-20" | "foreshadowing"
  selectorType: 'paragraph' | 'section' | 'semantic' | 'full';
  range?: { start: number; end: number };
}

function parseReference(ref: string): ParsedReference {
  // 1. 解析基础格式
  const match = ref.match(/^(chapter-(\d+))(?:#(.+))?$/);
  if (!match) throw new InvalidReferenceError(ref);

  const [, chapterId, chapterNum, selector] = match;

  // 2. 解析选择器
  const parsed = {
    chapterId,
    chapterNumber: parseInt(chapterNum),
    path: resolveChapterPath(chapterId),
    selector,
    selectorType: 'full' as const
  };

  if (!selector) return parsed;

  // 3. 解析选择器类型
  if (selector.startsWith('paragraph-')) {
    return parseParagraphSelector(parsed, selector);
  } else if (selector.startsWith('section-')) {
    return parseSectionSelector(parsed, selector);
  } else {
    return parseSemanticSelector(parsed, selector);
  }
}

function parseParagraphSelector(
  base: ParsedReference,
  selector: string
): ParsedReference {
  const rangeMatch = selector.match(/paragraph-(\d+)(?:-(\d+))?/);
  if (!rangeMatch) throw new InvalidSelectorError(selector);

  const start = parseInt(rangeMatch[1]);
  const end = rangeMatch[2] ? parseInt(rangeMatch[2]) : start;

  return {
    ...base,
    selectorType: 'paragraph',
    range: { start, end }
  };
}

function parseSemanticSelector(
  base: ParsedReference,
  selector: string
): ParsedReference {
  // 从章节索引获取语义段落位置
  const index = loadChapterIndex(base.chapterId);
  const positions = index.semanticMap[selector];

  if (!positions) {
    throw new SemanticNotFoundError(selector, base.chapterId);
  }

  return {
    ...base,
    selectorType: 'semantic',
    range: positions
  };
}
```

### 3.2 错误处理

```typescript
class ReferenceParseError extends Error {
  constructor(
    message: string,
    public ref: string,
    public code: string
  ) {
    super(message);
    this.name = 'ReferenceParseError';
  }
}

// 错误码定义
const ERROR_CODES = {
  INVALID_FORMAT: 'REF001',      // 格式错误
  CHAPTER_NOT_FOUND: 'REF002',   // 章节不存在
  PARAGRAPH_OUT_OF_RANGE: 'REF003',  // 段落越界
  SEMANTIC_NOT_FOUND: 'REF004',  // 语义标签不存在
  INVALID_RANGE: 'REF005'        // 范围格式错误
};
```

---

## 4. 内容加载器

### 4.1 加载策略

```typescript
// content-loader.ts

interface LoadOptions {
  useCache?: boolean;       // 是否使用缓存（默认true）
  maxLength?: number;       // 最大加载长度限制
  includeContext?: number;  // 包含前后上下文段落数
}

interface ContentSegment {
  reference: ParsedReference;
  content: string;
  paragraphs: Paragraph[];
  metadata: {
    wordCount: number;
    paragraphCount: number;
    loadTime: number;
    fromCache: boolean;
  };
}

async function loadContent(
  ref: string,
  options: LoadOptions = {}
): Promise<ContentSegment> {
  const { useCache = true, maxLength = 5000, includeContext = 0 } = options;

  // 1. 解析引用
  const parsed = parseReference(ref);

  // 2. 检查缓存
  if (useCache) {
    const cached = cacheManager.get(parsed);
    if (cached) {
      return addContextIfNeeded(cached, includeContext);
    }
  }

  // 3. 加载内容
  const segment = await loadFromFile(parsed);

  // 4. 长度检查
  if (segment.metadata.wordCount > maxLength) {
    throw new ContentTooLongError(ref, segment.metadata.wordCount, maxLength);
  }

  // 5. 加入缓存
  if (useCache) {
    cacheManager.set(parsed, segment);
  }

  // 6. 添加上下文
  return addContextIfNeeded(segment, includeContext);
}
```

### 4.2 分段加载实现

```typescript
async function loadFromFile(
  parsed: ParsedReference
): Promise<ContentSegment> {
  const fullContent = await fs.readFile(parsed.path, 'utf-8');
  const paragraphs = splitIntoParagraphs(fullContent);

  let selectedContent: string;
  let selectedParagraphs: Paragraph[];

  switch (parsed.selectorType) {
    case 'full':
      selectedContent = fullContent;
      selectedParagraphs = paragraphs;
      break;

    case 'paragraph':
      selectedParagraphs = paragraphs.slice(
        parsed.range!.start - 1,
        parsed.range!.end
      );
      selectedContent = selectedParagraphs.map(p => p.text).join('\n\n');
      break;

    case 'semantic':
      // 从索引获取语义段落位置
      const indices = await resolveSemanticIndices(parsed);
      selectedParagraphs = indices.map(i => paragraphs[i]);
      selectedContent = selectedParagraphs.map(p => p.text).join('\n\n');
      break;

    default:
      throw new Error(`Unknown selector type: ${parsed.selectorType}`);
  }

  return {
    reference: parsed,
    content: selectedContent,
    paragraphs: selectedParagraphs,
    metadata: {
      wordCount: countWords(selectedContent),
      paragraphCount: selectedParagraphs.length,
      loadTime: Date.now(),
      fromCache: false
    }
  };
}
```

### 4.3 批量加载优化

```typescript
async function loadBatch(
  refs: string[],
  options: LoadOptions = {}
): Promise<ContentSegment[]> {
  // 1. 解析所有引用
  const parsed = refs.map(parseReference);

  // 2. 按章节分组
  const grouped = groupBy(parsed, 'chapterId');

  // 3. 并行加载各章节
  const results = await Promise.all(
    Object.entries(grouped).map(async ([chapterId, refs]) => {
      // 对于同一章节，合并范围后一次性读取
      const mergedRange = mergeRanges(refs);
      return await loadContentWithMergedRange(chapterId, mergedRange);
    })
  );

  // 4. 按原始引用拆分结果
  return refs.map((ref, i) => extractSegment(results[i], parsed[i]));
}
```

---

## 5. 缓存管理器

### 5.1 缓存策略

```typescript
// cache-manager.ts

interface CacheEntry {
  segment: ContentSegment;
  lastAccessed: number;
  accessCount: number;
}

class ContentCacheManager {
  private cache = new Map<string, CacheEntry>();
  private maxSize = 100;  // 最大缓存条目数
  private maxAge = 5 * 60 * 1000;  // 5分钟过期

  private generateKey(parsed: ParsedReference): string {
    return `${parsed.chapterId}#${parsed.selector || 'full'}`;
  }

  get(parsed: ParsedReference): ContentSegment | null {
    const key = this.generateKey(parsed);
    const entry = this.cache.get(key);

    if (!entry) return null;

    // 检查过期
    if (Date.now() - entry.lastAccessed > this.maxAge) {
      this.cache.delete(key);
      return null;
    }

    // 更新访问信息
    entry.lastAccessed = Date.now();
    entry.accessCount++;

    return entry.segment;
  }

  set(parsed: ParsedReference, segment: ContentSegment): void {
    const key = this.generateKey(parsed);

    // 检查容量
    if (this.cache.size >= this.maxSize) {
      this.evictLRU();
    }

    this.cache.set(key, {
      segment,
      lastAccessed: Date.now(),
      accessCount: 1
    });
  }

  private evictLRU(): void {
    // 找到最久未访问的条目
    let oldest: [string, CacheEntry] | null = null;

    for (const entry of this.cache.entries()) {
      if (!oldest || entry[1].lastAccessed < oldest[1].lastAccessed) {
        oldest = entry;
      }
    }

    if (oldest) {
      this.cache.delete(oldest[0]);
    }
  }

  // 按章节清除缓存
  invalidateChapter(chapterId: string): void {
    for (const key of this.cache.keys()) {
      if (key.startsWith(chapterId)) {
        this.cache.delete(key);
      }
    }
  }

  // 获取缓存统计
  getStats(): { size: number; hitRate: number } {
    // ... 实现统计逻辑
  }
}

export const cacheManager = new ContentCacheManager();
```

### 5.2 缓存预热

```typescript
// 在章节生成完成后预热缓存
async function warmupCache(chapterId: string): Promise<void> {
  const index = loadChapterIndex(chapterId);

  // 预加载常用语义段落
  const commonSemantics = ['keyEvents', 'foreshadowing', 'cliffhanger'];

  for (const semantic of commonSemantics) {
    if (index.semanticMap[semantic]) {
      const ref = `${chapterId}#${semantic}`;
      await loadContent(ref, { useCache: true });
    }
  }
}
```

---

## 6. 索引服务集成

### 6.1 索引数据结构

```json
{
  "chapterId": "chapter-003",
  "paragraphCount": 45,
  "semanticMap": {
    "keyEvents": { "start": 15, "end": 18 },
    "foreshadowing": { "start": 20, "end": 22 },
    "cliffhanger": { "start": 44, "end": 45 },
    "dialogue-1": { "start": 5, "end": 8 },
    "dialogue-2": { "start": 25, "end": 28 }
  },
  "sectionMap": {
    "section-1": { "start": 1, "end": 15 },
    "section-2": { "start": 16, "end": 30 },
    "section-3": { "start": 31, "end": 45 }
  }
}
```

### 6.2 语义映射生成

```typescript
// 在 post-write-extraction hook 中生成
async function generateSemanticMap(
  chapterId: string,
  content: string
): Promise<SemanticMap> {
  const paragraphs = splitIntoParagraphs(content);
  const map: SemanticMap = {};

  // 使用LLM识别语义段落
  const prompt = `
分析以下章节内容，识别关键语义段落的位置：
- keyEvents: 关键事件段落
- foreshadowing: 伏笔段落
- cliffhanger: 结尾钩子
- dialogue-N: 第N段重要对话

章节内容（已分段）：
${paragraphs.map((p, i) => `[${i+1}] ${p.text.substring(0, 100)}...`).join('\n')}

返回JSON格式：
{
  "keyEvents": {"start": 段落号, "end": 段落号},
  "foreshadowing": {"start": 段落号, "end": 段落号},
  ...
}
`;

  const result = await llm.call(prompt);
  return JSON.parse(result);
}
```

---

## 7. 与 Queen Bee 集成

### 7.1 Queen Bee 使用规范

```markdown
## Queen Bee 按需加载使用规范

### 禁止行为
❌ 直接读取完整章节文件
❌ 一次性加载多个完整章节
❌ 重复读取相同内容

### 推荐做法
✅ 优先使用章节索引获取元数据
✅ 使用语义引用加载特定段落
✅ 利用缓存避免重复加载

### 使用示例

```yaml
# 生成前章回顾
default: |
  上一章回顾：{{prev-chapter.keyEvents}}

  需要呼应的伏笔：{{chapter-001.foreshadowing}}

# 验证连贯性
check: |
  检查时间线一致性：{{chapter-003[-3:].content}}
  确认角色状态：{{chapter-003.characters}}
```

```

### 7.2 配置选项

```yaml
# .mighty/config/loading.yaml
on_demand_loading:
  enabled: true
  cache:
    max_size: 100
    ttl: 300  # 秒
  limits:
    max_paragraphs_per_load: 10
    max_concurrent_loads: 5
  semantics:
    auto_generate: true
    common_types:
      - keyEvents
      - foreshadowing
      - cliffhanger
      - dialogue
```

---

## 8. 性能指标

### 8.1 预期性能

| 指标 | 传统方式 | 按需加载 | 提升 |
|------|---------|---------|------|
| 单次引用上下文 | ~4000字 | ~200字 | **95%** |
| 10章连贯性检查 | ~40000字 | ~2000字 | **95%** |
| 加载时间 | 500ms | 50ms | **90%** |
| 缓存命中率 | 0% | 70%+ | - |

### 8.2 监控指标

```typescript
interface LoadingMetrics {
  totalLoads: number;
  cacheHits: number;
  cacheMisses: number;
  averageLoadTime: number;
  bytesSaved: number;
  semanticCoverage: number;  // 语义标签覆盖率
}
```

---

## 9. 使用示例

### 9.1 在 Command 中使用

```markdown
# novel-write.md

## 前文引用

### 传统方式（不推荐）
```

读取: chapters/chapter-003.md  # 4000字

```

### 按需加载（推荐）
```

引用: chapter-003#keyEvents     # ~300字
引用: chapter-002#cliffhanger   # ~100字
总计: ~400字 (节省 90%)

```
```

### 9.2 在 Skill 中使用

```typescript
// webnovel-writing/Skill.ts

async function generateChapter(context: Context) {
  // 加载前章关键信息（按需）
  const prevChapter = await loadContent(
    `chapter-${context.chapterNum - 1}#cliffhanger`,
    { includeContext: 2 }  // 包含前后2段上下文
  );

  // 加载伏笔段落
  const foreshadowing = await loadBatch([
    'chapter-001#foreshadowing',
    'chapter-003#foreshadowing'
  ]);

  // 生成...
}
```

### 9.3 在 Bee 中使用

```markdown
# consistency-bee.md

## 连贯性检查

### 步骤1: 按需加载对比内容

```yaml
load:
  current_cliffhanger: "{{chapter-N-1}}#cliffhanger[-1]"
  next_opening: "{{chapter-N}}#paragraph-1-3"

compare:
  - 结尾钩子与开篇呼应
  - 角色状态连续性
  - 时间线一致性
```

```

---

## 10. 实施计划

### Phase A: 核心实现

- [ ] 实现引用解析器
- [ ] 实现内容加载器
- [ ] 实现缓存管理器
- [ ] 单元测试覆盖

### Phase B: 索引集成

- [ ] 扩展章节索引 Schema（添加 semanticMap）
- [ ] 更新 post-write-extraction hook
- [ ] 索引生成自动化

### Phase C: 系统集成

- [ ] Queen Bee 集成
- [ ] Commands 更新
- [ ] Skills 适配

### Phase D: 优化验证

- [ ] 性能基准测试
- [ ] 缓存命中率优化
- [ ] 错误处理完善

---

## 附录

### A. 相关文档

- [章节索引系统](./chapter-index-schema.md)
- [增量更新协议](./incremental-update-protocol.md)
- [串行生成模式](./serial-generation-mode.md)

### B. 术语表

| 术语 | 定义 |
|------|------|
| 按需加载 | 只加载引用指定的内容片段 |
| 语义引用 | 基于内容语义的引用方式（如 #foreshadowing） |
| LRU | 最近最少使用缓存淘汰策略 |
| 语义映射 | 语义标签到段落位置的映射表 |

### C. 故障排查

**Q: 语义引用返回空内容**
A: 检查章节索引中的 semanticMap 是否已生成

**Q: 缓存命中率低**
A: 调整缓存大小和TTL，或检查引用模式是否分散

**Q: 段落范围越界**
A: 检查章节索引的 paragraphCount 是否与实际文件一致
