# ClaudeCodeBootstrap

Claude Code を使った AI 駆動開発のための配布用 Bootstrap リポジトリです。

## 概要

このリポジトリは [Upstream Guardian](https://github.com/your-org/claude-upstream-guardian) で検証済みの skills / agents / hooks / harness のみを含む「安定版」です。

## 特徴

- **検証済み**: Upstream Guardian による回帰テストをパス
- **バージョン管理**: tag 固定運用でデグレを防止
- **即座に利用可能**: clone してすぐに使える構成

## ディレクトリ構成

```
ClaudeCodeBootstrap/
├─ .claude/
│  ├─ skills/           # Claude Code スキル定義
│  ├─ agents/           # Claude Code エージェント定義
│  └─ settings.json     # 設定（hooks含む）
├─ hooks/               # フックスクリプト
├─ harness/             # 回帰テスト
│  └─ tests/
├─ docs/
│  ├─ WORKFLOW.md       # 運用ガイド
│  ├─ COMPATIBILITY.md  # 互換性マトリクス
│  └─ CHANGELOG.md      # 変更履歴
├─ Makefile
└─ README.md
```

## セットアップ

```bash
# 1. リポジトリをクローン（本番は tag 固定）
git clone https://github.com/your-org/ClaudeCodeBootstrap.git
cd ClaudeCodeBootstrap
git checkout v1.0.0  # 本番環境

# 2. 依存関係をインストール
pip install -r requirements.txt -r requirements-dev.txt

# 3. 回帰テストを実行
make regression
```

## 使用方法

### スキルを使う

```bash
# /review でコードレビュースキルを呼び出し
claude
> /review
```

### エージェントを使う

```bash
# explorer エージェントでコードベースを探索
claude
> @explorer find all API endpoints
```

## 回帰テスト

```bash
make regression
```

以下を検証:
- hooks: stdin JSON 契約、exit code（0/1/2）
- skills: YAML frontmatter（name, description, path）
- agents: YAML frontmatter（name, description, tools, model）

## バージョン管理

**重要**: 本番環境では必ず tag 固定で使用してください。

```bash
# 現在のバージョンを確認
git describe --tags

# 特定のバージョンに切り替え
git checkout v1.0.0
```

## 上流追従

このリポジトリは [Upstream Guardian](https://github.com/your-org/claude-upstream-guardian) と連携しています。

1. Upstream Guardian が上流の変更を検知
2. 回帰テストを実行
3. 検証済みの場合のみ PR を作成
4. 手動レビュー後にマージ（自動マージ禁止）
5. 新しい tag を作成

## 顧客案件での使用

顧客案件では Bootstrap の最新版追従は **禁止** です。

- 案件開始時に特定の tag をチェックアウト
- 案件期間中はそのバージョンを固定
- アップグレードが必要な場合は Change Request を起票

## ドキュメント

- [WORKFLOW.md](docs/WORKFLOW.md) - 運用ガイド
- [COMPATIBILITY.md](docs/COMPATIBILITY.md) - 互換性マトリクス
- [CHANGELOG.md](docs/CHANGELOG.md) - 変更履歴

## ライセンス

MIT License
