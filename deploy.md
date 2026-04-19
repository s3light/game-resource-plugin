# 游戏资源宝库 - 部署指南

## 文件结构

```
game-resource-plugin/
├── app.py              # API 服务主程序（必部署）
├── coze-plugin.json    # Coze 插件配置（提交给 Coze 后台）
├── README.md           # 插件说明文档
└── deploy.md           # 本部署指南
```

---

## 部署步骤

### 第一步：部署 API 服务

你需要把 `app.py` 部署到一个**公网可访问的服务器**。

#### 推荐方案（免费/低成本）：

| 方案 | 费用 | 难度 | 说明 |
|------|------|------|------|
| **Railway** | 免费 | ⭐⭐ | 部署简单，支持 Python |
| **Render** | 免费 | ⭐⭐ | 适合后端服务 |
| **Vercel** | 免费 | ⭐⭐ | 需要适配 Vercel 格式 |
| **火山引擎/阿里云函数** | 免费 | ⭐⭐⭐ | 国内访问快 |

#### Railway 部署教程：
1. 注册 [Railway.app](https://railway.app)
2. 点击 "New Project" → "Deploy from GitHub" 或上传 ZIP
3. 配置文件：`railway.json`（自动检测 Python）
4. 部署后获取 URL，如：`https://your-app.railway.app`

---

### 第二步：配置 Coze 插件

1. 打开 [Coze开发者后台](https://coze.com)
2. 创建新插件 → 填写信息
3. 在插件配置中：
   - 填入你的 API 地址（如 `https://your-app.railway.app`）
   - 复制 `coze-plugin.json` 中的 tool 配置
4. 设置定价：¥9.9/月，每日免费 10 次
5. 提交审核

---

### 第三步：测试你的 API

部署成功后，访问：
```
https://你的API地址/api/search?game=原神&type=攻略
```

应返回：
```json
{
  "success": true,
  "game": "原神",
  "type": "攻略",
  "results": [...]
}
```

---

## 收入分成

- Coze 商店收入分成比例：你拿大头（具体看 Coze 政策）
- 付费用户通过 Coze 付款，你自动获得收入

---

## 后续优化

- [ ] 增加更多游戏数据
- [ ] 添加搜索历史记录
- [ ] 对接真实数据源（爬虫/API）
- [ ] 增加付费专属资源

---

## 常见问题

**Q: 我不懂代码怎么办？**
A: 找会 Python 的人帮你部署，或者用 Railway 的自动部署。

**Q: 需要服务器费用吗？**
A: 免费方案（Railway/Render）基本免费，流量小不要钱。

**Q: 能赚钱吗？**
A: 看你的插件质量了。好的工具类插件可以吸引大量用户。

---

有问题随时问我！