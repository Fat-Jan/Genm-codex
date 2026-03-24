# 章节索引系统技术方案

**文档版本**: v1.0
**创建日期**: 2026-03-18
**关联任务**: Phase 2.5 - 上下文膨胀解决

---

## 一、元数据分离原理

### 1.1 问题定义

**当前痛点**:

| 问题 | 表现 | 影响 |
|------|------|------|
| 上下文爆炸 | 每章4000字 × 10章 = 40,000字 | Token 消耗过大 |
| 验证效率低 | Queen Bee 读取全部章节验证连贯性 | 验证时间指数增长 |
| 真相文件未读取 | Agent 依赖描述而非真实文件 | 生成内容不一致 |

**根本原因**:

```
错误模式: Agent 读取完整章节内容 → 占用上下文 → Token 爆炸
正确模式: Agent 读取元数据索引 → 按需引用 → Token 优化
```

### 1.2 解决方案

**核心原则**: 文件系统作为唯一事实源，上下文只存当前任务。

```
┌─────────────────────────────────────────────────────────┐
│                    Context Window                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│  │ Chapter-011 │  │   Index     │  │  Truth Files    │  │
│  │  (current)  │  │  (metadata) │  │   (current)     │  │
│  │   ~4000字   │  │   ~500字    │  │    ~2000字      │  │
│  └─────────────┘  └─────────────┘  └─────────────────┘  │
│                                                          │
│  总上下文: ~6,500 字 (vs 40,000 字，节省 83%)           │
└─────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────┐
│                   Filesystem (Disk)                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐  │
│  │Chapter001│ │Chapter002│ │   ...    │ │ Chapter100 │  │
│  │Chapter101│ │Chapter102│ │   ...    │ │ Chapter200 │  │
│  └──────────┘ └──────────┘ └──────────┘ └────────────┘  │
│  (完整内容存储在磁盘，按需通过路径引用)                    │
└─────────────────────────────────────────────────────────┘
```

### 1.3 收益分析

| 指标 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| 章节验证 Token | 40,000 | 6,500 | -83% |
| 连贯性检查时间 | 12s | 3s | -75% |
| 上下文可用空间 | 60% | 92% | +53% |
| 支持并行章节数 | 3章 | 10章 | +233% |

---

## 二、章节索引 JSON Schema

### 2.1 主索引文件

**文件位置**: `.mighty/books/{book-id}/chapter-index.json`

