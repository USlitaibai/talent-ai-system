# ==========================================================
# Talent AI System - Docker 首次初始化脚本（Windows PowerShell）
#
# 作用：
#   1. 等待 ollama 健康
#   2. 拉取所需 Ollama 模型（一次性，约 2.4GB）
#   3. 等待 app 就绪并做健康检查
#
# 使用：
#   powershell -ExecutionPolicy Bypass -File scripts\docker-init.ps1
# ==========================================================

$ErrorActionPreference = "Stop"

$AppUrl     = "http://localhost:8000/"
$ModelLlm   = if ($env:OLLAMA_MODEL)       { $env:OLLAMA_MODEL }       else { "qwen3:4b" }
$ModelEmbed = if ($env:OLLAMA_EMBED_MODEL) { $env:OLLAMA_EMBED_MODEL } else { "nomic-embed-text:latest" }

Write-Host "============================================================"
Write-Host " Talent AI System - Docker 初始化"
Write-Host "============================================================"

# ----------------------------------------------------------
# 1. 等待 ollama 健康
# ----------------------------------------------------------

Write-Host ""
Write-Host "[1/3] 等待 ollama 服务就绪 ..."

$ok = $false
for ($i = 1; $i -le 60; $i++) {
    docker compose exec -T ollama ollama list *> $null
    if ($LASTEXITCODE -eq 0) { $ok = $true; break }
    Start-Sleep -Seconds 2
}

if (-not $ok) {
    Write-Host "      !! ollama 未在预期时间内就绪，请检查: docker compose logs ollama"
    exit 1
}
Write-Host "      ollama 已就绪"

# ----------------------------------------------------------
# 2. 拉取模型
# ----------------------------------------------------------

Write-Host ""
Write-Host "[2/3] 拉取 Ollama 模型（首次约 2.4GB，请耐心等待）"

$existing = (docker compose exec -T ollama ollama list) -join "`n"

foreach ($model in @($ModelEmbed, $ModelLlm)) {

    $base = $model.Split(":")[0]

    if ($existing -match [regex]::Escape($base)) {
        Write-Host "      $model 已存在，跳过"
        continue
    }

    Write-Host "      正在拉取 $model ..."
    docker compose exec -T ollama ollama pull $model

    if ($LASTEXITCODE -ne 0) {
        Write-Host "      !! 拉取 $model 失败"
        exit 1
    }
}

Write-Host ""
Write-Host "      当前模型列表："
docker compose exec -T ollama ollama list

# ----------------------------------------------------------
# 3. 等待 app 就绪
# ----------------------------------------------------------

Write-Host ""
Write-Host "[3/3] 等待应用就绪 ..."

$ok = $false
for ($i = 1; $i -le 60; $i++) {
    try {
        Invoke-WebRequest -Uri $AppUrl -TimeoutSec 5 -UseBasicParsing *> $null
        $ok = $true
        break
    } catch {
        Start-Sleep -Seconds 2
    }
}

if (-not $ok) {
    Write-Host "      !! 应用未在预期时间内就绪，请检查: docker compose logs app"
    exit 1
}
Write-Host "      应用已就绪"

Write-Host ""
Write-Host "============================================================"
Write-Host " 初始化完成"
Write-Host ""
Write-Host "   接口文档  ${AppUrl}docs"
Write-Host "   健康检查  ${AppUrl}"
Write-Host ""
Write-Host " 其他常用命令："
Write-Host "   docker compose ps           查看状态"
Write-Host "   docker compose logs -f app  查看应用日志"
Write-Host "   docker compose down         停止（保留数据）"
Write-Host "============================================================"
