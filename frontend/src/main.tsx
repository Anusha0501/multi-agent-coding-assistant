import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';

type AgentResult = {
  agent: string;
  status: string;
  summary: string;
  handoff: string;
  artifacts: Record<string, unknown>;
};

type RunResponse = {
  final_output: string;
  results: AgentResult[];
};

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';

function App() {
  const [task, setTask] = useState('Add logging and tests to the API');
  const [repoUrl, setRepoUrl] = useState('https://github.com/Anusha0501/multi-agent-coding-assistant');
  const [run, setRun] = useState<RunResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function submitRun(event: React.FormEvent) {
    event.preventDefault();
    setLoading(true);
    setError(null);
    setRun(null);
    try {
      const response = await fetch(`${API_URL}/api/runs`, {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ task, repo_url: repoUrl }),
      });
      if (!response.ok) {
        throw new Error(await response.text());
      }
      setRun(await response.json());
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="shell">
      <section className="hero">
        <p className="eyebrow">Staff AI Engineer Learning Project</p>
        <h1>Multi-Agent Coding Assistant</h1>
        <p>Learn how Devin, Cognition, and OpenHands-style systems plan, code, review, and test changes.</p>
      </section>

      <form className="card" onSubmit={submitRun}>
        <label>
          Task
          <textarea value={task} onChange={(event) => setTask(event.target.value)} />
        </label>
        <label>
          GitHub repository URL
          <input value={repoUrl} onChange={(event) => setRepoUrl(event.target.value)} />
        </label>
        <button disabled={loading}>{loading ? 'Running agents…' : 'Run workflow'}</button>
      </form>

      {error && <pre className="error">{error}</pre>}

      {run && (
        <section className="timeline">
          <h2>Final Output</h2>
          <pre>{run.final_output}</pre>
          {run.results.map((result) => (
            <article className="card" key={result.agent}>
              <h3>{result.agent}</h3>
              <p><strong>Status:</strong> {result.status}</p>
              <p>{result.summary}</p>
              <p><strong>Handoff:</strong> {result.handoff}</p>
              <details>
                <summary>Artifacts</summary>
                <pre>{JSON.stringify(result.artifacts, null, 2)}</pre>
              </details>
            </article>
          ))}
        </section>
      )}
    </main>
  );
}

createRoot(document.getElementById('root')!).render(<App />);
