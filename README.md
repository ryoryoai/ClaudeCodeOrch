# Claude Code Bootstrap

Claude Code を使った開発を効率化するためのテンプレートプロジェクトです。
要件定義から **実装 → レビュー → テストGreen** までを一気通貫で回しつつ、複数日・複数セッションでも進捗が崩れない **長期運用Harness**（進捗・意思決定・リスク管理）を提供します。

---

## 前提条件

- [Claude Code](https://claude.ai/code) がインストールされていること
- Node.js 18以上（MCP サーバー利用時）
- Git

---

## インストール

### 方法1: このリポジトリをクローン

```bash
git clone https://github.com/your-org/ClaudeCodeBootstrap.git my-project
cd my-project
rm -rf .git
git init
```

### 方法2: 既存プロジェクトにコピー

```bash
# 必要なディレクトリをコピー
cp -r ClaudeCodeBootstrap/.claude your-project/
cp -r ClaudeCodeBootstrap/harness your-project/
cp -r ClaudeCodeBootstrap/scripts your-project/
cp ClaudeCodeBootstrap/CLAUDE.md your-project/
```

---

## ディレクトリ構成

```
.
├── .claude/
│   ├── agents/           # エージェント定義（役割分担）
│   │   ├── harness-manager.md
│   │   ├── req-analyst.md
│   │   ├── implementer.md
│   │   ├── code-reviewer.md
│   │   └── test-runner.md
│   ├── commands/         # スラッシュコマンド
│   │   ├── start-session.md
│   │   ├── end-session.md
│   │   ├── implement.md
│   │   ├── review-changes.md
│   │   └── run-tests.md
│   ├── skills/           # スキル定義
│   │   ├── harness-maintenance/
│   │   ├── quality-gates/
│   │   ├── req-to-plan/
│   │   ├── review-checklist/
│   │   └── test-strategy/
│   ├── hooks/            # ツール実行フック
│   └── settings.json     # Claude Code 設定（MCP、Hook等）
├── harness/              # 長期運用ハーネス
│   ├── PROGRESS.md       # 進捗・次の一手
│   ├── FEATURES.json     # 機能一覧（構造化）
│   ├── WORKLOG.md        # 作業ログ
│   ├── DECISIONS.md      # 重要な判断
│   └── RISKS.md          # リスク管理
├── scripts/              # CI/テストスクリプト
│   ├── ci.sh             # フルテスト実行
│   ├── quickcheck.sh     # クイックチェック
│   ├── lint.sh           # Lint実行
│   └── security_scan.sh  # セキュリティスキャン
├── spec/                 # 要件定義（作成が必要）
│   └── REQ.md            # 要件定義ファイル
├── docs/                 # ドキュメント出力先
└── CLAUDE.md             # プロジェクトルール
```

---

## 使い方

### 1. セッション開始

プロジェクトディレクトリで Claude Code を起動し、以下のコマンドを実行:

```
/start-session
```

このコマンドで `harness/` 内のファイルを読み込み、前回の状態を把握して作業を再開します。

### 2. 要件定義から開発を開始

1. `spec/REQ.md` に要件を記述
2. 以下のコマンドで実装計画を作成:

```
/implement
```

### 3. テスト実行

```
/run-tests
```

### 4. コードレビュー

```
/review-changes
```

### 5. セッション終了

```
/end-session
```

進捗を `harness/` に保存し、次回セッションで再開できる状態にします。

---

## E2E ワークフロー

1. **harness-manager**: Harness 整備・現状把握
2. **req-analyst**: 要件 → 実装計画（`docs/IMPLEMENTATION_PLAN.md`）
3. **implementer**: 実装＋テスト追加
4. **code-reviewer**: 差分レビュー（読み取り専用）
5. **implementer**: 指摘反映
6. **test-runner**: フルテスト → Green まで
7. **harness-manager**: Harness 最終更新

---

## MCP サーバー

`.claude/settings.json` で以下の MCP サーバーが設定済み:

| サーバー | 説明 |
|---------|------|
| memory | セッション間の記憶保持 |
| git | Git 操作（diff, log, search） |
| fetch | Web コンテンツ取得 |
| sequential-thinking | 段階的思考 |
| filesystem | ファイルシステム操作 |
| playwright | E2E テスト・ブラウザ自動化 |
| github | GitHub API（要: `GITHUB_TOKEN` 環境変数） |

---

## カスタマイズ

### テストスクリプト

`scripts/ci.sh` はプロジェクトのテスト方法を自動検出しますが、独自のテストコマンドがある場合は `scripts/project_ci.sh` を作成してください:

```bash
#!/usr/bin/env bash
# scripts/project_ci.sh
your-test-command
```

### スキルの追加

`.claude/skills/` に新しいディレクトリを作成し、`SKILL.md` を配置:

```
.claude/skills/your-skill/
└── SKILL.md
```

---

## 注意事項

- Hook で実行するシェルスクリプトはあなたの環境権限で動きます。内容は必ず目視確認してください。
- `GITHUB_TOKEN` 環境変数を設定すると GitHub MCP サーバーが利用可能になります。

---

## ライセンス

MIT
