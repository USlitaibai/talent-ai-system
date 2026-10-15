#!/usr/bin/env bash
# ==========================================================
# Talent AI System - Docker 首次初始化脚本
#
# 作用：
#   1. 等待 mysql / ollama 健康
#   2. 拉取所需 Ollama 模型（一次性，约 2.4GB）
#   3. 等待 app 就绪并做健康检查
#
# 使用：
#   bash scripts/docker-init.sh
# ==========================================================

set -e

APP_URL="http://localhost:8000/"
MODEL_LLM="${OLLAMA_MODEL:-qwen3:4b}"
MODEL_EMBED="${OLLAMA_EMBED_MODEL:-nomic-embed-text:latest}"

echo "============================================================"
echo " Talent AI System - Docker 初始化"
echo "============================================================"

# ----------------------------------------------------------
# 1. 等待 ollama 健康
# ----------------------------------------------------------

echo ""
echo "[1/3] 等待 ollama 服务就绪 ..."

for i in $(seq 1 60); do
    if docker compose exec -T ollama ollama list >/dev/null 2>&1; then
        echo "      ollama 已就绪"
        break
    fi
    if [ "$i" -eq 60 ]; then
        echo "      !! ollama 未在预期时间内就绪，请检查: docker compose logs ollama"
        exit 1
    fi
    sleep 2
done

# ----------------------------------------------------------
# 2. 拉取模型
# ----------------------------------------------------------

echo ""
echo "[2/3] 拉取 Ollama 模型（首次约 2.4GB，请耐心等待）"

for model in "$MODEL_EMBED" "$MODEL_LLM"; do
    if docker compose exec -T ollama ollama list | grep -q "${model%%:*}"; then
        echo "      $model 已存在，跳过"
    else
        echo "      正在拉取 $model ..."
        docker compose exec -T ollama ollama pull "$model"
    fi
done

echo ""
echo "      当前模型列表："
docker compose exec -T ollama ollama list

# ----------------------------------------------------------
# 3. 等待 app 就绪
# ----------------------------------------------------------

echo ""
echo "[3/3] 等待应用就绪 ..."

for i in $(seq 1 60); do
    if curl -fsS "$APP_URL" >/dev/null 2>&1; then
        echo "      应用已就绪"
        break
    fi
    if [ "$i" -eq 60 ]; then
        echo "      !! 应用未在预期时间内就绪，请检查: docker compose logs app"
        exit 1
    fi
    sleep 2
done

echo ""
echo "============================================================"
echo " 初始化完成"
echo ""
echo "   接口文档  ${APP_URL}docs"
echo "   健康检查  ${APP_URL}"
echo ""
echo " 其他常用命令："
echo "   docker compose ps           查看状态"
echo "   docker compose logs -f app  查看应用日志"
echo "   docker compose down         停止（保留数据）"
echo "============================================================"
