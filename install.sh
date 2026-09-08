#!/usr/bin/env bash
# 辞达（Cídá）安装脚本
# 默认安装到 Claude Code 的用户级 skills 目录：~/.claude/skills/cida
# 用法：
#   bash install.sh              # 安装到 ~/.claude/skills/cida（符号链接）
#   bash install.sh --copy       # 复制而非链接
#   bash install.sh --project    # 安装到当前目录的 .claude/skills/cida
#   bash install.sh --dir <path> # 安装到指定目录
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODE="link"
DEST_ROOT="${HOME}/.claude/skills"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --copy)    MODE="copy"; shift ;;
    --project) DEST_ROOT="$(pwd)/.claude/skills"; shift ;;
    --dir)     DEST_ROOT="$2"; shift 2 ;;
    -h|--help)
      grep '^#' "$0" | sed 's/^# \?//'; exit 0 ;;
    *) echo "未知参数: $1"; exit 1 ;;
  esac
done

DEST="${DEST_ROOT}/cida"
mkdir -p "${DEST_ROOT}"

if [[ -e "${DEST}" || -L "${DEST}" ]]; then
  echo "已存在：${DEST}"
  echo "如需重装，请先移除：rm -rf '${DEST}'"
  exit 1
fi

if [[ "${MODE}" == "link" ]]; then
  ln -s "${SRC}" "${DEST}"
  echo "✓ 已链接 ${DEST} -> ${SRC}"
else
  rsync -a --exclude '.git' --exclude 'site' "${SRC}/" "${DEST}/"
  echo "✓ 已复制到 ${DEST}"
fi

echo ""
echo "辞达已就绪。在 Claude Code 中直接说："
echo "  「帮我把这篇文章改得更自然」 / 「把这段转录整理成文章」"
echo ""
echo "Codex / OpenCode 用户无需本脚本：将本仓库克隆到工作区，"
echo "根目录 AGENTS.md 会自动引导 agent 进入 SKILL.md。"
