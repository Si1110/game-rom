## 说明

修改下面的变量值，运行 `python py/generate_game_site.py` 脚本时会自动读取这些变量，在 python 生成网站源码的同时，自动填充 html 模板中。


### html 页面标题和提示

> 影响 `index.html`, `sections/*`

```
SITE_TITLE=26000+款怀旧游戏ROM合集 - GBA/FC/SFC/N64/NDS/PS中文版下载

INDEX_TITLE=🎮 经典怀旧游戏 ROM 合集 🎮
```



### SEO 配置（用于优化搜索引擎推荐排名）

> 影响 `docs/js/seo-meta.js`


```
SEO_TITLE=26000+款怀旧游戏ROM合集 - GBA/FC/SFC/N64/NDS/PS中文版下载

SEO_DESCRIPTION=26000+款经典怀旧游戏ROM中文版合集，涵盖GBA/FC/SFC/N64/NDS/PS1/PS2/PS3/WII等全平台，含宝可梦、马里奥、塞尔达传说、最终幻想等系列中文汉化版，支持模拟器运行。

SEO_KEYWORDS=怀旧游戏,经典游戏,ROM下载,中文ROM,中文汉化版,GBA游戏,FC游戏,SFC游戏,GBC游戏,N64游戏,NDS游戏,3DS游戏,PS2游戏,PS3游戏,PS1游戏,PSP游戏,WII游戏,宝可梦,精灵宝可梦,超级马里奥,马里奥,塞尔达传说,塞尔达,最终幻想,洛克人,热血系列,魂斗罗,龙珠,火焰纹章,恶魔城,高达,游戏王,牧场物语,星之卡比,逆转裁判,合金弹头,索尼克,高级战争,火影忍者,拳皇,超级机器人大战,黄金太阳,银河战士,节奏天国,F-Zero,任天堂,红白机,GameBoy,GameBoyAdvance,超级任天堂,GBA模拟器,FC模拟器,SFC模拟器,童年游戏,80后游戏,90后游戏,老游戏,复古游戏,模拟器游戏,汉化游戏,游戏ROM合集,怀旧游戏大全,模拟器中文版ROM

SEO_AUTHOR=Game ROM Collection

SEO_SITE_NAME=经典怀旧游戏 ROM 合集

SEO_DOMAIN=https://si1110.github.io/game-rom/

SEO_IMAGE=https://si1110.github.io/game-rom/docs/logo.png
```
