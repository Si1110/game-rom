/**
 * SEO 元标签管理
 * 动态补充 SEO 标签，不覆盖页面已有的静态 meta 标签
 */

(function() {
    'use strict';

    const seoConfig = {
        title: '26000+款怀旧游戏ROM合集 - GBA/FC/SFC/N64/NDS/PS中文版下载',
        description: '26000+款经典怀旧游戏ROM中文版合集，涵盖GBA/FC/SFC/N64/NDS/PS1/PS2/PS3/WII等全平台，含宝可梦、马里奥、塞尔达传说、最终幻想等系列中文汉化版，支持模拟器运行。',
        keywords: '怀旧游戏,经典游戏,ROM下载,中文ROM,中文汉化版,GBA游戏,FC游戏,SFC游戏,GBC游戏,N64游戏,NDS游戏,3DS游戏,PS2游戏,PS3游戏,PS1游戏,PSP游戏,WII游戏,宝可梦,精灵宝可梦,超级马里奥,马里奥,塞尔达传说,塞尔达,最终幻想,洛克人,热血系列,魂斗罗,龙珠,火焰纹章,恶魔城,高达,游戏王,牧场物语,星之卡比,逆转裁判,合金弹头,索尼克,高级战争,火影忍者,拳皇,超级机器人大战,黄金太阳,银河战士,节奏天国,F-Zero,任天堂,红白机,GameBoy,GameBoyAdvance,超级任天堂,GBA模拟器,FC模拟器,SFC模拟器,童年游戏,80后游戏,90后游戏,老游戏,复古游戏,模拟器游戏,汉化游戏,游戏ROM合集,怀旧游戏大全,模拟器中文版ROM',
        author: 'Game ROM Collection',
        siteName: '经典怀旧游戏 ROM 合集',
        domain: 'https://si1110.github.io/game-rom/',
        image: 'https://si1110.github.io/game-rom/docs/logo.png',
        locale: 'zh_CN',

        gameSeries: [
            { name: '马里奥系列', description: '马里奥系列经典游戏ROM中文版下载，包含超级马里奥、马里奥赛车等全系列作品，支持GBA/FC/SFC模拟器运行' },
            { name: '宝可梦系列', description: '宝可梦系列经典游戏ROM中文版下载，包含宝可梦红宝石、蓝宝石、火红、叶绿、心金、魂银等全系列中文汉化版' },
            { name: '塞尔达传说系列', description: '塞尔达传说系列游戏ROM中文版下载，包含缩小帽、时之笛、梦见岛、众神的三角力量等经典作品，支持GBA/N64/SFC/Wii模拟器' },
            { name: '最终幻想系列', description: '最终幻想系列游戏ROM中文版下载，包含FF1-6代等经典日式RPG作品，支持GBA/FC/SFC模拟器' },
            { name: '勇者斗恶龙系列', description: '勇者斗恶龙系列游戏ROM中文版下载，包含DQ1-9代经典日式RPG中文汉化版' },
            { name: '魂斗罗系列', description: '魂斗罗系列游戏ROM中文版下载，包含经典FC魂斗罗、超级魂斗罗等横版射击游戏' },
            { name: '恶魔城系列', description: '恶魔城系列游戏ROM中文版下载，包含月下夜想曲、晓月圆舞曲等动作冒险经典' },
            { name: '洛克人系列', description: '洛克人系列游戏ROM中文版下载，包含洛克人X、EXE、Zero等全系列动作游戏' },
            { name: '龙珠系列', description: '龙珠系列游戏ROM中文版下载，包含龙珠Z、龙珠大冒险等动漫改编格斗游戏' },
            { name: '火焰纹章系列', description: '火焰纹章系列游戏ROM中文版下载，包含烈火之剑、圣魔之光石等经典战棋RPG' },
            { name: '高达系列', description: '高达系列游戏ROM中文版下载，包含SD高达、机动战士高达等机器人战棋游戏' },
            { name: '拳皇系列', description: '拳皇系列游戏ROM中文版下载，包含拳皇97、98、99等经典格斗游戏ROM' },
            { name: '合金弹头系列', description: '合金弹头系列游戏ROM中文版下载，包含合金弹头1-6代经典横版射击游戏' },
            { name: '传说系列', description: '传说系列游戏ROM中文版下载，包含幻想传说、永恒传说等经典日式RPG' },
            { name: '游戏王系列', description: '游戏王系列游戏ROM中文版下载，包含游戏王决斗怪兽等经典卡牌对战游戏' },
            { name: '星之卡比系列', description: '星之卡比系列游戏ROM中文版下载，包含星之卡比梦之泉等可爱风格动作游戏' },
            { name: '牧场物语系列', description: '牧场物语系列游戏ROM中文版下载，包含矿石镇、双子村等模拟经营经典' },
            { name: '超级机器人大战系列', description: '超级机器人大战系列ROM中文版下载，包含机战A/R/D/J/OG等战棋游戏' },
            { name: '银河战士系列', description: '银河战士系列游戏ROM中文版下载，包含融合、零点任务等经典动作冒险游戏' },
            { name: '索尼克系列', description: '索尼克系列游戏ROM中文版下载，蓝色刺猬的高速平台跳跃动作游戏' },
            { name: '火影忍者系列', description: '火影忍者系列游戏ROM中文版下载，火影忍者动漫改编格斗动作游戏' },
            { name: '真女神转生系列', description: '真女神转生系列游戏ROM中文版下载，包含真女神转生、恶魔召唤师等RPG' },
            { name: '魔法系列', description: '魔法系列经典游戏ROM中文版下载合集，包含魔法气泡、魔法门等经典魔法题材游戏' },
            { name: '逆转裁判系列', description: '逆转裁判系列游戏ROM中文版下载，包含逆转裁判1-3部法庭推理经典' },
            { name: '黄金太阳系列', description: '黄金太阳系列游戏ROM中文版下载，GBA平台最佳日式RPG系列中文汉化版' },
            { name: '我们的太阳系列', description: '我们的太阳系列游戏ROM中文版下载，结合阳光传感器的独特动作RPG' },
            { name: '高级战争系列', description: '高级战争系列游戏ROM中文版下载，任天堂经典战棋策略游戏中文版' },
            { name: '鬼武者系列', description: '鬼武者系列游戏ROM中文版下载，包含鬼武者战略版等动作策略游戏' },
            { name: '光明之魂系列', description: '光明之魂系列游戏ROM中文版下载，GBA平台经典暗黑Like动作RPG' },
            { name: '侦探系列', description: '侦探系列经典游戏ROM中文版下载合集，包含侦探解密、悬疑推理等经典侦探题材游戏' },
            { name: '热血系列', description: '热血系列游戏ROM中文版下载，包含热血足球、篮球、格斗等热血硬派经典' },
            { name: '蜡笔小新系列', description: '蜡笔小新系列游戏ROM中文版下载，动漫改编休闲游戏合集' },
            { name: '网球王子系列', description: '网球王子系列游戏ROM中文版下载，动漫改编网球竞技游戏' },
            { name: '瓦力欧系列', description: '瓦力欧系列游戏ROM中文版下载，包含瓦力欧制造等创意动作游戏' },
            { name: '马力欧系列', description: '马力欧系列游戏ROM中文版下载，包含超级马里奥世界等经典平台跳跃游戏' },
            { name: '召唤之夜系列', description: '召唤之夜系列游戏ROM中文版下载，包含铸剑物语等经典日式RPG' },
            { name: '任天堂明星大乱斗系列', description: '任天堂明星大乱斗游戏ROM下载，任天堂全明星跨平台格斗游戏' },
            { name: 'F-Zero系列', description: 'F-Zero系列游戏ROM中文版下载，任天堂经典高速赛车游戏' },
            { name: '星际火狐系列', description: '星际火狐系列游戏ROM中文版下载，任天堂经典空战射击游戏' },
            { name: '耀西系列', description: '耀西系列游戏ROM中文版下载，包含耀西岛等可爱风格平台跳跃游戏' },
            { name: '动物森林系列', description: '动物森友会系列游戏ROM中文版下载，任天堂治愈系模拟经营游戏' },
            { name: '水上摩托系列', description: '水上摩托系列游戏ROM中文版下载，任天堂经典水上竞速游戏' },
            { name: '越野摩托系列', description: '越野摩托系列游戏ROM中文版下载，经典摩托车竞速游戏合集' },
            { name: '组合机器人系列', description: '组合机器人系列游戏ROM中文版下载合集，创意合体机器人动作游戏' },
            { name: 'CT特种部队系列', description: 'CT特种部队系列游戏ROM中文版下载合集，经典战术动作游戏' },
            { name: '节奏天国系列', description: '节奏天国系列游戏ROM中文版下载，任天堂创意音乐节奏游戏' },
            { name: '罪与罚系列', description: '罪与罚系列游戏ROM中文版下载，N64平台经典动作射击游戏' },
            { name: '决战三国系列', description: '决战三国系列游戏ROM中文版下载，三国题材策略战棋游戏合集' },
            { name: 'FC红白机系列', description: 'FC红白机系列经典怀旧游戏ROM中文版下载，包含2700+款经典FC/NES游戏中文汉化版' },
            { name: 'GBA系列', description: 'GBA系列经典游戏ROM中文版下载，包含4400+款GBA掌机游戏中文汉化版' },
            { name: 'N64系列', description: 'N64系列经典游戏ROM中文版下载，包含400款N64主机游戏中文汉化版' },
            { name: 'NDS系列', description: 'NDS系列经典游戏ROM中文版下载，包含5200款NDS掌机游戏中文汉化版' },
            { name: 'SFC超任系列', description: 'SFC超任系列经典游戏ROM中文版下载，包含3000+款SFC超任游戏中文汉化版' },
            { name: '其他游戏精选', description: '其他游戏精选经典游戏ROM合集，包含各平台精选怀旧游戏中文版' },
            { name: '其他游戏', description: '更多经典怀旧游戏ROM合集，包含各平台未分类经典游戏中文汉化版' }
        ]
    };

    function metaExists(name, attr, value) {
        const selector = name === 'property'
            ? `meta[property="${value}"]`
            : `meta[name="${value}"]`;
        return document.querySelector(selector) !== null;
    }

    function linkExists(rel) {
        return document.querySelector(`link[rel="${rel}"]`) !== null;
    }

    function createMetaTag(attrs) {
        const meta = document.createElement('meta');
        Object.keys(attrs).forEach(function(key) {
            meta.setAttribute(key, attrs[key]);
        });
        return meta;
    }

    function createLinkTag(attrs) {
        const link = document.createElement('link');
        Object.keys(attrs).forEach(function(key) {
            link.setAttribute(key, attrs[key]);
        });
        return link;
    }

    function insertSEOTags() {
        var head = document.head;
        var fragment = document.createDocumentFragment();

        var pageUrl = window.location.href.split('?')[0].split('#')[0];
        var pageTitle = document.title;
        var pageDesc = document.querySelector('meta[name="description"]');
        var pageKeywords = document.querySelector('meta[name="keywords"]');

        // Only set global title if page has no specific title
        if (pageTitle === '' || pageTitle === '26000+款怀旧游戏ROM合集 - 旧梦游戏站' || pageTitle === seoConfig.title) {
            document.title = seoConfig.title;
        }

        // Basic SEO tags - skip if already exists
        var basicTags = [
            { name: 'description', content: seoConfig.description },
            { name: 'keywords', content: seoConfig.keywords },
            { name: 'author', content: seoConfig.author },
            { name: 'robots', content: 'index, follow' },
            { name: 'googlebot', content: 'index, follow' },
            { name: 'bingbot', content: 'index, follow' }
        ];

        basicTags.forEach(function(attrs) {
            if (!metaExists('name', 'name', attrs.name)) {
                fragment.appendChild(createMetaTag(attrs));
            }
        });

        // Canonical - only if not already set
        if (!linkExists('canonical')) {
            var canonicalLink = document.createElement('link');
            canonicalLink.rel = 'canonical';
            canonicalLink.href = pageUrl;
            fragment.appendChild(canonicalLink);
        }

        // Open Graph - skip if already exists
        var ogTags = [
            { property: 'og:title', content: pageTitle || seoConfig.title },
            { property: 'og:description', content: pageDesc ? pageDesc.getAttribute('content') : seoConfig.description },
            { property: 'og:type', content: 'website' },
            { property: 'og:image', content: seoConfig.image },
            { property: 'og:url', content: pageUrl },
            { property: 'og:site_name', content: seoConfig.siteName },
            { property: 'og:locale', content: seoConfig.locale }
        ];

        ogTags.forEach(function(attrs) {
            if (!metaExists('property', 'property', attrs.property)) {
                fragment.appendChild(createMetaTag(attrs));
            }
        });

        // Twitter Card - skip if already exists
        var twitterTags = [
            { name: 'twitter:card', content: 'summary_large_image' },
            { name: 'twitter:title', content: pageTitle || seoConfig.title },
            { name: 'twitter:description', content: pageDesc ? pageDesc.getAttribute('content') : seoConfig.description },
            { name: 'twitter:image', content: seoConfig.image }
        ];

        twitterTags.forEach(function(attrs) {
            if (!metaExists('name', 'name', attrs.name)) {
                fragment.appendChild(createMetaTag(attrs));
            }
        });

        // Mobile optimization
        var mobileTags = [
            { name: 'mobile-web-app-capable', content: 'yes' },
            { name: 'apple-mobile-web-app-capable', content: 'yes' },
            { name: 'apple-mobile-web-app-status-bar-style', content: 'black' }
        ];

        mobileTags.forEach(function(attrs) {
            if (!metaExists('name', 'name', attrs.name)) {
                fragment.appendChild(createMetaTag(attrs));
            }
        });

        // Language alternates
        var langLinks = [
            { rel: 'alternate', hreflang: 'zh', href: seoConfig.domain },
            { rel: 'alternate', hreflang: 'x-default', href: seoConfig.domain }
        ];

        langLinks.forEach(function(attrs) {
            var sel = 'link[rel="alternate"][hreflang="' + attrs.hreflang + '"]';
            if (!document.querySelector(sel)) {
                fragment.appendChild(createLinkTag(attrs));
            }
        });

        if (!document.querySelector('link[rel="apple-touch-icon"]')) {
            fragment.appendChild(createLinkTag({
                rel: 'apple-touch-icon',
                href: './docs/favicon.png'
            }));
        }

        head.appendChild(fragment);
    }

    function init() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', insertSEOTags);
        } else {
            insertSEOTags();
        }
    }

    init();

    window.SEOConfig = seoConfig;

})();