**Schema 定义**:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "title": "Chapter Index",
  "description": "网文章节元数据索引，用于快速检索和连贯性验证",
  "properties": {
    "bookId": {
      "type": "string",
      "description": "书籍唯一标识"
    },
    "bookTitle": {
      "type": "string",
      "description": "书籍标题"
    },
    "totalChapters": {
      "type": "integer",
      "description": "总章节数"
    },
    "totalWordCount": {
      "type": "integer",
      "description": "总字数"
    },
    "lastUpdated": {
      "type": "string",
      "format": "date-time",
      "description": "最后更新时间"
    },
    "chapters": {
      "type": "object",
      "patternProperties": {
        "^chapter-[0-9]{3}$": {
          "$ref": "#/definitions/chapterMeta"
        }
      },
      "additionalProperties": false
    }
  },
  "required": ["bookId", "totalChapters", "chapters"],
  "definitions": {
    "chapterMeta": {
      "type": "object",
      "properties": {
        "chapterNumber": {
          "type": "integer",
          "minimum": 1,
          "description": "章节序号"
        },
        "title": {
          "type": "string",
          "description": "章节标题"
        },
        "wordCount": {
          "type": "integer",
          "minimum": 0,
          "description": "章节字数"
        },
        "summary": {
          "type": "string",
          "maxLength": 200,
          "description": "章节内容摘要（200字以内）"
        },
        "keyEvents": {
          "type": "array",
          "items": { "type": "string" },
          "description": "关键事件列表"
        },
        "characters": {
          "type": "array",
          "items": { "type": "string" },
          "description": "出场角色列表"
        },
        "locations": {
          "type": "array",
          "items": { "type": "string" },
          "description": "场景地点列表"
        },
        "foreshadowing": {
          "type": "array",
          "items": { "type": "string" },
          "description": "埋设伏笔列表"
        },
        "foreshadowingResolved": {
          "type": "array",
          "items": { "type": "string" },
          "description": "已回收伏笔列表"
        },
        "cliffhanger": {
          "type": "string",
          "description": "本章悬念/钩子"
        },
        "emotionalTone": {
          "type": "string",
          "enum": ["紧张", "舒缓", "悲伤", "喜悦", "愤怒", "悬疑", "温情", "热血", "搞笑", "恐怖"],
          "description": "本章情感基调"
        },
        "progression": {
          "type": "object",
          "properties": {
            "mainPlot": { "type": "number", "minimum": 0, "maximum": 100 },
            "characterArc": { "type": "number", "minimum": 0, "maximum": 100 },
            "worldBuilding": { "type": "number", "minimum": 0, "maximum": 100 }
          },
          "description": "进度推进指标（百分比）"
        },
        "path": {
          "type": "string",
          "description": "章节文件相对路径"
        },
        "status": {
          "type": "string",
          "enum": ["draft", "reviewing", "approved", "locked"],
          "description": "章节状态"
        },
        "version": {
          "type": "integer",
          "minimum": 1,
          "description": "版本号"
        },
        "createdAt": {
          "type": "string",
          "format": "date-time",
          "description": "创建时间"
        },
        "updatedAt": {
          "type": "string",
          "format": "date-time",
          "description": "最后更新时间"
        },
        "auditScore": {
          "type": "number",
          "minimum": 0,
          "maximum": 100,
          "description": "质量审核得分"
        },
        "tags": {
          "type": "array",
          "items": { "type": "string" },
          "description": "自定义标签"
        },
        "paragraphCount": {
          "type": "integer",
          "minimum": 1,
          "description": "章节段落总数"
        },
        "semanticMap": {
          "type": "object",
          "description": "语义映射表，记录关键内容段落的段落位置",
          "patternProperties": {
            "^[a-zA-Z_][a-zA-Z0-9_-]*$": {
              "type": "object",
              "properties": {
                "start": {
                  "type": "integer",
                  "minimum": 1,
                  "description": "起始段落编号"
                },
                "end": {
                  "type": "integer",
                  "minimum": 1,
                  "description": "结束段落编号"
                },
                "paragraphs": {
                  "type": "array",
                  "items": { "type": "integer", "minimum": 1 },
                  "description": "包含的所有段落编号列表"
                }
              },
              "required": ["start", "end", "paragraphs"]
            }
          },
          "additionalProperties": true
        },
        "sectionMap": {
          "type": "object",
          "description": "章节结构映射，记录各小节位置",
          "patternProperties": {
            "^section-[0-9]+$": {
              "type": "object",
              "properties": {
                "start": { "type": "integer", "minimum": 1 },
                "end": { "type": "integer", "minimum": 1 }
              },
              "required": ["start", "end"]
            }
          }
        },
        "paragraphTypes": {
          "type": "array",
          "description": "段落类型标记列表",
          "items": {
            "type": "object",
            "properties": {
              "index": {
                "type": "integer",
                "minimum": 1,
                "description": "段落编号"
              },
              "type": {
                "type": "string",
                "enum": ["narrative", "dialogue", "action", "description", "monologue", "exposition"],
                "description": "段落类型"
              }
            },
            "required": ["index", "type"]
          }
        }
      },
      "required": ["chapterNumber", "title", "wordCount", "summary", "path", "status", "createdAt", "updatedAt"]
    }
  }
}
```

### 2.2 示例数据

```json
{
  "bookId": "test-novel",
  "bookTitle": "测试小说",
  "totalChapters": 10,
  "totalWordCount": 40000,
  "lastUpdated": "2026-03-18T10:00:00Z",
  "chapters": {
    "chapter-001": {
      "chapterNumber": 1,
      "title": "天才陨落",
      "wordCount": 3985,
      "summary": "主角林凡曾是绝世天才，却因神秘原因修为尽失，沦为宗门笑柄。在遭受欺凌后，意外觉醒神秘系统。",
      "keyEvents": ["修为尽失", "遭受欺凌", "系统觉醒"],
      "characters": ["林凡", "周通", "苏婉儿"],
      "locations": ["青云宗", "外门广场"],
      "foreshadowing": ["神秘系统来源", "上界秘密"],
      "foreshadowingResolved": [],
      "cliffhanger": "系统提示音响起：'检测到宿主，是否绑定？'",
      "emotionalTone": "压抑",
      "progression": {
        "mainPlot": 5,
        "characterArc": 10,
        "worldBuilding": 15
      },
      "path": "chapters/chapter-001.md",
      "status": "locked",
      "version": 3,
      "createdAt": "2026-03-15T08:00:00Z",
      "updatedAt": "2026-03-15T18:30:00Z",
      "auditScore": 87,
      "tags": ["开篇", "系统觉醒"]
    },
    "chapter-002": {
      "chapterNumber": 2,
      "title": "系统绑定",
      "wordCount": 4021,
      "summary": "林凡绑定'万界修炼系统'，获得新手大礼包。通过系统任务快速提升修为，准备参加外门大比。",
      "keyEvents": ["系统绑定", "获得新手礼包", "接取第一个任务"],
      "characters": ["林凡", "系统", "周通"],
      "locations": ["青云宗", "修炼室"],
      "foreshadowing": ["外门大比奖励", "神秘老者身份"],
      "foreshadowingResolved": ["系统功能说明"],
      "cliffhanger": "周通带着人找上门来...",
      "emotionalTone": "热血",
      "progression": {
        "mainPlot": 15,
        "characterArc": 25,
        "worldBuilding": 20
      },
      "path": "chapters/chapter-002.md",
      "status": "locked",
      "version": 2,
      "createdAt": "2026-03-15T10:00:00Z",
      "updatedAt": "2026-03-15T20:00:00Z",
      "auditScore": 85,
      "tags": ["系统", "修炼"]
    },
    "chapter-003": {
      "chapterNumber": 3,
      "title": "一夜突破",
      "wordCount": 4156,
      "summary": "林凡利用系统奖励的丹药一夜突破到炼气五层，在冲突中击败周通，震惊外门。",
      "keyEvents": ["突破到炼气五层", "击败周通", "引起长老关注"],
      "characters": ["林凡", "周通", "苏婉儿", "李长老"],
      "locations": ["青云宗", "外门演武场"],
      "foreshadowing": ["上界秘密线索", "李长老身份"],
      "foreshadowingResolved": [],
      "cliffhanger": "李长老意味深长地说：'小子，你可知道这意味着什么？'",
      "emotionalTone": "热血",
      "progression": {
        "mainPlot": 25,
        "characterArc": 35,
        "worldBuilding": 25
      },
      "path": "chapters/chapter-003.md",
      "status": "approved",
      "version": 2,
      "createdAt": "2026-03-16T09:00:00Z",
      "updatedAt": "2026-03-18T10:00:00Z",
      "auditScore": 88,
      "tags": ["突破", "战斗"],
      "paragraphCount": 45,
      "semanticMap": {
        "keyEvents": { "start": 15, "end": 18, "paragraphs": [15, 16, 17, 18] },
        "foreshadowing": { "start": 20, "end": 22, "paragraphs": [20, 21, 22] },
        "cliffhanger": { "start": 44, "end": 45, "paragraphs": [44, 45] },
        "dialogue-1": { "start": 5, "end": 8, "paragraphs": [5, 6, 7, 8] },
        "battle-1": { "start": 25, "end": 30, "paragraphs": [25, 26, 27, 28, 29, 30] },
        "cultivation_breakthrough": { "start": 15, "end": 17, "paragraphs": [15, 16, 17] }
      },
      "sectionMap": {
        "section-1": { "start": 1, "end": 15 },
        "section-2": { "start": 16, "end": 30 },
        "section-3": { "start": 31, "end": 45 }
      },
      "paragraphTypes": [
        { "index": 1, "type": "narrative" },
        { "index": 5, "type": "dialogue" },
        { "index": 15, "type": "action" },
        { "index": 20, "type": "description" }
      ]
    }
  }
}
```

### 2.3 书籍元数据文件

**文件位置**: `.mighty/books/{book-id}/metadata.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "title": "Book Metadata",
  "description": "书籍级别元数据",
  "properties": {
    "bookId": {
      "type": "string",
      "description": "书籍唯一标识"
    },
    "title": {
      "type": "string",
      "description": "书籍标题"
    },
    "subtitle": {
      "type": "string",
      "description": "副标题"
    },
    "genre": {
      "type": "string",
      "description": "题材类型"
    },
    "subGenre": {
      "type": "string",
      "description": "子题材"
    },
    "wordCountTarget": {
      "type": "integer",
      "description": "目标总字数"
    },
    "chapterCountTarget": {
      "type": "integer",
      "description": "目标章节数"
    },
    "wordsPerChapter": {
      "type": "integer",
      "description": "每章字数"
    },
    "status": {
      "type": "string",
      "enum": ["planning", "writing", "completed", "paused"],
      "description": "书籍状态"
    },
    "createdAt": {
      "type": "string",
      "format": "date-time",
      "description": "创建时间"
    },
    "updatedAt": {
      "type": "string",
      "format": "date-time",
      "description": "最后更新时间"
    },
    "mainCharacters": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "role": { "type": "string", "enum": ["protagonist", "deuteragonist", "antagonist", "supporting"] },
          "description": { "type": "string" }
        }
      },
      "description": "主要角色列表"
    },
    "tags": {
      "type": "array",
      "items": { "type": "string" },
      "description": "标签"
    },
    "profile": {
      "type": "object",
      "properties": {
        "name": { "type": "string" },
        "version": { "type": "string" },
        "path": { "type": "string" }
      },
      "description": "使用的题材配置"
    }
  },
  "required": ["bookId", "title", "genre", "status", "createdAt"]
}
```

---

## 三、索引文件位置

### 3.1 目录结构

```
.mighty/books/{book-id}/
├── metadata.json           # 书籍元数据
├── chapter-index.json      # 章节索引（核心）
├── state.json              # 运行时状态
├── truth/                  # 真相文件目录
│   ├── current_state.md
│   ├── pending_hooks.md
│   ├── chapter_summaries.md
│   ├── emotional_arcs.md
│   ├── character_matrix.md
│   ├── subplot_board.md
│   └── particle_ledger.md
├── chapters/               # 章节内容
│   ├── chapter-001.md
│   ├── chapter-002.md
│   └── ...
└── snapshots/              # 章节快照
    ├── chapter-001/
    │   ├── v1/
    │   │   ├── content.md
    │   │   └── meta.json
    │   └── v2/
    │       ├── content.md
    │       └── meta.json
    └── ...
