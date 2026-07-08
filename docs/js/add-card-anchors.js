/**
 * 为所有游戏卡片添加唯一的锚点ID
 * 用于支持从搜索结果直接跳转到对应卡片位置
 */

(function() {
    'use strict';

    /**
     * 生成锚点ID（基于标题）
     * @param {string} title - 卡片标题
     * @returns {string} 锚点ID
     */
    function generateAnchorId(title) {
        if (!title) return '';
        // 移除特殊字符，保留字母、数字和中文，用连字符替换
        return 'card-' + title.replace(/[^a-zA-Z0-9\u4e00-\u9fa5]/g, '-').substring(0, 50);
    }

    /**
     * 为所有卡片添加ID
     */
    function addCardAnchors() {
        // 查找所有游戏卡片
        const cards = document.querySelectorAll('.card.mb-3.bold-border');
        
        cards.forEach((card, index) => {
            // 提取标题
            const titleElement = card.querySelector('.card-title');
            if (titleElement) {
                const title = titleElement.textContent.trim();
                const anchorId = generateAnchorId(title);
                
                // 为卡片添加ID
                if (anchorId) {
                    card.setAttribute('id', anchorId);
                    
                    // 添加平滑滚动样式
                    card.style.scrollMarginTop = '100px'; // 留出顶部导航栏的空间
                }
            }
        });

        console.log(`✅ 已为 ${cards.length} 个卡片添加锚点ID`);
    }

    /**
     * 检查URL中是否有锚点，如果有则滚动到对应位置
     */
    function scrollToAnchor() {
        const hash = window.location.hash;
        if (hash) {
            // 延迟滚动，确保页面完全加载
            setTimeout(() => {
                const target = document.querySelector(hash);
                if (target) {
                    // 平滑滚动到目标
                    target.scrollIntoView({ 
                        behavior: 'smooth', 
                        block: 'center' 
                    });
                    
                    // 添加高亮效果
                    target.style.transition = 'all 0.5s ease';
                    target.style.boxShadow = '0 0 20px rgba(212, 175, 55, 0.8)';
                    target.style.transform = 'scale(1.02)';
                    
                    // 2秒后移除高亮
                    setTimeout(() => {
                        target.style.boxShadow = '';
                        target.style.transform = '';
                    }, 2000);
                    
                    console.log(`📍 已滚动到: ${hash}`);
                }
            }, 300);
        }
    }

    // 页面加载完成后执行
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            addCardAnchors();
            scrollToAnchor();
        });
    } else {
        addCardAnchors();
        scrollToAnchor();
    }

    // 监听 hash 变化（用户点击锚点链接后）
    window.addEventListener('hashchange', scrollToAnchor);

})();
