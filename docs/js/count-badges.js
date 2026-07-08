/**
 * 自动统计各 section 页面的卡片数量并更新徽章数字
 * 通过异步加载 section 页面，统计卡片数量后更新主页徽章
 */

(function() {
    'use strict';

    // Section 配置：section 文件名 -> 对应的徽章元素选择器
    const SECTIONS = [
        { file: 'section-01.html', index: 0 },
        { file: 'section-02.html', index: 1 },
        { file: 'section-03.html', index: 2 },
        { file: 'section-04.html', index: 3 },
        { file: 'section-05.html', index: 4 },
        { file: 'section-06.html', index: 5 },
        { file: 'section-07.html', index: 6 },
        { file: 'section-08.html', index: 7 },
        { file: 'section-09.html', index: 8 },
        { file: 'section-10.html', index: 9 },
        { file: 'section-11.html', index: 10 },
        { file: 'section-12.html', index: 11 },
        { file: 'section-13.html', index: 12 },
        { file: 'section-14.html', index: 13 },
        { file: 'section-15.html', index: 14 },
        { file: 'section-16.html', index: 15 },
        { file: 'section-17.html', index: 16 },
        { file: 'section-18.html', index: 17 },
        { file: 'section-19.html', index: 18 },
        { file: 'section-20.html', index: 19 },
        { file: 'section-21.html', index: 20 },
        { file: 'section-22.html', index: 21 },
        { file: 'section-23.html', index: 22 },
        { file: 'section-24.html', index: 23 },
        { file: 'section-25.html', index: 24 },
        { file: 'section-26.html', index: 25 },
        { file: 'section-27.html', index: 26 },
        { file: 'section-28.html', index: 27 },
        { file: 'section-29.html', index: 28 },
        { file: 'section-30.html', index: 29 },
        { file: 'section-31.html', index: 30 },
        { file: 'section-32.html', index: 31 },
        { file: 'section-33.html', index: 32 },
        { file: 'section-34.html', index: 33 },
        { file: 'section-35.html', index: 34 },
        { file: 'section-36.html', index: 35 },
        { file: 'section-37.html', index: 36 },
        { file: 'section-38.html', index: 37 },
        { file: 'section-39.html', index: 38 },
        { file: 'section-40.html', index: 39 },
        { file: 'section-41.html', index: 40 },
        { file: 'section-42.html', index: 41 },
        { file: 'section-43.html', index: 42 },
        { file: 'section-44.html', index: 43 },
        { file: 'section-45.html', index: 44 },
        { file: 'section-46.html', index: 45 },
        { file: 'section-47.html', index: 46 },
        { file: 'section-48.html', index: 47 },
        { file: 'section-49.html', index: 48 },
        { file: 'section-50.html', index: 49 },
        { file: 'section-51.html', index: 50 },
        { file: 'section-52.html', index: 51 },
        { file: 'section-53.html', index: 52 },
        { file: 'section-54.html', index: 53 },
        { file: 'section-55.html', index: 54 }
    ];

    /**
     * 通过 fetch 加载 section 页面并统计卡片数量
     * @param {string} sectionFile - section 文件名
     * @returns {Promise<number>} 卡片数量
     */
    async function countCardsInSection(sectionFile) {
        try {
            const response = await fetch(`./sections/${sectionFile}`);
            if (!response.ok) {
                console.warn(`⚠️ 无法加载 ${sectionFile}: ${response.status}`);
                return 0;
            }

            const html = await response.text();
            
            // 使用正则表达式统计卡片数量（更可靠）
            const pattern = /<div\s+class="card\s+mb-3\s+bold-border"/gi;
            const matches = html.match(pattern);
            return matches ? matches.length : 0;
        } catch (error) {
            console.error(`❌ 统计 ${sectionFile} 时出错:`, error);
            return 0;
        }
    }

    /**
     * 更新指定徽章的数字
     * @param {number} index - 徽章索引（0-7）
     * @param {number} count - 卡片数量
     */
    function updateBadge(index, count) {
        // 获取所有徽章元素
        const badges = document.querySelectorAll('.section-badge');
        
        if (index < 0 || index >= badges.length) {
            console.warn(`⚠️ 徽章索引 ${index} 超出范围`);
            return;
        }

        const badge = badges[index];
        const oldText = badge.textContent;
        
        // 保留原有格式（如 "82+ 款" 中的 "+"）
        const hasPlus = oldText.includes('+');
        const newText = hasPlus ? `${count}+ 款` : `${count} 款`;
        
        // 更新徽章文本
        badge.textContent = newText;
        
        console.log(`✓ 更新徽章 [${index}]: ${oldText} → ${newText}`);
    }

    /**
     * 统计所有 section 并更新徽章
     */
    async function updateAllBadges() {
        console.log('📊 开始统计各 section 页面的卡片数量...');
        
        const startTime = performance.now();
        
        // 并行加载所有 section 页面
        const promises = SECTIONS.map(async (section) => {
            const count = await countCardsInSection(section.file);
            updateBadge(section.index, count);
            return { file: section.file, count };
        });

        // 等待所有统计完成
        const results = await Promise.all(promises);
        
        const endTime = performance.now();
        const duration = (endTime - startTime).toFixed(2);
        
        console.log('✨ 徽章统计完成！');
        console.log(`⏱️ 耗时: ${duration}ms`);
        console.log('📈 统计结果:');
        results.forEach(r => {
            console.log(`   ${r.file} → ${r.count} 款`);
        });
    }

    // 页面加载完成后自动执行统计
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', updateAllBadges);
    } else {
        // DOM 已经加载完成，直接执行
        updateAllBadges();
    }

    // 暴露到全局（方便调试）
    window.updateAllBadges = updateAllBadges;

})();