```

### 3.2 文件说明

| 文件 | 类型 | 大小 | 用途 |
|------|------|------|------|
| `metadata.json` | JSON | ~2KB | 书籍基础信息 |
| `chapter-index.json` | JSON | ~50KB | 所有章节元数据 |
| `state.json` | JSON | ~5KB | 运行时状态 |
| `truth/*.md` | Markdown | ~20KB | 真相文件（Agent可读） |
| `chapters/*.md` | Markdown | ~4MB | 完整章节内容 |
| `snapshots/*/` | Mixed | ~8MB | 历史版本快照 |

---

## 四、索引更新时机

### 4.1 更新触发点

```
┌─────────────────────────────────────────────────────────────┐
│                      章节生命周期                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   [生成] ──────→ [审核] ──────→ [修正] ──────→ [锁定]       │
│      │             │             │             │           │
│      ▼             ▼             ▼             ▼           │
│   创建索引      更新审核分     更新版本     锁定状态         │
│   提取元数据    标记状态       累加版本     禁止修改         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 具体触发条件

| 触发时机 | 操作 | 说明 |
|----------|------|------|
| **章节生成后** | 创建索引条目 | 首次生成章节时创建完整元数据 |
| **审核完成后** | 更新审核分 | 记录质量得分和审计结果 |
| **重写章节后** | 版本+1 | 累加版本号，保留历史 |
| **审核通过后** | 状态→approved | 标记为已批准 |
| **手动锁定后** | 状态→locked | 禁止自动修改 |
| **每日定时** | 同步统计 | 更新总字数、章节数等 |

