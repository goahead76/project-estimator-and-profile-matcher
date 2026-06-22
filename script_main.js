
        const form = document.getElementById('upload-form');
        const submitBtn = document.getElementById('submit-btn');
        const loader = document.getElementById('loader');
        const analyticsPanel = document.getElementById('analytics-panel');
        const resultsContainer = document.getElementById('results-container');
        const placeholderView = document.getElementById('placeholder-view');
        const matchBadge = document.getElementById('match-badge');
        const fileStatus = document.getElementById('file-status');

        let categoryChartInstance = null;
        let densityChartInstance = null;

        function escapeRegExp(string) {
            return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        }

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const fileInput = document.getElementById('pdf-file');
            const keywordsInput = document.getElementById('keywords');
            if (!fileInput.files[0]) return;

            submitBtn.disabled = true;
            submitBtn.classList.add('opacity-50');
            loader.classList.remove('hidden');
            analyticsPanel.classList.add('hidden');
            
            const formData = new FormData();
            formData.append('file', fileInput.files[0]);
            formData.append('keywords', keywordsInput.value);

            try {
                const response = await fetch('/filtered-data', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    const errData = await response.json();
                    throw new Error(errData.detail || 'Failed processing document');
                }

                const data = await response.json();
                renderDashboard(data);
                
            } catch (error) {
                alert(`Error parsing PDF: ${error.message}`);
                console.error(error);
            } finally {
                submitBtn.disabled = false;
                submitBtn.classList.remove('opacity-50');
                loader.classList.add('hidden');
            }
        });

        function renderDashboard(data) {
            placeholderView.classList.add('hidden');
            fileStatus.textContent = `Active File: ${data.filename}`;
            fileStatus.classList.remove('hidden');
            matchBadge.textContent = `${data.total_matches_found} Matches`;
            matchBadge.classList.remove('hidden');

            resultsContainer.querySelectorAll('.result-item').forEach(el => el.remove());

            if (data.results.length === 0) {
                const noResults = document.createElement('div');
                noResults.className = 'result-item text-center py-12 text-gray-500 italic text-sm';
                noResults.textContent = 'No keywords matched sentences within this document contents.';
                resultsContainer.appendChild(noResults);
            } else {
                const fragment = document.createDocumentFragment();
                data.results.forEach(item => {
                    const card = document.createElement('div');
                    card.className = 'result-item p-4 border border-gray-100 rounded-lg hover:bg-gray-50 transition bg-white shadow-sm space-y-3 mb-3';
                    
                    let highlightedText = item.sentence;
                    item.matched_keywords.forEach(keyword => {
                        const safeKeyword = escapeRegExp(keyword);
                        const regex = new RegExp(`\\b(${safeKeyword})\\b`, 'gi');
                        highlightedText = highlightedText.replace(regex, `<mark class="bg-yellow-200 text-yellow-900 rounded px-1 font-medium">$1</mark>`);
                    });

                    card.innerHTML = `
                        <p class="text-sm text-gray-700 leading-relaxed">${highlightedText}</p>
                        <div class="flex flex-wrap gap-2 pt-1 border-t border-dashed border-gray-100">
                            ${item.categories.map(cat => `
                                <span class="bg-blue-50 text-blue-700 text-xs px-2.5 py-0.5 rounded font-semibold border border-blue-100 uppercase tracking-wider">${cat}</span>
                            `).join('')}
                        </div>
                    `;
                    fragment.appendChild(card);
                });
                resultsContainer.appendChild(fragment);
            }

            if (typeof Chart !== 'undefined') {
                analyticsPanel.classList.remove('hidden');

                if (categoryChartInstance) categoryChartInstance.destroy();
                const ctxCat = document.getElementById('categoryChart').getContext('2d');
                categoryChartInstance = new Chart(ctxCat, {
                    type: 'bar',
                    data: {
                        labels: data.chart_data.categories,
                        datasets: [{
                            label: 'Matches',
                            data: data.chart_data.counts,
                            backgroundColor: '#3b82f6',
                            borderRadius: 4
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: { legend: { display: false } },
                        scales: { y: { beginAtZero: true, ticks: { precision: 0 } } }
                    }
                });

                if (densityChartInstance) densityChartInstance.destroy();
                const ctxDens = document.getElementById('densityChart').getContext('2d');
                densityChartInstance = new Chart(ctxDens, {
                    type: 'bar',
                    data: {
                        labels: data.keyword_density.labels,
                        datasets: [{
                            label: 'Occurrences',
                            data: data.keyword_density.values,
                            backgroundColor: '#10b981',
                            borderRadius: 4
                        }]
                    },
                    options: {
                        indexAxis: 'y',
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: { legend: { display: false } },
                        scales: { x: { beginAtZero: true, ticks: { precision: 0 } } }
                    }
                });
            }
        }
 
