"""
游戏资源宝库 - API 服务
Coze 付费插件后端

使用说明：
1. 安装依赖：pip install flask flask-cors
2. 运行服务：python app.py
3. 部署到公网（需要公网访问）

API 端点：
- GET /api/search?game=xxx&type=xxx
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import random
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# ============ 资源数据库（可扩展）===========
# 实际生产环境应该从数据库或配置文件读取
GAME_RESOURCES = {
    "原神": {
        "攻略": [
            {"title": "原神 Wiki 攻略", "url": "https://wiki.biligame.com/ys/", "source": "B站wiki" },
            {"title": "原神攻略 - NGA", "url": "https://nga.178.com/ys/", "source": "NGA" },
            {"title": "原神全角色培养攻略", "url": "https://genshin.honeyhunterworld.com/", "source": "Honey" }
        ],
        "视频": [
            {"title": "原神 B站官方", "url": "https://space.bilibili.com/395341833", "source": "B站" },
            {"title": "原神攻略视频", "url": "https://search.bilibili.com/article?keyword=原神攻略", "source": "B站" }
        ],
        "MOD": [
            {"title": "原神画质MOD", "url": "https://www.bilibili.com/video/BV1GJ411x7h7/", "source": "B站" },
            {"title": "原神类MOD合集", "url": "https://www.aplaybox.com/", "source": "Aplaybox" }
        ],
        "下载": [
            {"title": "原神官方下载", "url": "https://ys.mihoyo.com/", "source": "官网" }
        ],
        "论坛": [
            {"title": "原神 NGA 论坛", "url": "https://nga.178.com/ys/", "source": "NGA" },
            {"title": "原神 TapTap 社区", "url": "https://www.taptap.com/app/168883", "source": "TapTap" }
        ]
    },
    "我的世界": {
        "攻略": [
            {"title": "MC Wiki 中文百科", "url": "https://minecraft.fandom.com/zh/wiki/", "source": "Fandom" },
            {"title": "我的世界 攻略 - NGA", "url": "https://nga.178.com/mc/", "source": "NGA" }
        ],
        "视频": [
            {"title": "Minecraft B站教程", "url": "https://search.bilibili.com/video?keyword=Minecraft教程", "source": "B站" },
            {"title": "我的世界 官方", "url": "https://space.bilibili.com/11056280", "source": "B站" }
        ],
        "MOD": [
            {"title": "CurseForge MC MOD", "url": "https://www.curseforge.com/minecraft/mc-mods", "source": "CurseForge" },
            {"title": "MC 模组网", "url": "https://www.mcmod.cn/", "source": "MC模组网" },
            {"title": "MCBBS 模组区", "url": "https://www.mcbbs.net/forum-mod-1.html", "source": "MCBBS" }
        ],
        "下载": [
            {"title": "MC 官方启动器下载", "url": "https://www.minecraft.net/zh-hans/download", "source": "官网" },
            {"title": "HMCL 启动器", "url": "https://hmcl.huangyuhui.cn/", "source": "HMCL" }
        ],
        "论坛": [
            {"title": "MCBBS", "url": "https://www.mcbbs.net/", "source": "MCBBS" },
            {"title": "MC 百科", "url": "https://www.mcmod.cn/", "source": "MC百科" }
        ]
    },
    "王者荣耀": {
        "攻略": [
            {"title": "王者荣耀 攻略 - NGA", "url": "https://nga.178.com/wzry/", "source": "NGA" },
            {"title": "王者营地 攻略", "url": "https://pvp.qq.com/web201606/", "source": "官网" }
        ],
        "视频": [
            {"title": "王者荣耀 KPL", "url": "https://pvp.qq.com/kpl/", "source": "官网" },
            {"title": "B站王者荣耀", "url": "https://search.bilibili.com/video?keyword=王者荣耀教程", "source": "B站" }
        ],
        "MOD": [],
        "下载": [
            {"title": "王者荣耀 下载", "url": "https://pvp.qq.com/", "source": "官网" }
        ],
        "论坛": [
            {"title": "王者荣耀 NGA", "url": "https://nga.178.com/wzry/", "source": "NGA" },
            {"title": "TapTap 王者荣耀", "url": "https://www.taptap.com/app/63398", "source": "TapTap" }
        ]
    },
    "崩坏星穹铁道": {
        "攻略": [
            {"title": "星穹铁道 Wiki", "url": "https://wiki.biligame.com/sr/", "source": "B站wiki" },
            {"title": "星穹铁道 攻略", "url": "https://nga.178.com/sr/", "source": "NGA" }
        ],
        "视频": [
            {"title": "星穹铁道 B站", "url": "https://space.bilibili.com/7736062", "source": "B站" }
        ],
        "MOD": [],
        "下载": [
            {"title": "星穹铁道 官网", "url": "https://sr.mihoyo.com/", "source": "官网" }
        ],
        "论坛": [
            {"title": "星穹铁道 NGA", "url": "https://nga.178.com/sr/", "source": "NGA" }
        ]
    },
    "CS": {
        "攻略": [
            {"title": "CS2 攻略 - NGA", "url": "https://nga.178.com/cs2/", "source": "NGA" },
            {"title": "CSGO 完美攻略", "url": "https://www.wanplus.com/csgo/strategy", "source": "完美" }
        ],
        "视频": [
            {"title": "CS2 B站教程", "url": "https://search.bilibili.com/video?keyword=CS2教程", "source": "B站" },
            {"title": "CSGO 官方", "url": "https://www.csgo.com.cn/", "source": "CSGO中文网" }
        ],
        "MOD": [
            {"title": "CS2 皮肤合集", "url": "https://csgo.gamersclub.gg/", "source": "GamersClub" },
            {"title": "CSGO 换肤", "url": "https://csgostash.com/", "source": "CSGOSTASH" }
        ],
        "下载": [
            {"title": "CS2 Steam 下载", "url": "https://store.steampowered.com/app/730/CounterStrike_2/", "source": "Steam" }
        ],
        "论坛": [
            {"title": "CSGO NGA", "url": "https://nga.178.com/cs2/", "source": "NGA" },
            {"title": "完美电竞", "url": "https://www.wanplus.com/csgo", "source": "完美" }
        ]
    },
    "英雄联盟": {
        "攻略": [
            {"title": "英雄联盟 Wiki", "url": "https://wiki.biligame.com/lol/", "source": "B站wiki" },
            {"title": "LOL NGA 攻略", "url": "https://nga.178.com/lol/", "source": "NGA" },
            {"title": "OP.GG 攻略", "url": "https://www.op.gg/", "source": "OP.GG" }
        ],
        "视频": [
            {"title": "英雄联盟 官方", "url": "https://space.bilibili.com/484436528", "source": "B站" },
            {"title": "LPL 官方", "url": "https://lpl.qq.com/", "source": "LPL" }
        ],
        "MOD": [],
        "下载": [
            {"title": "LOL 客户端下载", "url": "https://lol.qq.com/download/", "source": "官网" }
        ],
        "论坛": [
            {"title": "LOL NGA", "url": "https://nga.178.com/lol/", "source": "NGA" },
            {"title": "TapTap 英雄联盟", "url": "https://www.taptap.com/app/6850", "source": "TapTap" }
        ]
    }
}


def fuzzy_match_game(game_name):
    """模糊匹配游戏名"""
    game_name_lower = game_name.lower()
    
    # 精确匹配
    if game_name in GAME_RESOURCES:
        return game_name
    
    # 模糊匹配
    for game in GAME_RESOURCES:
        if game_name_lower in game.lower() or game.lower() in game_name_lower:
            return game
    
    # 常用别名映射
    aliases = {
        "mc": "我的世界",
        "我的世界": "我的世界",
        "minecraft": "我的世界",
        "原神": "原神",
        "genshin": "原神",
        "王者": "王者荣耀",
        "农药": "王者荣耀",
        "lol": "英雄联盟",
        "英雄联盟": "英雄联盟",
        "csgo": "CS",
        "cs2": "CS",
        "cs": "CS",
        "崩坏星穹铁道": "崩坏星穹铁道",
        "星穹铁道": "崩坏星穹铁道",
        "星铁": "崩坏星穹铁道",
        "sr": "崩坏星穹铁道"
    }
    
    for key, value in aliases.items():
        if key in game_name_lower:
            return value
    
    return None


# ============ API 路由 ============

@app.route('/api/search', methods=['GET', 'POST'])
def search():
    """
    搜索游戏资源
    
    参数：
    - game: 游戏名称
    - type: 资源类型 (攻略/视频/MOD/下载/论坛)
    - limit: 返回数量限制
    """
    game = request.args.get('game', '')
    resource_type = request.args.get('type', '')
    limit = int(request.args.get('limit', 10))
    
    if not game:
        return jsonify({
            "success": False,
            "message": "请输入游戏名称"
        }), 400
    
    # 匹配游戏
    matched_game = fuzzy_match_game(game)
    
    if not matched_game:
        return jsonify({
            "success": False,
            "message": f"未找到游戏 '{game}'，请尝试其他关键词"
        }), 404
    
    game_data = GAME_RESOURCES[matched_game]
    
    # 默认返回所有类型
    if not resource_type:
        results = []
        for res_type, resources in game_data.items():
            for res in resources[:3]:
                results.append({
                    "type": res_type,
                    "title": res["title"],
                    "url": res["url"],
                    "source": res["source"]
                })
        return jsonify({
            "success": True,
            "game": matched_game,
            "results": results[:limit]
        })
    
    # 指定类型
    if resource_type not in game_data:
        return jsonify({
            "success": False,
            "message": f"暂不支持 '{resource_type}' 类型，支持: {', '.join(game_data.keys())}"
        }), 404
    
    resources = game_data[resource_type]
    results = [{
        "type": resource_type,
        "title": r["title"],
        "url": r["url"],
        "source": r["source"]
    } for r in resources[:limit]]
    
    return jsonify({
        "success": True,
        "game": matched_game,
        "type": resource_type,
        "results": results
    })


@app.route('/api/games', methods=['GET', 'POST'])
def get_games():
    """获取支持的游戏列表"""
    return jsonify({
        "success": True,
        "games": list(GAME_RESOURCES.keys())
    })


@app.route('/api/types', methods=['GET', 'POST'])
def get_types():
    """获取支持的资源类型"""
    return jsonify({
        "success": True,
        "types": ["攻略", "视频", "MOD", "下载", "论坛"]
    })
@app.route('/openapi.json', methods=['GET', 'POST'])
def openapi():
 """返回 OpenAPI 规范（Coze 插件用）"""
 return jsonify({
 "openapi": "3.0.0",
 "info": {
 "title": "游戏资源宝库 API",
 "version": "1.0.0"
 },
 "paths": {
 "/api/search": {
 "get": {
 "operationId": "search_game",
 "summary": "搜索游戏资源",
 "parameters": [
 {"name": "game", "in": "query", "required": True},
 {"name": "type", "in": "query"},
 {"name": "limit", "in": "query"}
 ],
 "responses": {"200": {"description": "OK"}}
 }
 },
 "/api/games": {"get": {"responses": {"200": {"description": "OK"}}}},
 "/api/types": {"get": {"responses": {"200": {"description": "OK"}}}},
 "/health": {"get": {"responses": {"200": {"description": "OK"}}}}
 }
 })


@app.route('/health', methods=['GET', 'POST'])
def health():
    """健康检查"""
    return jsonify({"status": "ok", "service": "游戏资源宝库 API"})


# ============ Coze 插件配置 ============
def generate_coze_plugin_config():
    """生成 Coze 插件配置"""
    return {
        "schema_version": "v2",
        "name": "游戏资源宝库",
        "description": "输入游戏名称和资源类型，快速获取游戏攻略、视频、MOD、下载链接、论坛社区等资源。支持主流游戏：原神、王者荣耀、我的世界、英雄联盟、CS2、崩坏星穹铁道等。",
        "icon": "🎮",
        "category": "工具",
        "price": {
            "type": "subscription",
            "monthly_price": 9.9,
            "free_quota": 10,
            "quota_unit": "次/天"
        },
        "tools": [
            {
                "name": "search_game_resource",
                "description": "搜索游戏资源，包括攻略、视频、MOD、下载、论坛等",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "game": {
                            "type": "string",
                            "description": "游戏名称，如：原神、王者荣耀、我的世界、英雄联盟、CS2、崩坏星穹铁道"
                        },
                        "type": {
                            "type": "string",
                            "description": "资源类型：攻略、视频、MOD、下载、论坛（不填则返回所有类型）"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "返回结果数量，默认10"
                        }
                    },
                    "required": ["game"]
                }
            },
            {
                "name": "list_games",
                "description": "获取支持的游戏列表"
            },
            {
                "name": "list_types",
                "description": "获取支持的资源类型"
            }
        ]
    }


if __name__ == '__main__':
    print("=" * 50)
    print("🎮 游戏资源宝库 API 服务")
    print("=" * 50)
    print("服务地址: http://localhost:5000")
    print("API 文档: http://localhost:5000/api")
    print("")
    print("支持的 API 端点:")
    print("  GET /api/search?game=游戏名&type=类型")
    print("  GET /api/games")
    print("  GET /api/types")
    print("  GET /health")
    print("=" * 50)
    
    # 生成 Coze 配置
    config = generate_coze_plugin_config()
    print("\n📦 Coze 插件配置:")
    print(config)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