### 4.3 更新流程

```yaml
chapter_generated:
  - extract_metadata_from_content    # 从内容提取元数据
  - update_chapter_index             # 更新索引条目
  - sync_with_truth_files           # 同步真相文件
  - increment_book_stats            # 更新书籍统计

chapter_rewritten:
  - create_snapshot                 # 创建快照
  - extract_metadata_from_content   # 重新提取
  - update_chapter_index:           # 更新索引
      version: +1
      status: draft
  - sync_with_truth_files

audit_completed:
  - update_chapter_index:
      auditScore: {score}
      status: reviewing
```

---

## 五、Queen Bee 索引使用规范

### 5.1 读取策略

**禁止做法**:

```yaml
❌ 错误 - 读取全部章节:
  context:
    - chapter-001.md  # 4000字
    - chapter-002.md  # 4000字
    - ...
    - chapter-010.md  # 4000字
  total: 40,000字

❌ 错误 - 重复读取:
  - 验证连贯性时再次读取
  - 生成新章节时重复加载
```

**正确做法**:

```yaml
✅ 正确 - 只读索引:
  context:
    - chapter-index.json    # 500字
    - truth/current_state.md  # 2000字
    - truth/pending_hooks.md  # 500字
  total: ~3,000字

✅ 正确 - 按需引用:
  references:
    - "参见 chapter-003.md 第15-20段"
    - "根据 chapter-005 的伏笔..."
```

