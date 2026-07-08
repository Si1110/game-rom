/**
 * 全局搜索功能 - 搜索所有 section 页面中的游戏卡片
 * 支持搜索游戏名称和简介，最多显示前 9 个匹配结果
 */

(function() {
    'use strict';

    // 检测当前页面路径，判断是主页还是 section 页面
    const isIndexPage = !window.location.pathname.includes('/sections/');
    const sectionsPath = isIndexPage ? './sections/' : './';

    // Section 配置
    const SECTIONS = [
        { file: 'section-01.html', name: '马里奥系列' },
        { file: 'section-02.html', name: '宝可梦系列' },
        { file: 'section-03.html', name: '塞尔达传说系列' },
        { file: 'section-04.html', name: '最终幻想系列' },
        { file: 'section-05.html', name: '勇者斗恶龙系列' },
        { file: 'section-06.html', name: '魂斗罗系列' },
        { file: 'section-07.html', name: '恶魔城系列' },
        { file: 'section-08.html', name: '洛克人系列' },
        { file: 'section-09.html', name: '龙珠系列' },
        { file: 'section-10.html', name: '火焰纹章系列' },
        { file: 'section-11.html', name: '高达系列' },
        { file: 'section-12.html', name: '拳皇系列' },
        { file: 'section-13.html', name: '合金弹头系列' },
        { file: 'section-14.html', name: '传说系列' },
        { file: 'section-15.html', name: '游戏王系列' },
        { file: 'section-16.html', name: '星之卡比系列' },
        { file: 'section-17.html', name: '牧场物语系列' },
        { file: 'section-18.html', name: '超级机器人大战系列' },
        { file: 'section-19.html', name: '银河战士系列' },
        { file: 'section-20.html', name: '索尼克系列' },
        { file: 'section-21.html', name: '火影忍者系列' },
        { file: 'section-22.html', name: '真女神转生系列' },
        { file: 'section-23.html', name: '魔法系列' },
        { file: 'section-24.html', name: '逆转裁判系列' },
        { file: 'section-25.html', name: '黄金太阳系列' },
        { file: 'section-26.html', name: '我们的太阳系列' },
        { file: 'section-27.html', name: '高级战争系列' },
        { file: 'section-28.html', name: '鬼武者系列' },
        { file: 'section-29.html', name: '光明之魂系列' },
        { file: 'section-30.html', name: '侦探系列' },
        { file: 'section-31.html', name: '热血系列' },
        { file: 'section-32.html', name: '蜡笔小新系列' },
        { file: 'section-33.html', name: '网球王子系列' },
        { file: 'section-34.html', name: '瓦力欧系列' },
        { file: 'section-35.html', name: '马力欧系列' },
        { file: 'section-36.html', name: '召唤之夜系列' },
        { file: 'section-37.html', name: '任天堂明星大乱斗系列' },
        { file: 'section-38.html', name: 'F-Zero系列' },
        { file: 'section-39.html', name: '星际火狐系列' },
        { file: 'section-40.html', name: '耀西系列' },
        { file: 'section-41.html', name: '动物森林系列' },
        { file: 'section-42.html', name: '水上摩托系列' },
        { file: 'section-43.html', name: '越野摩托系列' },
        { file: 'section-44.html', name: '组合机器人系列' },
        { file: 'section-45.html', name: 'CT特种部队系列' },
        { file: 'section-46.html', name: '节奏天国系列' },
        { file: 'section-47.html', name: '罪与罚系列' },
        { file: 'section-48.html', name: '决战三国系列' },
        { file: 'section-49.html', name: 'FC红白机系列' },
        { file: 'section-50.html', name: 'GBA系列' },
        { file: 'section-51.html', name: 'N64系列' },
        { file: 'section-52.html', name: 'NDS系列' },
        { file: 'section-53.html', name: 'SFC超任系列' },
        { file: 'section-54.html', name: '其他游戏精选' },
        { file: 'section-55.html', name: '其他游戏' }
    ];

    const MAX_RESULTS = 9; // 最多显示 9 个结果

    /**
     * 从 HTML 中提取卡片信息
     * @param {string} html - section 页面的 HTML 内容
     * @param {string} sectionName - section 名称
     * @param {string} sectionFile - section 文件名
     * @returns {Array} 卡片信息数组
     */
    function extractCards(html, sectionName, sectionFile) {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const cards = [];

        // 查找所有卡片
        const cardElements = doc.querySelectorAll('.card.mb-3.bold-border');
        
        cardElements.forEach((card) => {
            try {
                // 提取标题
                const titleElement = card.querySelector('.card-title');
                const title = titleElement ? titleElement.textContent.trim() : '';

                // 生成唯一的锚点ID（使用标题的简化版本）
                const anchorId = title ? 'card-' + title.replace(/[^a-zA-Z0-9\u4e00-\u9fa5]/g, '-').substring(0, 50) : '';

                // 提取简介（在 list-group-item-primary 中）
                const descElement = card.querySelector('.list-group-item-primary');
                const description = descElement ? descElement.textContent.trim() : '';

                // 提取缩略图
                const imgElement = card.querySelector('img.card-img');
                const thumbnail = imgElement ? imgElement.getAttribute('src') : '';

                // 提取语言信息
                const langElement = card.querySelector('.list-group-item-success');
                const language = langElement ? langElement.textContent.trim() : '';

                // 提取字幕信息
                const subElement = card.querySelector('.list-group-item-info');
                const subtitle = subElement ? subElement.textContent.trim() : '';

                if (title) {
                    cards.push({
                        title,
                        anchorId,
                        description,
                        thumbnail,
                        language,
                        subtitle,
                        sectionName,
                        sectionFile
                    });
                }
            } catch (error) {
                console.warn('解析卡片时出错:', error);
            }
        });

        return cards;
    }

    /**
     * 搜索所有 section 中的卡片
     * @param {string} keyword - 搜索关键字
     * @returns {Promise<Array>} 匹配的卡片数组
     */
    async function searchAllSections(keyword) {
        if (!keyword || keyword.trim().length === 0) {
            return [];
        }

        const keywordLower = keyword.toLowerCase();
        const allCards = [];

        // 并行加载所有 section 页面
        const promises = SECTIONS.map(async (section) => {
            try {
                const response = await fetch(`${sectionsPath}${section.file}`);
                if (!response.ok) {
                    console.warn(`无法加载 ${section.file}`);
                    return [];
                }

                const html = await response.text();
                return extractCards(html, section.name, section.file);
            } catch (error) {
                console.error(`加载 ${section.file} 时出错:`, error);
                return [];
            }
        });

        const results = await Promise.all(promises);
        results.forEach(cards => allCards.push(...cards));

        // 过滤匹配的卡片（搜索标题和简介）
        const matchedCards = allCards.filter(card => {
            const titleMatch = card.title.toLowerCase().includes(keywordLower);
            const descMatch = card.description.toLowerCase().includes(keywordLower);
            return titleMatch || descMatch;
        });

        // 只返回前 9 个结果
        return matchedCards.slice(0, MAX_RESULTS);
    }

    /**
     * 渲染搜索结果
     * @param {Array} results - 搜索结果数组
     * @param {string} keyword - 搜索关键字
     */
    function renderSearchResults(results, keyword) {
        const resultsContainer = document.getElementById('searchResults');
        const modalTitle = document.getElementById('searchModalLabel');

        if (results.length === 0) {
            modalTitle.textContent = '搜索结果';
            resultsContainer.innerHTML = `
                <div class="text-center text-muted py-5">
                    <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" fill="currentColor" class="bi bi-search" viewBox="0 0 16 16">
                        <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"/>
                    </svg>
                    <p class="mt-3">未找到包含 "<strong>${keyword}</strong>" 的内容</p>
                    <small>请尝试其他关键字</small>
                </div>
            `;
            return;
        }

        modalTitle.textContent = `找到 ${results.length} 个结果`;

        // 渲染卡片
        let html = '<div class="row">';
        results.forEach((card, index) => {
            // 高亮显示关键字
            const highlightedTitle = highlightKeyword(card.title, keyword);
            
            // 截断简介到 100 字符
            let displayDesc = card.description.length > 100 
                ? card.description.substring(0, 100) + '...' 
                : card.description;
            const highlightedDesc = highlightKeyword(displayDesc, keyword);

            // 修正缩略图路径
            let thumbnailPath = card.thumbnail;
            if (thumbnailPath) {
                // 如果在主页，添加 sections/ 前缀；如果在 section 页面，保持不变
                thumbnailPath = isIndexPage ? `./sections/${thumbnailPath}` : thumbnailPath;
            }

            // 修正跳转链接，添加锚点
            const sectionLink = isIndexPage ? `./sections/${card.sectionFile}#${card.anchorId}` : `./${card.sectionFile}#${card.anchorId}`;
            
            // 判断是否是当前页面
            const isCurrentPage = !isIndexPage && window.location.pathname.includes(card.sectionFile);

            html += `
                <div class="col-md-6 col-lg-4 mb-3">
                    <div class="card h-100">
                        ${thumbnailPath ? `<img src="${thumbnailPath}" class="card-img-top" alt="${card.title}" style="height: 150px; object-fit: cover;">` : ''}
                        <div class="card-body">
                            <h6 class="card-title" style="color: #000; background: none; padding: 0; margin-bottom: 10px;">${highlightedTitle}</h6>
                            <p class="card-text small text-muted">${highlightedDesc}</p>
                            <div class="d-flex justify-content-between align-items-center mt-2">
                                <small class="text-muted">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="currentColor" viewBox="0 0 16 16">
                                        <path d="M9.293 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V4.707A1 1 0 0 0 13.707 4L10 .293A1 1 0 0 0 9.293 0zM9.5 3.5v-2l3 3h-2a1 1 0 0 1-1-1zM4.5 9a.5.5 0 0 1 0-1h7a.5.5 0 0 1 0 1h-7zM4 10.5a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7a.5.5 0 0 1-.5-.5zm.5 2.5a.5.5 0 0 1 0-1h4a.5.5 0 0 1 0 1h-4z"/>
                                    </svg>
                                    ${card.sectionName}
                                </small>
                                <a href="${sectionLink}" 
                                   class="btn btn-sm btn-outline-primary search-result-link" 
                                   data-anchor="${card.anchorId}"
                                   data-current-page="${isCurrentPage}">查看详情</a>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        });
        html += '</div>';

        resultsContainer.innerHTML = html;
        
        // 为所有"查看详情"按钮绑定点击事件
        bindSearchResultLinks();
    }

    /**
     * 为搜索结果链接绑定点击事件
     * 如果点击的是当前页面的卡片，关闭模态框并滚动到位置
     */
    function bindSearchResultLinks() {
        const links = document.querySelectorAll('.search-result-link');
        
        links.forEach(link => {
            link.addEventListener('click', function(e) {
                const isCurrentPage = this.getAttribute('data-current-page') === 'true';
                
                if (isCurrentPage) {
                    // 当前页面：阻止默认跳转，关闭模态框，滚动到锚点
                    e.preventDefault();
                    
                    const anchorId = this.getAttribute('data-anchor');
                    const targetElement = document.getElementById(anchorId);
                    
                    if (targetElement) {
                        // 关闭搜索模态框
                        const modal = bootstrap.Modal.getInstance(document.getElementById('searchModal'));
                        if (modal) {
                            modal.hide();
                        }
                        
                        // 等待模态框关闭动画完成后再滚动
                        setTimeout(() => {
                            // 更新 URL hash（不触发页面跳转）
                            history.pushState(null, null, `#${anchorId}`);
                            
                            // 滚动到目标位置
                            targetElement.scrollIntoView({ 
                                behavior: 'smooth', 
                                block: 'center' 
                            });
                            
                            // 添加高亮效果
                            targetElement.style.transition = 'all 0.5s ease';
                            targetElement.style.boxShadow = '0 0 20px rgba(212, 175, 55, 0.8)';
                            targetElement.style.transform = 'scale(1.02)';
                            
                            // 2秒后移除高亮
                            setTimeout(() => {
                                targetElement.style.boxShadow = '';
                                targetElement.style.transform = '';
                            }, 2000);
                        }, 300);
                    }
                } else {
                    // 跨页面：正常跳转（会打开新页面）
                    // 不需要做任何处理，浏览器默认行为
                }
            });
        });
    }

    /**
     * 高亮显示关键字
     * @param {string} text - 原文本
     * @param {string} keyword - 关键字
     * @returns {string} 高亮后的 HTML
     */
    function highlightKeyword(text, keyword) {
        if (!text || !keyword) return text;

        const regex = new RegExp(`(${escapeRegex(keyword)})`, 'gi');
        return text.replace(regex, '<mark>$1</mark>');
    }

    /**
     * 转义正则表达式特殊字符
     * @param {string} str - 字符串
     * @returns {string} 转义后的字符串
     */
    function escapeRegex(str) {
        return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    /**
     * 执行搜索
     */
    async function performSearch() {
        const input = document.getElementById('globalSearchInput');
        const keyword = input.value.trim();

        if (!keyword) {
            alert('请输入搜索关键字');
            return;
        }

        // 显示模态框
        const modal = new bootstrap.Modal(document.getElementById('searchModal'));
        modal.show();

        // 显示加载状态
        const resultsContainer = document.getElementById('searchResults');
        resultsContainer.innerHTML = `
            <div class="text-center py-5">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">搜索中...</span>
                </div>
                <p class="mt-3 text-muted">正在搜索 "${keyword}"...</p>
            </div>
        `;

        try {
            // 执行搜索
            const results = await searchAllSections(keyword);
            
            // 渲染结果
            renderSearchResults(results, keyword);

            console.log(`🔍 搜索 "${keyword}" 完成，找到 ${results.length} 个结果`);
        } catch (error) {
            console.error('搜索出错:', error);
            resultsContainer.innerHTML = `
                <div class="alert alert-danger">
                    <strong>搜索出错：</strong>${error.message}
                </div>
            `;
        }
    }

    // 绑定事件
    document.addEventListener('DOMContentLoaded', function() {
        const searchBtn = document.getElementById('globalSearchBtn');
        const searchInput = document.getElementById('globalSearchInput');

        if (searchBtn) {
            searchBtn.addEventListener('click', performSearch);
        }

        if (searchInput) {
            // 回车键触发搜索
            searchInput.addEventListener('keydown', function(e) {
                if (e.key === 'Enter') {
                    e.preventDefault(); // 防止表单提交
                    performSearch();
                }
            });
        }
    });

    // 暴露到全局（方便调试）
    window.performGlobalSearch = performSearch;

})();
