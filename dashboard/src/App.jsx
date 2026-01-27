import React, { useState, useEffect } from 'react';
import { Shield, Rocket, Target, BarChart3, AlertTriangle, CheckCircle, Upload, ChevronRight, Settings } from 'lucide-react';
import './App.css';

function App() {
    const [projectName, setProjectName] = useState('My New Launch');
    const [selectedPack, setSelectedPack] = useState('token_map.yaml');
    const [packs, setPacks] = useState([]);
    const [files, setFiles] = useState([]);
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        fetch('http://localhost:8000/packs')
            .then(res => res.json())
            .then(data => setPacks(data));
    }, []);

    const handleValidation = async () => {
        if (files.length === 0) return;
        setLoading(true);

        const formData = new FormData();
        formData.append('project_name', projectName);
        formData.append('token_map', selectedPack);
        files.forEach(f => formData.append('files', f));

        try {
            const res = await fetch('http://localhost:8000/validate', {
                method: 'POST',
                body: formData,
            });
            const data = await res.json();
            setResult(data);
        } catch (err) {
            console.error(err);
            alert('Validation failed. Make sure server.py is running on port 8000.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="dashboard-container">
            <header className="header">
                <h1>NIMDP Command Center</h1>
                <p>Gate your launch against market domination standards</p>
            </header>

            <div className="grid">
                {/* Input Panel */}
                <div className="glass-card">
                    <div className="card-header">
                        <Target className="icon primary" />
                        <h2>Launch Configuration</h2>
                    </div>

                    <div className="form-group">
                        <label>Project Name</label>
                        <input
                            type="text"
                            value={projectName}
                            onChange={(e) => setProjectName(e.target.value)}
                            className="glass-input"
                        />
                    </div>

                    <div className="form-group">
                        <label>Target NIMDP Pack</label>
                        <select
                            value={selectedPack}
                            onChange={(e) => setSelectedPack(e.target.value)}
                            className="glass-input"
                        >
                            <option value="token_map.yaml">Default Protocol</option>
                            {packs.map(p => <option key={p} value={p}>{p}</option>)}
                        </select>
                    </div>

                    <div className="form-group">
                        <label>Upload Specs</label>
                        <div className="upload-zone" onClick={() => document.getElementById('file-input').click()}>
                            <Upload />
                            <p>{files.length > 0 ? `${files.length} files selected` : "Drag or click to upload"}</p>
                            <input
                                id="file-input"
                                type="file"
                                multiple
                                hidden
                                onChange={(e) => setFiles(Array.from(e.target.files))}
                            />
                        </div>
                    </div>

                    <button
                        className="btn-primary"
                        onClick={handleValidation}
                        disabled={loading || files.length === 0}
                    >
                        {loading ? "Validating..." : "Execute Validation"}
                    </button>
                </div>

                {/* Results Overview */}
                {result && (
                    <div className="glass-card">
                        <div className="card-header">
                            <BarChart3 className="icon secondary" />
                            <h2>Validation Summary</h2>
                        </div>

                        <div className="summary-stats">
                            <div className="score-circle">
                                <span className="score-value">{Math.round(result.score * 100)}%</span>
                                <span className="score-label">Score</span>
                            </div>
                            <div className="status-container">
                                <span className={`status-badge ${result.status === 'MARKET READY' ? 'status-ready' : 'status-blocked'}`}>
                                    {result.status}
                                </span>
                                <p>{result.hard_block_triggered ? "Hard blockers detected" : "No hard blocks"}</p>
                            </div>
                        </div>

                        <div className="phase-list">
                            {Object.entries(result.phases).map(([name, phase]) => (
                                <div key={name} className="phase-item">
                                    <span>{name}</span>
                                    <div className="progress-bar">
                                        <div
                                            className="progress-fill"
                                            style={{ width: `${(phase.score_contrib / 0.3) * 100}%` }}
                                        ></div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {/* Remediation Plan */}
                {result?.remediations?.length > 0 && (
                    <div className="glass-card full-width">
                        <div className="card-header">
                            <AlertTriangle className="icon warn" />
                            <h2>Remediation Plan</h2>
                        </div>
                        <div className="remediation-grid">
                            {result.remediations.map((r, i) => (
                                <div key={i} className="remediation-item">
                                    <div className="rem-header">
                                        <span className="rem-token">{r.token}</span>
                                        <CheckCircle className="icon-sm" />
                                    </div>
                                    <p className="rem-issue">{r.issue}</p>
                                    <p className="rem-fix"><strong>Fix:</strong> {r.fix}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

export default App;