### 5.2 连贯性验证流程

```yaml
verify_continuity:
  steps:
    1. read_chapter_index:           # 只读索引
       - 获取前3章的 summary
       - 获取关键事件时间线
       - 获取人物出场记录

    2. identify_check_points:        # 确定检查点
       - 修为一致性
       - 人物关系进度
       - 伏笔呼应情况

    3. selective_content_read:       # 选择性读取
       only_if_needed:
         - "chapter-00X.md 第Y段"
       threshold: "无法从索引确定时"

    4. generate_report:
       - 连续性问题列表
       - 建议修改项
       - 通过/失败标记
```

### 5.3 缓存策略

```yaml
cache_policy:
  chapter_index:
    ttl: 300  # 5分钟
    invalidate_on:
      - chapter_updated
      - book_reopened

  truth_files:
    ttl: 60   # 1分钟
    invalidate_on:
      - chapter_completed
      - manual_refresh
```

---

## 六、索引生成自动化

### 6.1 Hook: post-write-extraction

**触发**: 章节写入完成后

**流程**:

```
┌─────────────────────────────────────────────────────────────┐
│                 Post-Write Extraction Hook                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Input: chapter-00X.md (新生成的章节)                        │
│                                                             │
│  Step 1: Parse Content                                      │
│    ├── 提取标题 (从 frontmatter 或 H1)                       │
│    ├── 统计字数 (排除 markdown 标记)                         │
│    └── 识别段落结构                                         │
│                                                             │
│  Step 2: LLM Extraction                                     │
│    ├── 生成摘要 (200字以内)                                  │
│    ├── 识别关键事件                                          │
│    ├── 识别出场角色                                          │
│    ├── 识别场景地点                                          │
│    ├── 识别埋设伏笔                                          │
│    ├── 识别回收伏笔                                          │
│    └── 提取章节悬念                                          │
│                                                             │
│  Step 3: Truth Sync                                         │
│    ├── 更新 chapter_summaries.md                            │
│    ├── 更新 current_state.md                                │
│    ├── 更新 pending_hooks.md                                │
│    └── 更新 character_matrix.md                             │
│                                                             │
│  Step 4: Update Index                                       │
│    ├── 创建/更新 chapter-index.json                         │
│    ├── 更新 metadata.json 统计                              │
│    └── 记录 updatedAt                                       │
│                                                             │
│  Output: 更新后的索引文件                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 元数据提取 Prompt

```yaml
extraction_prompt:
  system: |
    你是一个专业的网文内容分析器。请从提供的章节内容中提取结构化元数据。

  input: |
    章节内容: {{chapter_content}}
    章节编号: {{chapter_number}}

  output_format: |
    ```json
    {
      "title": "章节标题",
      "wordCount": 4000,
      "summary": "200字以内摘要",
      "keyEvents": ["事件1", "事件2"],
      "characters": ["角色A", "角色B"],
      "locations": ["地点1"],
      "foreshadowing": ["新埋设伏笔"],
      "foreshadowingResolved": ["已回收伏笔"],
      "cliffhanger": "本章悬念",
      "emotionalTone": "情感基调"
    }
    ```

  rules:
    - summary 必须控制在200字以内
    - keyEvents 最多5个
    - 只列出本章新埋设的伏笔
    - 只列出本章回收的伏笔
