async function loadData() {
    try {
        const response = await fetch('data.json');
        const data = await response.json();
        const container = document.getElementById('dashboard');
        container.innerHTML = ''; 

        for (const [district, candidates] of Object.entries(data)) {
            const districtDiv = document.createElement('div');
            districtDiv.className = 'district-card';
            
            let html = `<h2>District: ${district}</h2>`;
            
            candidates.forEach(cand => {
                const burnRate = ((cand.spent / cand.raised) * 100).toFixed(1);
                const cohWidth = Math.min((cand.coh / 5000000) * 100, 100);

                // LOGIC FIX: Determine the correct badge label
                let badgeText = "Primary Rival";
                let badgeClass = "badge-rival";

                if (cand.is_impact) {
                    badgeText = "Impact Endorsed";
                    badgeClass = "badge-impact";
                } else if (cand.name.includes("(Incumbent)")) {
                    badgeText = "General Opponent (Incumbent)";
                    badgeClass = "badge-rival"; // Keeps the red color for opponents
                }

                html += `
                    <div class="candidate-block">
                        <div class="header-row">
                            <span class="name">${cand.name} ${cand.is_impact ? '⭐' : ''}</span>
                            <span class="badge ${badgeClass}">${badgeText}</span>
                        </div>
                        
                        <div class="metrics-grid">
                            <div class="metric-box">
                                <span class="label">Total Raised</span>
                                <span class="val">$${cand.raised.toLocaleString()}</span>
                            </div>
                            <div class="metric-box">
                                <span class="label">Total Spent</span>
                                <span class="val">$${cand.spent.toLocaleString()}</span>
                            </div>
                            <div class="metric-box">
                                <span class="label">Cash on Hand</span>
                                <span class="val" style="color: ${cand.is_impact ? '#38a169' : '#e53e3e'}">
                                    $${cand.coh.toLocaleString()}
                                </span>
                            </div>
                        </div>

                        <div class="progress-bar">
                            <div class="fill" style="width: ${cohWidth}%; background: ${cand.is_impact ? '#38a169' : '#e53e3e'}"></div>
                        </div>
                        
                        <div class="footer-info">
                            <span>Burn Rate: ${burnRate}%</span>
                            <span>As of ${cand.updated}</span>
                        </div>
                    </div>
                `;
            });
            
            districtDiv.innerHTML = html;
            container.appendChild(districtDiv);
        }
    } catch (e) {
        console.error(e);
    }
}
loadData();
