#!/usr/bin/env bash
# 辞达（Cídá）安装脚本
# 用法：
#   bash install.sh              # 安全复制安装
#   bash install.sh --project    # 安装到当前目录的 .claude/skills/cida
#   bash install.sh --dir <path> # 安装到指定目录
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST_ROOT="${HOME}/.claude/skills"

while [[ $# -gt 0 ]]; do
  case "$1" in
  --copy)    shift ;;
    --link)
      echo "不支持符号链接安装，请使用默认的安全复制方式。" >&2
      exit 1
      ;;
    --project) DEST_ROOT="$(pwd)/.claude/skills"; shift ;;
    --dir)     DEST_ROOT="$2"; shift 2 ;;
    -h|--help)
      grep '^#' "$0" | sed 's/^# \?//'; exit 0 ;;
    *) echo "未知参数: $1"; exit 1 ;;
  esac
done

DEST="${DEST_ROOT}/cida"

if [[ -e "${DEST}" || -L "${DEST}" ]]; then
  echo "已存在：${DEST}"
  echo "请先移走或重命名已有目录，再重新安装。"
  exit 1
fi

mkdir -p "${DEST_ROOT}"
mkdir -p "${DEST}"
rsync -a \
  --include='/LICENSE' \
  --include='/SKILL.md' \
  --include='/STYLE_SYSTEM.md' \
  --include='/workflows/' \
  --include='/workflows/***' \
  --include='/platforms/' \
  --include='/platforms/***' \
  --include='/knowledge/' \
  --include='/knowledge/anti_patterns/' \
  --include='/knowledge/anti_patterns/***' \
  --include='/knowledge/conversation/' \
  --include='/knowledge/conversation/***' \
  --include='/knowledge/discourse/' \
  --include='/knowledge/discourse/***' \
  --include='/knowledge/hosting/' \
  --include='/knowledge/hosting/***' \
  --include='/knowledge/mechanisms/' \
  --include='/knowledge/mechanisms/*.md' \
  --include='/knowledge/pragmatics/' \
  --include='/knowledge/pragmatics/***' \
  --include='/knowledge/register/' \
  --include='/knowledge/register/***' \
  --include='/knowledge/rhetoric/' \
  --include='/knowledge/rhetoric/***' \
  --include='/knowledge/writing/' \
  --include='/knowledge/writing/***' \
  --exclude='*' \
  "${SRC}/" "${DEST}/"
echo "✓ 已安全复制到 ${DEST}"
echo
echo "辞达已就绪。在 Claude Code 中直接说："
echo "  「帮我把这篇文章改得更自然」 / 「把这段转录整理成文章」"
echo
echo "Codex / OpenCode 用户无需本脚本：将本仓库克隆到工作区，"
echo "根目录 AGENTS.md 会自动引导 agent 进入 SKILL.md。"