```

### 6.3 与真相文件同步

```yaml
truth_sync_mapping:
  chapter_summaries.md:
    source: chapter-index.json.chapters.*.summary
    format: "## 第X章 {title}\n{summary}\n"

  current_state.md:
    source:
      - chapter-index.json.chapters.*.keyEvents
      - chapter-index.json.chapters.*.characters
    update: append_latest

  pending_hooks.md:
    source:
      created: chapter-index.json.chapters.*.foreshadowing
      resolved: chapter-index.json.chapters.*.foreshadowingResolved
    update: move_from_pending_to_resolved

  character_matrix.md:
    source: chapter-index.json.chapters.*.characters
    update: track_appearances

  semantic_map.md:
    source: chapter-index.json.chapters.*.semanticMap
    update: append_latest
```

---

## 七、语义映射规范

### 7.1 语义标签标准定义

语义标签用于标记章节内具有特定功能的内容段落，支持按需加载系统精确定位。

| 语义标签 | 描述 | 自动检测依据 |
|----------|------|-------------|
| **keyEvents** | 关键事件段落 | 情节转折、重要事件、剧情推进节点 |
| **foreshadowing** | 伏笔段落 | 暗示性内容、未揭晓悬念、后续线索 |
| **cliffhanger** | 结尾钩子 | 章节末尾悬念、吸引读者继续阅读的内容 |
| **dialogue-N** | 第N段重要对话 | 对话标记、角色互动、关键对白（N为序号） |
| **battle-N** | 第N场战斗 | 动作描写、战斗场景、比武场面（N为序号） |
| **cultivation_breakthrough** | 修炼突破 | 境界提升描述、功法突破场景 |
| **emotional_peak** | 情感高潮 | 情绪激烈变化、情感爆发段落 |
| **revelation** | 真相揭示 | 秘密揭晓、谜题解开、重要信息揭露 |
| **flashback** | 回忆段落 | 倒叙内容、过往事件回忆 |
| **description** | 场景描写 | 环境、氛围、细节描写段落 |

### 7.2 语义标签命名规范

```yaml
# 标准格式
semantic_tag:
  # 单实例标签（每章通常只有一个）
  cliffhanger
  keyEvents
  cultivation_breakthrough
  emotional_peak
  revelation

  # 多实例标签（需要序号区分）
  dialogue-1, dialogue-2, dialogue-3...
  battle-1, battle-2, battle-3...
  flashback-1, flashback-2...

# 命名规则
rules:
  - 使用小写字母和下划线
  - 多实例标签使用 "-N" 后缀编号
  - 编号从1开始连续递增
  - 避免使用特殊字符
```

### 7.3 语义映射数据结构

```json
{
  "chapterId": "chapter-003",
  "paragraphCount": 45,
  "semanticMap": {
    "keyEvents": {
      "start": 15,
      "end": 18,
      "paragraphs": [15, 16, 17, 18]
    },
    "foreshadowing": {
      "start": 20,
      "end": 22,
      "paragraphs": [20, 21, 22]
    },
    "cliffhanger": {
      "start": 44,
      "end": 45,
      "paragraphs": [44, 45]
    },
    "dialogue-1": {
      "start": 5,
      "end": 8,
      "paragraphs": [5, 6, 7, 8]
    },
    "dialogue-2": {
      "start": 32,
      "end": 35,
      "paragraphs": [32, 33, 34, 35]
    },
    "battle-1": {
      "start": 25,
      "end": 30,
      "paragraphs": [25, 26, 27, 28, 29, 30]
    },
    "cultivation_breakthrough": {
      "start": 15,
      "end": 17,
      "paragraphs": [15, 16, 17]
    }
  },
  "sectionMap": {
    "section-1": { "start": 1, "end": 15 },
    "section-2": { "start": 16, "end": 30 },
    "section-3": { "start": 31, "end": 45 }
  },
  "paragraphTypes": [
    { "index": 1, "type": "narrative" },
    { "index": 5, "type": "dialogue" },
    { "index": 15, "type": "action" },
    { "index": 20, "type": "description" },
    { "index": 25, "type": "dialogue" },
    { "index": 44, "type": "narrative" }
  ]
}
```

### 7.4 语义映射生成时机

```yaml
# 生成触发点
triggers:
  post_write:
    # 章节写入完成后
    - 分析章节内容结构
    - 识别关键语义段落
    - 生成 semanticMap
    - 更新章节索引

  post_rewrite:
    # 章节重写后
    - 重新分析段落结构
    - 更新语义映射
    - 版本号+1

  manual_trigger:
    # 手动触发
    - 检测到段落标记异常
    - 用户手动重建索引

# 生成流程
generation_flow:
  step_1_parse:
    - 将章节内容分割为段落
    - 统计总段落数
    - 识别段落类型

  step_2_analyze:
    - 使用LLM分析语义内容
    - 识别关键事件位置
    - 标记伏笔和钩子位置

  step_3_build_map:
    - 构建 semanticMap 对象
    - 计算段落范围
    - 验证边界合法性

  step_4_validate:
    - 检查段落编号连续性
    - 验证无重叠区间
    - 确保在有效范围内

  step_5_update:
    - 写入 chapter-index.json
    - 同步 truth/semantic_map.md
```

### 7.5 语义映射更新触发条件

| 触发条件 | 操作 | 说明 |
|----------|------|------|
| 章节重写 | 重新生成 | 内容变化导致段落结构改变 |
| 段落增删 | 重新生成 | 段落数变化影响位置映射 |
| 内容调整 | 部分更新 | 小幅修改可能只影响局部标签 |
| 标签新增 | 追加更新 | 手动添加新语义标签 |
| 版本回滚 | 恢复旧版 | 回退到历史版本的映射 |

### 7.6 与按需加载系统集成

```yaml
# 集成方式
integration:
  # 1. 索引服务层
  index_service:
    - 提供语义标签查询API
    - 返回段落范围信息
    - 支持批量查询

  # 2. 内容加载层
  content_loader:
    - 接收语义引用（如 chapter-003#foreshadowing）
    - 查询索引获取段落范围
    - 按需加载指定段落

  # 3. 缓存层
  cache_manager:
    - 按语义标签缓存内容
    - LRU淘汰策略
    - 支持预热常用标签

# 使用示例
examples:
  # 直接引用
  - "chapter-003#keyEvents" → 加载第15-18段
  - "chapter-003#cliffhanger" → 加载第44-45段

  # 范围引用
  - "chapter-003#paragraph-15-18" → 同 keyEvents

  # 跨标签引用
  - "chapter-003#battle-1" + "chapter-003#dialogue-2" → 组合加载
```

### 7.7 段落类型标记

```yaml
# 段落类型枚举
paragraph_types:
  narrative:      # 叙述段落，推进剧情
  dialogue:       # 对话段落，角色交流
  action:         # 动作段落，战斗或行动
  description:    # 描写段落，场景氛围
  monologue:      # 独白段落，内心活动
  exposition:     # 说明段落，背景解释

# 使用场景
usage:
  - 按需加载时按类型过滤
  - 分析章节结构组成
  - 统计各类段落占比
  - 辅助语义标签识别
```

---

## 八、迁移方案

### 8.1 现有项目迁移

对于已有章节但无索引的项目：

```bash
# 一键迁移命令
/novel-index-rebuild

# 执行流程:
1. 扫描 chapters/ 目录所有章节
2. 读取每章内容提取元数据
3. 生成 chapter-index.json
4. 生成 metadata.json
5. 初始化 truth/ 目录
6. 创建初始快照
```

### 8.2 向后兼容

```yaml
compatibility:
  legacy_mode:
    - 检测是否存在 chapter-index.json
    - 不存在时自动重建
    - Queen Bee 回退到完整读取模式

  migration_warning:
    - 首次使用时提示重建索引
    - 显示预计时间和 Token 消耗
```

---

## 九、验收标准

### 9.1 功能验收

- [ ] `chapter-index.json` Schema 验证通过
- [ ] `metadata.json` 生成正确
- [ ] 章节写入后自动更新索引
- [ ] 重写后版本号正确累加
- [ ] 真相文件与索引同步更新
- [ ] `semanticMap` 字段正确生成
- [ ] 语义标签引用正常工作
- [ ] 按需加载系统可正确解析语义引用

### 9.2 性能验收

- [ ] Queen Bee 上下文使用量 < 10,000 字（前10章）
- [ ] 连贯性验证时间 < 5s
- [ ] 索引生成时间 < 3s
- [ ] 支持 100+ 章节索引
- [ ] 按需加载节省 90%+ 上下文

### 9.3 集成验收

- [ ] `/novel-write` 命令自动更新索引
- [ ] `/novel-rewrite` 命令正确处理版本
- [ ] `/novel-review` 使用索引进行验证
- [ ] 快照系统与索引版本对应
- [ ] 语义映射与按需加载系统正常集成

---

## 十、相关文档

- [findings.md](../../findings.md) - 项目级问题分析和解决方案
- [task_plan.md](../../task_plan.md) - 当前活跃计划
- [truth-files-guide.md](./truth-files-guide.md) - 真相文件使用指南
- [post-write-validator.md](../validators/post-write-validator.md) - 写后验证器
- [on-demand-loading.md](./on-demand-loading.md) - 按需加载技术方案

---

**文档历史**:

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.1 | 2026-03-18 | 添加 semanticMap 支持按需加载系统 |
| v1.0 | 2026-03-18 | 初始版本 |
